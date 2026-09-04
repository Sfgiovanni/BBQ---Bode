"""Deterministic construction of paired bilingual BBQ examples."""

import hashlib
import json
import string
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import pandas as pd
import yaml


LANGUAGES = ("pt", "en")
LETTERS = ("A", "B", "C")
# Reference run 20260710_000126 built every category with exactly 3 pairs and
# used that count as the stride for the group-order/negative-actor schedules.
# Freezing it here (instead of reading len(category["pairs"])) keeps those
# schedules identical for the original pairs when new pairs are appended to a
# category, so appending is a true content superset rather than a reshuffle.
# Only valid if new pairs are appended after, not inserted among, the
# original ones for a given category.
REFERENCE_PAIRS_PER_CATEGORY = 3
PERMUTATIONS = {
    0: ("group1", "group2", "unknown"),
    1: ("unknown", "group1", "group2"),
    2: ("group2", "unknown", "group1"),
}
CONDITIONS = (
    ("ambiguous_negative", "ambiguous", "negative"),
    ("ambiguous_non_negative", "ambiguous", "non_negative"),
    ("disambiguated_negative", "disambiguated", "negative"),
    ("disambiguated_non_negative", "disambiguated", "non_negative"),
)


def stable_id(value: str, prefix: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:20]
    return "{}_{}".format(prefix, digest)


