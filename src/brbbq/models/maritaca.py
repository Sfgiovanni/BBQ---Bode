"""Maritaca (Sabiá) adapter: first-token log probabilities over an HTTP API.

The reference BODE run scores A/B/C from a local causal LM's next-token
distribution. The Maritaca chat API exposes the same quantity through
`logprobs` + `top_logprobs`, so the scoring *method* transfers rather than
being replaced by generative multiple choice.

Three deviations from the local scorer are unavoidable, and all three are
recorded per row or in `metadata()` rather than being smoothed over:

1. **Truncated distribution.** `top_logprobs` is capped at 20 by the API, so a
   letter outside the top 20 has no reported log probability. It is scored as
   ``-inf`` and the row records `letters_found` (0-3) and `letters_missing`.
   A run where this is not ~always 3 is measuring the API's truncation, not
   the model's preference.
2. **Variant discovery is observational.** The local adapter enumerates the
   token ids for ``"A"``, ``" A"``, ``"\\nA"`` up front. Here the tokenizer is
   not reachable, so variants are discovered from what the API actually
   returns: every returned token whose stripped form is a bare letter is
   aggregated into that letter with `logsumexp` -- the same aggregation, over
   an observed rather than an enumerated variant set. The variants seen are
   accumulated and reported in `metadata()`.
3. **Batch size cannot perturb results.** Each prompt is an independent HTTP
   request, so unlike the GPU path there is no batch-size/tie confound; the
   batch is only a concurrency window.

The prompt uses the repository's own `prompt_style: simple`, whose instruction
and body copy are byte-identical to what the Alpaca renderer wraps for BODE.
Only the model-family scaffolding differs -- which still means a BODE-vs-Sabiá
delta is a model *and* prompt-format delta, and must not be attributed to the
model alone.
"""

import math
import os
import platform
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Sequence, Tuple

from brbbq.models.base import BaseModelAdapter
from brbbq.prompts import render_prompt

LETTERS = ("A", "B", "C")
DEFAULT_BASE_URL = "https://chat.maritaca.ai/api"
NEG_INF = float("-inf")

#: Body `code` values that no amount of waiting will clear. A spending cap or a
#: bad key is an operator problem: burning the retry budget on it wastes minutes
#: and buries the real message under a generic "failed after N attempts".
FATAL_CODES = frozenset({
    "api_key_spending_limit_exceeded",
    "insufficient_quota",
    "invalid_api_key",
})


def _is_fatal(error: BaseException) -> bool:
    """True when retrying cannot possibly help."""
    status = getattr(error, "status_code", None)
    if status in (400, 401, 403, 404, 422):
        return True
    body = getattr(error, "body", None)
    if isinstance(body, dict):
        inner = body.get("error") if isinstance(body.get("error"), dict) else body
        if isinstance(inner, dict) and inner.get("code") in FATAL_CODES:
            return True
    return any(code in str(error) for code in FATAL_CODES)


