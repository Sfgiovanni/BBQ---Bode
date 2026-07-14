"""Strict structural and balance validation for the bilingual dataset."""

from typing import Any, Dict, List

import pandas as pd

from brbbq.dataset.builder import LANGUAGES


EXPECTED_CATEGORY_NAMES_PT = [
    "Regionalidade",
    "Religião",
    "Raça/cor",
    "Classe socioeconômica",
    "Gênero",
    "Educação",
    "Interior versus capital",
    "Orientação política",
    "Preferência musical",
]


def _assert_pairing(logical: pd.DataFrame) -> None:
    paired = logical.groupby("semantic_pair_id", sort=False)
    assert (paired.size() == 2).all(), "Every semantic pair must have exactly PT and EN"
    assert (paired["language"].nunique() == 2).all()
    shared = [
        "category_id",
        "scenario_id",
        "pair_id",
        "group1_id",
        "group2_id",
        "semantic_block_id",
        "bias_target_id",
        "condition_id",
        "context_type",
        "question_type",
        "correct_content",
        "biased_content",
        "semantic_correct_answer",
        "semantic_biased_answer",
        "negative_actor_content",
        "negative_action_id",
        "positive_action_id",
    ]
    for column in shared:
        assert (paired[column].nunique(dropna=False) == 1).all(), column


def _assert_permutations(expanded: pd.DataFrame) -> None:
    grouped = expanded.groupby("logical_id", sort=False)
    assert (grouped.size() == 3).all()
    assert (grouped["permutation_index"].nunique() == 3).all()
    assert (grouped["unknown_position"].nunique() == 3).all()
    assert (grouped["context"].nunique() == 1).all()
    assert (grouped["question"].nunique() == 1).all()
    for record in expanded.to_dict("records"):
        assert record["content_of_{}".format(record["correct_option"])] == record["correct_content"]
        assert record["content_of_{}".format(record["biased_option"])] == record["biased_content"]
        assert record["content_of_{}".format(record["unknown_position"])] == "unknown"
    bilingual_perm = expanded.groupby(["semantic_pair_id", "permutation_index"])
    assert (bilingual_perm["unknown_position"].nunique() == 1).all()
    for content in (
        "content_of_A",
        "content_of_B",
        "content_of_C",
        "correct_option",
        "biased_option",
    ):
        assert (bilingual_perm[content].nunique() == 1).all(), content


def validate_catalog(catalog: Dict[str, Any], scenarios: List[Dict[str, Any]]) -> None:
    categories = catalog["categories"]
    assert len(categories) == 9
    assert [category["name_pt"] for category in categories] == EXPECTED_CATEGORY_NAMES_PT
    assert len(scenarios) == 30
    assert len({scenario["scenario_id"] for scenario in scenarios}) == 30
    for category in categories:
        assert len(category["pairs"]) == 3
        ids = {group["id"] for group in category["groups"]}
        for pair in category["pairs"]:
            assert pair["target"] in ids and pair["comparison"] in ids
            assert pair["stereotype_target"] in ids
            assert "needs_human_validation" in pair
        if category["id"] == "music_preference":
            assert category["aggregation"] == "exploratory_cultural"
    for scenario in scenarios:
        assert set(scenario["texts"]) == set(LANGUAGES)
        for field in (
            "ambiguous_context",
            "disambiguated_context",
            "negative_question",
            "non_negative_question",
            "negative_action",
            "positive_action",
        ):
            assert field in scenario["texts"]["pt"] and field in scenario["texts"]["en"]


def validate_dataset(
    catalog: Dict[str, Any],
    scenarios: List[Dict[str, Any]],
    templates: pd.DataFrame,
    logical: pd.DataFrame,
    expanded: pd.DataFrame,
) -> Dict[str, int]:
    """Validate all required cardinalities and semantic invariants."""
    validate_catalog(catalog, scenarios)
    assert len(templates) == 270
    assert (templates.groupby("category_id").size() == 30).all()
    assert len(logical) == 6480
    assert logical["logical_id"].nunique() == 6480
    assert logical["semantic_pair_id"].nunique() == 3240
    assert (logical.groupby("language").size() == 3240).all()
    assert (logical.groupby(["category_id", "language"]).size() == 360).all()
    assert (logical.groupby(["template_id", "language"]).size() == 12).all()
    assert (logical.groupby(["language", "condition_id"]).size() == 810).all()
    assert (logical.groupby(["category_id", "group_order_inverted"]).size() == 360).all()
    assert (logical.groupby(["category_id", "negative_actor_content"]).size() == 360).all()
    assert (
        not logical[["context", "question", "group1", "group2"]]
        .apply(lambda column: column.str.contains(r"\{[^}]+\}", regex=True).any())
        .any()
    )
    assert len(expanded) == 19440
    assert expanded["example_id"].nunique() == 19440
    assert not expanded.duplicated(["logical_id", "permutation_index"]).any()
    assert (expanded.groupby("correct_option").size() == 6480).all()
    _assert_pairing(logical)
    _assert_permutations(expanded)
    return {
        "categories": 9,
        "scenarios": 30,
        "templates": len(templates),
        "semantic_pairs": logical["semantic_pair_id"].nunique(),
        "logical_examples": len(logical),
        "expanded_evaluations": len(expanded),
    }
