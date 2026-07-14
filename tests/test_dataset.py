from pathlib import Path

from brbbq.dataset import build_dataset, load_catalogs, validate_dataset


ROOT = Path(__file__).resolve().parents[1]


def test_full_bilingual_cardinality_and_balance():
    categories_path = ROOT / "questions/categories_bilingual.yaml"
    scenarios_path = ROOT / "questions/scenarios_bilingual.jsonl"
    catalog, scenarios = load_catalogs(categories_path, scenarios_path)
    templates, logical, expanded = build_dataset(categories_path, scenarios_path)
    counts = validate_dataset(catalog, scenarios, templates, logical, expanded)
    assert counts == {
        "categories": 9,
        "scenarios": 30,
        "templates": 270,
        "semantic_pairs": 3240,
        "logical_examples": 6480,
        "expanded_evaluations": 19440,
    }


def test_structural_pair_and_position_invariants():
    categories_path = ROOT / "questions/categories_bilingual.yaml"
    scenarios_path = ROOT / "questions/scenarios_bilingual.jsonl"
    _, logical, expanded = build_dataset(categories_path, scenarios_path)
    for _, group in expanded.groupby("logical_id"):
        assert set(group["unknown_position"]) == {"A", "B", "C"}
        assert group["correct_option"].nunique() == 3
        assert group["biased_option"].nunique() == 3
        assert group["context"].nunique() == 1
        assert group["question"].nunique() == 1
    for _, group in logical.groupby("semantic_pair_id"):
        assert set(group["language"]) == {"pt", "en"}
        assert group["semantic_correct_answer"].nunique() == 1
        assert group["semantic_biased_answer"].nunique() == 1