def _jsonl(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_catalogs(
    categories_path: Path, scenarios_path: Path
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    with categories_path.open("r", encoding="utf-8") as handle:
        categories = yaml.safe_load(handle)
    scenarios = _jsonl(scenarios_path)
    return categories, scenarios


def _placeholders(text: str) -> set:
    return {name for _, name, _, _ in string.Formatter().parse(text) if name}


def _format(text: str, values: Dict[str, str]) -> str:
    expected = _placeholders(text)
    missing = expected - set(values)
    if missing:
        raise ValueError("Missing placeholders {} in {!r}".format(sorted(missing), text))
    output = text.format(**values)
    if _placeholders(output):
        raise ValueError("Unfilled placeholder in {!r}".format(output))
    return output


def _group_map(category: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    return {group["id"]: group for group in category["groups"]}


def build_base_templates(
    catalog: Dict[str, Any], scenarios: Iterable[Dict[str, Any]]
) -> pd.DataFrame:
    rows = []
    scenarios = list(scenarios)
    for category_index, category in enumerate(catalog["categories"]):
        for scenario in scenarios:
            rows.append(
                {
                    "template_id": "{}.{}".format(category["id"], scenario["scenario_id"]),
                    "category_id": category["id"],
                    "category_pt": category["name_pt"],
                    "category_en": category["name_en"],
                    "category_index": category_index,
                    "scenario_id": scenario["scenario_id"],
                    "scenario_index": scenario["scenario_index"],
                    "aggregation": category["aggregation"],
                    "brazil_specific": bool(category["brazil_specific"]),
                    "source_status": category["source_status"],
                    "needs_human_validation": bool(
                        category.get("needs_human_validation", False)
                        or scenario.get("needs_human_validation", False)
                    ),
                }
            )
    return pd.DataFrame(rows)


def _content_for_group(group_id: str, group1_id: str) -> str:
    return "group1" if group_id == group1_id else "group2"


def build_logical_examples(
    catalog: Dict[str, Any], scenarios: List[Dict[str, Any]]
) -> pd.DataFrame:
    """Build 12 conditions per category/scenario/language."""
    unknown = catalog["unknown"]
    rows = []
    for category in catalog["categories"]:
        groups = _group_map(category)
        for scenario in scenarios:
            scenario_index = int(scenario["scenario_index"])
            template_id = "{}.{}".format(category["id"], scenario["scenario_id"])
            for pair_index, pair in enumerate(category["pairs"]):
                target_id, comparison_id = pair["target"], pair["comparison"]
                invert_order = (
                    scenario_index * REFERENCE_PAIRS_PER_CATEGORY + pair_index
                ) % 2 == 1
                group1_id, group2_id = (
                    (comparison_id, target_id) if invert_order else (target_id, comparison_id)
                )
                target_content = _content_for_group(target_id, group1_id)
                comparison_content = _content_for_group(comparison_id, group1_id)
                pair_sequence = scenario_index * REFERENCE_PAIRS_PER_CATEGORY + pair_index
                # 0011 schedule is orthogonal to the 0101 group-order schedule.
                target_is_negative = (pair_sequence // 2) % 2 == 0
                negative_content = target_content if target_is_negative else comparison_content
                positive_content = comparison_content if target_is_negative else target_content

                for condition_id, context_type, question_type in CONDITIONS:
                    semantic_block_id = stable_id(
                        "|".join([category["id"], scenario["scenario_id"], pair["id"]]),
                        "sb",
                    )
                    semantic_raw = "|".join(
                        [category["id"], scenario["scenario_id"], pair["id"], condition_id]
                    )
                    semantic_pair_id = stable_id(semantic_raw, "sp")
                    if context_type == "ambiguous":
                        correct_content = "unknown"
                    elif question_type == "negative":
                        correct_content = negative_content
                    else:
                        correct_content = positive_content
                    biased_content = (
                        target_content if question_type == "negative" else comparison_content
                    )

                    for language in LANGUAGES:
                        group1_text = groups[group1_id][language]
                        group2_text = groups[group2_id][language]
                        text = scenario["texts"][language]
                        values = {
                            "group1": group1_text,
                            "group2": group2_text,
                            "negative_actor": group1_text
                            if negative_content == "group1"
                            else group2_text,
                            "positive_actor": group1_text
                            if positive_content == "group1"
                            else group2_text,
                        }
                        context_key = "{}_context".format(context_type)
                        question_key = (
                            "negative_question"
                            if question_type == "negative"
                            else "non_negative_question"
                        )
                        logical_id = stable_id(semantic_raw + "|" + language, "log")
                        rows.append(
                            {
                                "semantic_pair_id": semantic_pair_id,
                                "semantic_block_id": semantic_block_id,
                                "logical_id": logical_id,
                                "language": language,
                                "template_id": template_id,
                                "category_id": category["id"],
                                "category": category["name_pt"]
                                if language == "pt"
                                else category["name_en"],
                                "category_pt": category["name_pt"],
                                "category_en": category["name_en"],
                                "aggregation": category["aggregation"],
                                "brazil_specific": bool(category["brazil_specific"]),
                                "scenario_id": scenario["scenario_id"],
                                "scenario_index": scenario_index,
                                "pair_id": pair["id"],
                                "pair_index": pair_index,
                                "group_order_inverted": invert_order,
                                "group1_id": group1_id,
                                "group2_id": group2_id,
                                "group1": group1_text,
                                "group2": group2_text,
                                "bias_target_id": pair["stereotype_target"],
                                "bias_target_content": target_content,
                                "biased_content": biased_content,
                                "negative_actor_content": negative_content,
                                "positive_actor_content": positive_content,
                                "condition_id": condition_id,
                                "context_type": context_type,
                                "question_type": question_type,
                                "context": _format(text[context_key], values),
                                "question": _format(text[question_key], values),
                                "correct_content": correct_content,
                                "semantic_correct_answer": (
                                    unknown["id"]
                                    if correct_content == "unknown"
                                    else group1_id
                                    if correct_content == "group1"
                                    else group2_id
                                ),
                                "semantic_biased_answer": (
                                    group1_id if biased_content == "group1" else group2_id
                                ),
                                "unknown_text": unknown[language],
                                "negative_action": text["negative_action"],
                                "positive_action": text["positive_action"],
                                "negative_action_id": "{}:negative_action".format(
                                    scenario["scenario_id"]
                                ),
                                "positive_action_id": "{}:positive_action".format(
                                    scenario["scenario_id"]
                                ),
                                "source_status": category["source_status"],
                                "pair_source": pair.get("source"),
                                "needs_human_validation": bool(
                                    category.get("needs_human_validation", False)
                                    or pair.get("needs_human_validation", False)
                                    or scenario.get("needs_human_validation", False)
                                ),
                            }
                        )
    return pd.DataFrame(rows)


def expand_permutations(logical: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for record in logical.to_dict("records"):
        labels = {
            "group1": record["group1"],
            "group2": record["group2"],
            "unknown": record["unknown_text"],
        }
        for permutation_index, layout in PERMUTATIONS.items():
            letter_of = {content: LETTERS[index] for index, content in enumerate(layout)}
            row = dict(record)
            row.update(
                {
                    "permutation_index": permutation_index,
                    "example_id": stable_id(
                        "{}|perm{}".format(record["logical_id"], permutation_index), "ex"
                    ),
                    "option_A": labels[layout[0]],
                    "option_B": labels[layout[1]],
                    "option_C": labels[layout[2]],
                    "content_of_A": layout[0],
                    "content_of_B": layout[1],
                    "content_of_C": layout[2],
                    "unknown_position": letter_of["unknown"],
                    "correct_option": letter_of[record["correct_content"]],
                    "biased_option": letter_of[record["biased_content"]],
                    "bias_target_position": letter_of[record["bias_target_content"]],
                }
            )
            rows.append(row)
    return pd.DataFrame(rows)


def build_dataset(categories_path: Path, scenarios_path: Path):
    """Return base templates, logical examples, and expanded evaluations."""
    catalog, scenarios = load_catalogs(categories_path, scenarios_path)
    templates = build_base_templates(catalog, scenarios)
    logical = build_logical_examples(catalog, scenarios)
    expanded = expand_permutations(logical)
    return templates, logical, expanded
