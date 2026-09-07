"""Serve first-token letter scores that were precomputed by the OpenAI Batch API.

The BR-BBQ runner is synchronous: it renders a batch of prompts and blocks on
`score_options`. The Batch API is not -- results arrive up to 24 h later. Rather
than reimplement the runner (and risk drifting from the row schema the published
BODE run used), the batch is submitted separately by `scripts/openai_batch.py`
and this adapter replays the stored results.

The runner therefore still owns everything that makes the comparison valid: the
row schema, resume/checkpointing, the metrics, and the clustered bootstrap. Only
the source of the four scoring fields changes.

Prompts are matched to stored results by SHA-1 of the rendered prompt string,
because `score_options` receives prompts, not example ids. A prompt with no
stored result is a hard error -- silently scoring it as unknown would put a hole
in the dataset that the metrics would happily average over.

`generate_free` still calls the API live: the free-generation audit is 100 rows
in total, and replaying it would mean storing a second batch for a rounding
error's worth of cost.
"""

import hashlib
import json
import os
import platform
from typing import Any, Dict, List, Sequence, Tuple

from brbbq.models.base import BaseModelAdapter
from brbbq.prompts import render_prompt

LETTERS = ("A", "B", "C")
NEG_INF = float("-inf")


def prompt_key(prompt: str) -> str:
    """Stable id for a rendered prompt; shared with the submit script."""
    return hashlib.sha1(prompt.encode("utf-8")).hexdigest()


class OpenAIReplayAdapter(BaseModelAdapter):
    """Replays stored OpenAI batch scores; generates live only for the audit."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._scores: Dict[str, Dict[str, Any]] = {}
        self._client = None
        self._served = 0
        self._missing = 0
        self._live_fallbacks = []

    # ---------------------------------------------------------------- loading
    def load_tokenizer(self) -> Any:
        return None

    def load_model(self) -> Any:
        """Load the stored batch results. Nothing is downloaded."""
        if self._scores:
            return self._scores
        path = self.config.get("results_path")
        if not path or not os.path.exists(path):
            raise RuntimeError(
                "results_path missing or not found: {!r}. Run "
                "scripts/openai_batch.py --collect first.".format(path)
            )
        with open(path, encoding="utf-8") as handle:
            self._scores = json.load(handle)
        if not self._scores:
            raise RuntimeError("{} is empty".format(path))
        return self._scores

    def _live(self):
        if self._client is None:
            from openai import OpenAI

            key = os.environ.get(self.config.get("api_key_env", "OPENAI_API_KEY"))
            if not key:
                raise RuntimeError("set OPENAI_API_KEY for the free-generation audit")
            self._client = OpenAI(api_key=key)
        return self._client

    def get_devices(self) -> List[str]:
        return ["openai-batch:{}".format(self.config.get("model_name"))]

    def render_prompt(self, example: Dict[str, Any]) -> str:
        return render_prompt(example, self.config.get("prompt_style", "simple"), None)

    # ---------------------------------------------------------------- scoring
    def option_token_metadata(self) -> Dict[str, Any]:
        return {
            "letters": {
                letter: {
                    "considered_token_ids": [],
                    "discovery": "observational",
                    "accepts": "returned top-logprob token whose stripped form == '{}'".format(
                        letter
                    ),
                }
                for letter in LETTERS
            },
            "aggregation": "logsumexp over observed variants",
            "top_logprobs": int(self.config.get("top_logprobs", 5)),
            "truncated_distribution": True,
            "missing_letter_policy": "-inf, counted per row in letters_found",
            "note": (
                "This model caps top_logprobs at 5 and its next-token distribution is "
                "highly peaked, so typically only the selected letter carries a finite "
                "log probability. predicted_option (the argmax, and every metric derived "
                "from it) is unaffected; the logprob_* columns are sparse by construction "
                "and must not be compared to the BODE run's full-vocab values."
            ),
        }

    def score_options(self, prompts: Sequence[str]) -> List[Dict[str, Any]]:
        store = self.load_model()
        rows = []
        for prompt in prompts:
            key = prompt_key(prompt)
            row = store.get(key)
            if row is None:
                # The runner probes two synthetic "neutral baseline" prompts that
                # are not part of the catalog and so were never in the batch.
                # Those get scored live. Anything beyond a handful of misses is a
                # hole in the dataset, not a probe, and must still be fatal --
                # filling it silently would let the metrics average over a gap.
                self._missing += 1
                limite = int(self.config.get("live_fallback_limit", 8))
                if self._missing > limite:
                    raise RuntimeError(
                        "{} prompts sem resultado armazenado (limite {}). O lote esta "
                        "incompleto -- rode scripts/openai_batch.py --collect de novo."
                        .format(self._missing, limite)
                    )
                row = self._score_live(prompt)
                self._live_fallbacks.append(key[:12])
            self._served += 1
            rows.append(dict(row))
        return rows

    def _score_live(self, prompt: str) -> Dict[str, Any]:
        """Score a single prompt through the live API (used only for probes)."""
        import math

        client = self._live()
        response = client.chat.completions.create(
            model=self.config["model_name"],
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=int(self.config.get("max_completion_tokens", 1)),
            temperature=0.0,
            logprobs=True,
            top_logprobs=int(self.config.get("top_logprobs", 20)),
        )
        content = response.choices[0].logprobs.content
        buckets = {L: [] for L in LETTERS}
        for cand in content[0].top_logprobs:
            letter = cand.token.strip()
            if letter in buckets:
                buckets[letter].append(cand.logprob)

        def lse(vals):
            if not vals:
                return NEG_INF
            top = max(vals)
            return top + math.log(sum(math.exp(v - top) for v in vals))

        scores = {L: lse(buckets[L]) for L in LETTERS}
        found = [L for L in LETTERS if scores[L] != NEG_INF]
        return {
            "predicted_option": max(LETTERS, key=lambda L: scores[L]) if found else None,
            "logprob_A": scores["A"], "logprob_B": scores["B"], "logprob_C": scores["C"],
            "n_input_tokens": int(response.usage.prompt_tokens or 0),
            "letters_found": len(found),
            "letters_missing": ",".join(L for L in LETTERS if scores[L] == NEG_INF),
            "top_token": content[0].token,
        }

    def generate_free(self, prompt: str, max_new_tokens: int) -> Tuple[str, int]:
        client = self._live()
        response = client.chat.completions.create(
            model=self.config["model_name"],
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=max(int(max_new_tokens), 16),
            temperature=0.0,
        )
        text = response.choices[0].message.content or ""
        return text, int(response.usage.completion_tokens or 0)

    # --------------------------------------------------------------- metadata
    def metadata(self) -> Dict[str, Any]:
        import openai

        meta = dict(self.config.get("batch_metadata") or {})
        return {
            "adapter": "openai_replay",
            "model_name": self.config.get("model_name"),
            "provider": "openai",
            "prompt_style": self.config.get("prompt_style", "simple"),
            "scoring_method": "first_token_logprob_api_batch",
            "top_logprobs": int(self.config.get("top_logprobs", 5)),
            "temperature": 0.0,
            "weights_are_remote": True,
            "revision": None,
            "revision_note": (
                "A hosted model has no pinnable revision; reproducibility is bounded "
                "by the run date, unlike the BODE run's pinned commit SHA."
            ),
            "results_path": self.config.get("results_path"),
            "rows_served": self._served,
            "rows_missing": self._missing,
            "live_fallbacks": list(self._live_fallbacks),
            "batch": meta,
            "openai_sdk": openai.__version__,
            "python": platform.python_version(),
        }
