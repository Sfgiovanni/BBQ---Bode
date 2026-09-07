"""Letter-token discovery and free-generation parsing.

RECONSTRUCTED MODULE -- NOT THE ORIGINAL.

The upstream repository never committed this file: `.gitignore` line 83 is
`*token*` (written to keep credentials out of version control) and it also
matches `src/brbbq/scoring/tokens.py`. `git log --all -- '*scoring/tokens.py'`
returns nothing, so the published tree cannot even be imported -- every entry
point fails at `from brbbq.scoring.tokens import ...`.

This reconstruction follows the contract that the rest of the tree and
`docs/METHODOLOGY.md` pin down:

  "Valid immediate token IDs discovered for A, B, and C are aggregated per
   letter with `logsumexp`; the prediction is their `argmax`. Token variants
   `A`, ` A`, and `\\nA` (and B/C) are recorded, including rejected
   multi-token variants. No token ID may belong to more than one letter."

Consumers:
  * `brbbq.models.huggingface.HuggingFaceCausalLMAdapter.option_token_metadata`
    -> `audit_letter_tokens(tokenizer)["letters"][L]["considered_token_ids"]`
  * `brbbq.scoring.runner` -> `parse_generated_option(generated)` for the
    free-generation audit rows only (100 rows in the reference run); it never
    touches the primary log-probability scoring path.

Behavioural equivalence with the original is NOT established. It is byte-exact
on nothing and verified against no test -- the upstream test suite never
referenced either function. Any *re-run of BODE* using this file must be
reported as a reconstruction, not as a reproduction of the published run. The
Maritaca adapter supplies its own `option_token_metadata` and does not call
`audit_letter_tokens` at all, so an API run is unaffected by the first
function.
"""

import re
from typing import Any, Dict, List, Optional

LETTERS = ("A", "B", "C")

#: Surface forms probed for each letter. The bare form plus the two whitespace
#: leaders a causal LM most often emits after a prompt ending in "Resposta:".
VARIANT_TEMPLATES = ("{}", " {}", "\n{}")


def _encode_variants(tokenizer, letter: str) -> Dict[str, Any]:
    """Encode every surface variant of ``letter``; split accepted/rejected.

    A variant is accepted only when it encodes to exactly one token: the score
    is read off a single next-token distribution, so a multi-token variant has
    no single logit to contribute.
    """
    accepted: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []
    for template in VARIANT_TEMPLATES:
        text = template.format(letter)
        ids = tokenizer.encode(text, add_special_tokens=False)
        record = {"variant": text, "token_ids": [int(i) for i in ids]}
        if len(ids) == 1:
            accepted.append(record)
        else:
            record["reason"] = "multi_token"
            rejected.append(record)
    return {"accepted": accepted, "rejected": rejected}


def audit_letter_tokens(tokenizer) -> Dict[str, Any]:
    """Discover the immediate token ids that stand for A, B and C.

    Returns the structure the adapters and the run manifest expect::

        {"letters": {"A": {"considered_token_ids": [...],
                           "accepted_variants": [...],
                           "rejected_variants": [...]}, ...},
         "variant_templates": [...],
         "collisions": [...],
         "reconstructed": True}

    A token id claimed by more than one letter is dropped from every letter and
    reported under ``collisions``: the contract forbids sharing, and silently
    keeping it would let one letter's probability mass leak into another's.
    """
    per_letter: Dict[str, Dict[str, Any]] = {}
    for letter in LETTERS:
        variants = _encode_variants(tokenizer, letter)
        ids: List[int] = []
        for record in variants["accepted"]:
            token_id = record["token_ids"][0]
            if token_id not in ids:
                ids.append(token_id)
        per_letter[letter] = {
            "considered_token_ids": ids,
            "accepted_variants": variants["accepted"],
            "rejected_variants": variants["rejected"],
        }

    seen: Dict[int, List[str]] = {}
    for letter, data in per_letter.items():
        for token_id in data["considered_token_ids"]:
            seen.setdefault(token_id, []).append(letter)
    collisions = [
        {"token_id": token_id, "letters": letters}
        for token_id, letters in sorted(seen.items())
        if len(letters) > 1
    ]
    shared = {entry["token_id"] for entry in collisions}
    for data in per_letter.values():
        data["considered_token_ids"] = [
            i for i in data["considered_token_ids"] if i not in shared
        ]

    empty = [letter for letter, data in per_letter.items()
             if not data["considered_token_ids"]]
    if empty:
        raise ValueError(
            "no single-token representation survived for letter(s) {}; "
            "this tokenizer cannot be scored by first-token log probability"
            .format(", ".join(empty))
        )

    return {
        "letters": per_letter,
        "variant_templates": list(VARIANT_TEMPLATES),
        "collisions": collisions,
        "reconstructed": True,
    }


#: First standalone A/B/C in the generation, optionally followed by ")" or "."
_OPTION_RE = re.compile(r"(?<![A-Za-z0-9])([ABC])(?![A-Za-z0-9])")


def parse_generated_option(generated: Optional[str]) -> Optional[str]:
    """Extract the letter a free generation settles on, or ``None``.

    Used only for the free-generation audit, which cross-checks that greedy
    decoding agrees with the log-probability argmax. Returns ``None`` when the
    generation names no letter -- disagreement and unparseability are both
    findings, so neither is papered over with a guess.
    """
    if not generated:
        return None
    match = _OPTION_RE.search(generated.strip().upper())
    return match.group(1) if match else None