class MaritacaAPIAdapter(BaseModelAdapter):
    """First-token log-probability scorer backed by the Maritaca chat API."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._client = None
        self._lock = threading.Lock()
        self._variants_seen: Dict[str, Dict[str, int]] = {l: {} for l in LETTERS}
        self._missing_letter_rows = 0
        self._scored_rows = 0
        self._retries = 0

    # ---------------------------------------------------------------- loading
    def load_tokenizer(self) -> Any:
        """No local tokenizer exists; scoring reads token strings off the API."""
        return None

    def load_model(self) -> Any:
        """Build the HTTP client. Nothing is downloaded and no device is used."""
        if self._client is not None:
            return self._client
        from openai import OpenAI

        key = os.environ.get(self.config.get("api_key_env", "MARITACA_API_KEY"))
        if not key:
            raise RuntimeError(
                "set {} in the environment; the key must never be written into "
                "a config file".format(self.config.get("api_key_env", "MARITACA_API_KEY"))
            )
        self._client = OpenAI(
            api_key=key,
            base_url=self.config.get("base_url", DEFAULT_BASE_URL),
            timeout=float(self.config.get("request_timeout", 60.0)),
            max_retries=0,  # retries are handled here so they can be counted
        )
        return self._client

    def get_devices(self) -> List[str]:
        return ["maritaca-api:{}".format(self.config.get("model_name"))]

    def render_prompt(self, example: Dict[str, Any]) -> str:
        return render_prompt(example, self.config.get("prompt_style", "simple"), None)

    # ---------------------------------------------------------------- scoring
    def option_token_metadata(self) -> Dict[str, Any]:
        """Describe the letter-scoring policy.

        There are no local token ids to enumerate, so `considered_token_ids` is
        empty by construction and the discovery policy is stated instead. The
        variants actually observed accumulate during the run and are reported
        by `metadata()`.
        """
        return {
            "letters": {
                letter: {
                    "considered_token_ids": [],
                    "discovery": "observational",
                    "accepts": "any returned top-logprob token whose stripped form == '{}'".format(
                        letter
                    ),
                }
                for letter in LETTERS
            },
            "aggregation": "logsumexp over observed variants",
            "top_logprobs": int(self.config.get("top_logprobs", 20)),
            "truncated_distribution": True,
            "missing_letter_policy": "-inf, counted in letters_found/letters_missing",
            "note": (
                "API-side scoring: the distribution is truncated to the top-k tokens, "
                "so absolute log probabilities are not comparable to a local full-vocab "
                "softmax. Letter *ordering* and argmax are."
            ),
        }

    def _score_one(self, prompt: str) -> Dict[str, Any]:
        client = self.load_model()
        top_k = int(self.config.get("top_logprobs", 20))
        attempts = int(self.config.get("max_attempts", 6))
        last: BaseException = RuntimeError("unreached")
        for attempt in range(attempts):
            try:
                response = client.chat.completions.create(
                    model=self.config["model_name"],
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1,
                    temperature=0.0,
                    logprobs=True,
                    top_logprobs=top_k,
                )
                return self._parse(response)
            except BaseException as error:  # noqa: BLE001 - retried then re-raised
                last = error
                if _is_fatal(error):
                    raise RuntimeError(
                        "Maritaca refused the request and retrying cannot help: {}".format(error)
                    ) from error
                if attempt == attempts - 1:
                    break
                with self._lock:
                    self._retries += 1
                time.sleep(min(2.0 ** attempt, 30.0))
        raise RuntimeError("Maritaca scoring failed after {} attempts: {}".format(attempts, last))

    def _parse(self, response: Any) -> Dict[str, Any]:
        choice = response.choices[0]
        content = getattr(choice.logprobs, "content", None) if choice.logprobs else None
        buckets: Dict[str, List[float]] = {letter: [] for letter in LETTERS}
        variants: Dict[str, List[str]] = {letter: [] for letter in LETTERS}
        if content:
            for candidate in content[0].top_logprobs:
                letter = candidate.token.strip()
                if letter in buckets:
                    buckets[letter].append(candidate.logprob)
                    variants[letter].append(candidate.token)

        scores = {}
        for letter in LETTERS:
            values = buckets[letter]
            scores[letter] = _logsumexp(values) if values else NEG_INF

        found = [letter for letter in LETTERS if scores[letter] != NEG_INF]
        prediction = max(LETTERS, key=lambda l: scores[l]) if found else None

        with self._lock:
            self._scored_rows += 1
            if len(found) < len(LETTERS):
                self._missing_letter_rows += 1
            for letter in LETTERS:
                for token in variants[letter]:
                    self._variants_seen[letter][token] = (
                        self._variants_seen[letter].get(token, 0) + 1
                    )

        usage = getattr(response, "usage", None)
        return {
            "predicted_option": prediction,
            "logprob_A": scores["A"],
            "logprob_B": scores["B"],
            "logprob_C": scores["C"],
            "n_input_tokens": int(getattr(usage, "prompt_tokens", 0) or 0),
            "letters_found": len(found),
            "letters_missing": ",".join(l for l in LETTERS if scores[l] == NEG_INF),
            "top_token": content[0].token if content else None,
        }

    def score_options(self, prompts: Sequence[str]) -> List[Dict[str, Any]]:
        """Score a batch concurrently, preserving input order."""
        prompts = list(prompts)
        if not prompts:
            return []
        workers = min(len(prompts), int(self.config.get("max_concurrency", 16)))
        if workers <= 1:
            return [self._score_one(prompt) for prompt in prompts]
        with ThreadPoolExecutor(max_workers=workers) as pool:
            return list(pool.map(self._score_one, prompts))

    def generate_free(self, prompt: str, max_new_tokens: int) -> Tuple[str, int]:
        client = self.load_model()
        response = client.chat.completions.create(
            model=self.config["model_name"],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=int(max_new_tokens),
            temperature=0.0,
        )
        text = response.choices[0].message.content or ""
        usage = getattr(response, "usage", None)
        return text, int(getattr(usage, "completion_tokens", 0) or 0)

    # --------------------------------------------------------------- metadata
    def metadata(self) -> Dict[str, Any]:
        import openai

        with self._lock:
            observed = {
                letter: dict(sorted(counts.items(), key=lambda kv: -kv[1]))
                for letter, counts in self._variants_seen.items()
            }
            scored, missing, retries = self._scored_rows, self._missing_letter_rows, self._retries
        return {
            "adapter": "maritaca_api",
            "model_name": self.config.get("model_name"),
            "base_url": self.config.get("base_url", DEFAULT_BASE_URL),
            "prompt_style": self.config.get("prompt_style", "simple"),
            "scoring_method": "first_token_logprob_api",
            "top_logprobs": int(self.config.get("top_logprobs", 20)),
            "max_concurrency": int(self.config.get("max_concurrency", 16)),
            "temperature": 0.0,
            "max_tokens": 1,
            "weights_are_remote": True,
            "revision": None,
            "revision_note": (
                "A hosted model has no pinnable revision: Maritaca can change the "
                "weights behind '{}' without notice. Reproducibility is bounded by "
                "the run date, unlike the BODE run's pinned commit SHA."
            ).format(self.config.get("model_name")),
            "observed_letter_variants": observed,
            "rows_scored": scored,
            "rows_with_missing_letter": missing,
            "http_retries": retries,
            "openai_sdk": openai.__version__,
            "python": platform.python_version(),
        }


def _logsumexp(values: Sequence[float]) -> float:
    finite = [v for v in values if v != NEG_INF]
    if not finite:
        return NEG_INF
    top = max(finite)
    return top + math.log(sum(math.exp(v - top) for v in finite))
