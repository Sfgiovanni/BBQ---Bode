"""Strict structural and balance validation for the bilingual dataset."""

from typing import Any, Dict, List

import pandas as pd

from brbbq.dataset.builder import CONDITIONS, LANGUAGES, PERMUTATIONS


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


def category_pair_counts(catalog: Dict[str, Any]) -> Dict[str, int]:
    """Number of pairs declared per category, as authored in the YAML.

    This is the source of truth for dataset cardinality. Categories are not
    required to have the same pair count as each other (see the extended
    catalog, which adds pairs unevenly per category).
    """
    return {category["id"]: len(category["pairs"]) for category in catalog["categories"]}


def category_balance(logical: pd.DataFrame) -> pd.DataFrame:
    """Report, per category, how the group-order/negative-actor schedules split.

    Informational only -- not asserted against a fixed ratio. With a uniform
    pair count per category (the reference catalog) both schedules split
    exactly 50/50; with heterogeneous pair counts (the extended catalog) some
    categories can be imbalanced. Callers decide whether that imbalance needs
    weighting in aggregation.
    """
    return (
        logical.groupby("category_id")
        .agg(
            n_rows=("logical_id", "size"),
            group_order_inverted_share=("group_order_inverted", "mean"),
            negative_actor_group1_share=(
                "negative_actor_content",
                lambda column: (column == "group1").mean(),
            ),
        )
        .reset_index()
    )


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
        assert len(category["pairs"]) >= 1, category["id"]
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
    """Validate all required cardinalities and semantic invariants.

    Cardinalities are derived from the catalog's own pair counts per
    category, not hardcoded -- categories may have different pair counts
    (see the extended catalog). With the reference catalog (3 pairs in every
    category) this reduces to the original fixed numbers (270/6480/19440).
    """
    validate_catalog(catalog, scenarios)
    n_categories = len(catalog["categories"])
    n_scenarios = len(scenarios)
    n_conditions = len(CONDITIONS)
    n_languages = len(LANGUAGES)
    n_permutations = len(PERMUTATIONS)
    pair_counts = category_pair_counts(catalog)
    total_pairs = sum(pair_counts.values())

    expected_templates = n_categories * n_scenarios
    assert len(templates) == expected_templates
    assert (templates.groupby("category_id").size() == n_scenarios).all()

    expected_semantic_pairs = total_pairs * n_scenarios * n_conditions
    expected_logical_total = expected_semantic_pairs * n_languages
    assert len(logical) == expected_logical_total
    assert logical["logical_id"].nunique() == expected_logical_total
    assert logical["semantic_pair_id"].nunique() == expected_semantic_pairs
    assert (logical.groupby("language").size() == expected_semantic_pairs).all()

    category_language_counts = logical.groupby(["category_id", "language"]).size()
    for category_id, pairs_in_category in pair_counts.items():
        expected = pairs_in_category * n_scenarios * n_conditions
        for language in LANGUAGES:
            assert category_language_counts[(category_id, language)] == expected, (
                category_id,
                language,
            )

    template_language_counts = logical.groupby(["template_id", "category_id", "language"]).size()
    for (template_id, category_id, _language), count in template_language_counts.items():
        assert count == pair_counts[category_id] * n_conditions, template_id

    expected_per_condition = expected_semantic_pairs // n_conditions
    assert (logical.groupby(["language", "condition_id"]).size() == expected_per_condition).all()

    assert (
        not logical[["context", "question", "group1", "group2"]]
        .apply(lambda column: column.str.contains(r"\{[^}]+\}", regex=True).any())
        .any()
    )
    expected_expanded_total = expected_logical_total * n_permutations
    assert len(expanded) == expected_expanded_total
    assert expanded["example_id"].nunique() == expected_expanded_total
    assert not expanded.duplicated(["logical_id", "permutation_index"]).any()
    assert (expanded.groupby("correct_option").size() == expected_logical_total).all()
    _assert_pairing(logical)
    _assert_permutations(expanded)
    return {
        "categories": n_categories,
        "scenarios": n_scenarios,
        "templates": len(templates),
        "semantic_pairs": logical["semantic_pair_id"].nunique(),
        "logical_examples": len(logical),
        "expanded_evaluations": len(expanded),
    }
