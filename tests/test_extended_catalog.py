"""Proves the extended catalog (questions/categories_bilingual_extended.yaml) is a
true content superset of the published reference run, not a renumbering.

Reference run: 20260710_000126_bilingual_bode_bode-7b-alpaca-pt-br-no-peft.
questions/manifest.json and the reference parquet files are read-only fixtures
here -- never written to.
"""

import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest

from brbbq.dataset import build_dataset, category_balance, category_pair_counts, validate_dataset
from brbbq.dataset.builder import load_catalogs


ROOT = Path(__file__).resolve().parents[1]
OLD_CATALOG = ROOT / "questions/categories_bilingual.yaml"
EXTENDED_CATALOG = ROOT / "questions/categories_bilingual_extended.yaml"
SCENARIOS = ROOT / "questions/scenarios_bilingual.jsonl"
MANIFEST = ROOT / "questions/manifest.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def reference_logical():
    return pd.read_parquet(ROOT / "questions/logical_questions.parquet")


@pytest.fixture(scope="module")
def reference_expanded():
    return pd.read_parquet(ROOT / "questions/evaluated_questions.parquet")


def test_reference_files_match_manifest(manifest, reference_logical, reference_expanded):
    """The on-disk reference artifacts are exactly what manifest.json records."""
    files = manifest["files"]
    assert _sha256(OLD_CATALOG) == files["categories_bilingual.yaml"]["sha256"]
    assert _sha256(SCENARIOS) == files["scenarios_bilingual.jsonl"]["sha256"]
    assert _sha256(ROOT / "questions/logical_questions.parquet") == (
        files["logical_questions.parquet"]["sha256"]
    )
    assert _sha256(ROOT / "questions/evaluated_questions.parquet") == (
        files["evaluated_questions.parquet"]["sha256"]
    )


def test_old_catalog_reproduces_reference_exactly(reference_logical, reference_expanded):
    """Rebuilding from the untouched old catalog with current code must match
    the published reference content bit-for-bit -- proof that the
    REFERENCE_PAIRS_PER_CATEGORY stride freeze did not change old behavior.
    """
    _, logical, expanded = build_dataset(OLD_CATALOG, SCENARIOS)

    assert set(logical["logical_id"]) == set(reference_logical["logical_id"])
    assert set(expanded["example_id"]) == set(reference_expanded["example_id"])

    left = logical.set_index("logical_id").sort_index()
    right = reference_logical.set_index("logical_id").sort_index()
    shared_columns = [c for c in left.columns if c in right.columns]
    for column in shared_columns:
        assert (left[column].astype(str) == right[column].astype(str)).all(), column

    left_e = expanded.set_index("example_id").sort_index()
    right_e = reference_expanded.set_index("example_id").sort_index()
    shared_columns_e = [c for c in left_e.columns if c in right_e.columns]
    for column in shared_columns_e:
        assert (left_e[column].astype(str) == right_e[column].astype(str)).all(), column


def test_extended_catalog_is_a_true_content_superset(reference_logical, reference_expanded):
    """The 19,440 example_ids from the reference run must appear, unchanged in
    content, inside the extended (51-pair) build. This is the property that
    makes the extended run comparable to the reference run: appending pairs
    must not perturb the original pairs' group order, negative/positive actor
    assignment, or correct answer.
    """
    _, logical, expanded = build_dataset(EXTENDED_CATALOG, SCENARIOS)

    assert set(reference_logical["logical_id"]) <= set(logical["logical_id"])
    assert set(reference_expanded["example_id"]) <= set(expanded["example_id"])

    shared_ids = set(reference_logical["logical_id"])
    left = logical[logical["logical_id"].isin(shared_ids)].set_index("logical_id").sort_index()
    right = reference_logical.set_index("logical_id").sort_index()
    shared_columns = [c for c in left.columns if c in right.columns]
    mismatches = {
        column: int((left[column].astype(str) != right[column].astype(str)).sum())
        for column in shared_columns
    }
    mismatches = {k: v for k, v in mismatches.items() if v}
    assert not mismatches, mismatches

    shared_example_ids = set(reference_expanded["example_id"])
    left_e = (
        expanded[expanded["example_id"].isin(shared_example_ids)]
        .set_index("example_id")
        .sort_index()
    )
    right_e = reference_expanded.set_index("example_id").sort_index()
    shared_columns_e = [c for c in left_e.columns if c in right_e.columns]
    mismatches_e = {
        column: int((left_e[column].astype(str) != right_e[column].astype(str)).sum())
        for column in shared_columns_e
    }
    mismatches_e = {k: v for k, v in mismatches_e.items() if v}
    assert not mismatches_e, mismatches_e


def test_extended_catalog_has_heterogeneous_pair_counts():
    catalog, _ = load_catalogs(EXTENDED_CATALOG, SCENARIOS)
    counts = category_pair_counts(catalog)
    assert counts == {
        "regionality": 6,
        "religion": 6,
        "race_color": 6,
        "socioeconomic_class": 6,
        "gender": 5,
        "education": 5,
        "interior_capital": 6,
        "political_orientation": 5,
        "music_preference": 6,
    }
    assert sum(counts.values()) == 51
    assert len(set(counts.values())) > 1, "catalog should be non-uniform for this test to be meaningful"


def test_extended_catalog_validates_with_derived_counts():
    catalog, scenarios = load_catalogs(EXTENDED_CATALOG, SCENARIOS)
    templates, logical, expanded = build_dataset(EXTENDED_CATALOG, SCENARIOS)
    result = validate_dataset(catalog, scenarios, templates, logical, expanded)
    assert result == {
        "categories": 9,
        "scenarios": 30,
        "templates": 270,
        "semantic_pairs": 51 * 30 * 4,
        "logical_examples": 51 * 30 * 4 * 2,
        "expanded_evaluations": 51 * 30 * 4 * 2 * 3,
    }
    assert result["semantic_pairs"] == 6120
    assert result["logical_examples"] == 12240
    assert result["expanded_evaluations"] == 36720


def test_group_order_stays_balanced_regardless_of_pair_count():
    """group_order_inverted is exactly 50/50 per category in both catalogs.
    30 scenarios is even, which symmetrizes this schedule for any pair count.
    """
    for catalog_path in (OLD_CATALOG, EXTENDED_CATALOG):
        _, logical, _ = build_dataset(catalog_path, SCENARIOS)
        balance = category_balance(logical)
        deviation = (balance["group_order_inverted_share"] - 0.5).abs()
        assert (deviation < 1e-9).all(), (catalog_path, balance)


def test_negative_actor_schedule_skews_under_extension():
    """The old catalog (uniform 3 pairs/category) is exactly balanced on
    negative_actor_content. The extended catalog is not: every category
    (5-pair and 6-pair alike) picks up a small skew (~1-1.3 pp) because
    target_is_negative has period 4 and 30 * pairs_in_category is not always
    a multiple of 4. This is real, small, and present across all extended
    categories -- not isolated to the uneven (5-pair) ones -- so it must be
    surfaced (see docs/EXTENDED_PAIRS_AUDIT.md Step 5 note) rather than
    assumed away. It is informational: validate_dataset does not fail on it.
    """
    _, old_logical, _ = build_dataset(OLD_CATALOG, SCENARIOS)
    old_balance = category_balance(old_logical)
    old_deviation = (old_balance["negative_actor_group1_share"] - 0.5).abs()
    assert (old_deviation < 1e-9).all()

    _, ext_logical, _ = build_dataset(EXTENDED_CATALOG, SCENARIOS)
    ext_balance = category_balance(ext_logical).set_index("category_id")
    skew = (ext_balance["negative_actor_group1_share"] - 0.5).abs()
    assert (skew > 0).all(), "expected every extended category to show some skew"
    assert (skew < 0.02).all(), "skew larger than expected, investigate before trusting metrics"


def test_global_aggregation_weights_categories_by_row_count_not_equally():
    """brbbq.metrics.paired.paired_analysis computes its "overall" row by
    pooling every evaluated row across all categories (metrics/paired.py,
    `_difference(frame)` where `frame` is the whole dataset) -- it is not an
    average of the 9 per-category values. With a uniform pair count per
    category (reference catalog) that pooling happens to give every category
    an equal 1/9 share. With the extended catalog's heterogeneous pair counts
    (5 or 6 per category) it does not: 6-pair categories get more weight than
    5-pair categories in any global metric computed this way.

    This is the "sub/over-represented in the global aggregation" check asked
    for in Step 5 -- pinned down numerically so it can't silently drift, and
    surfaced in docs/EXTENDED_PAIRS_AUDIT.md as an open question for Step 7
    (whether to keep this row-weighted "micro" global metric as-is, or also
    report a category-averaged "macro" variant that weights every category
    equally regardless of pair count).
    """
    _, _, ref_expanded = build_dataset(OLD_CATALOG, SCENARIOS)
    ref_share = ref_expanded.groupby("category_id").size() / len(ref_expanded)
    assert ((ref_share - 1 / 9).abs() < 1e-9).all(), ref_share.to_dict()

    _, _, ext_expanded = build_dataset(EXTENDED_CATALOG, SCENARIOS)
    ext_share = ext_expanded.groupby("category_id").size() / len(ext_expanded)

    six_pair_categories = {
        "regionality",
        "religion",
        "race_color",
        "socioeconomic_class",
        "interior_capital",
        "music_preference",
    }
    five_pair_categories = {"gender", "education", "political_orientation"}

    for category_id in six_pair_categories:
        assert abs(ext_share[category_id] - 6 / 51) < 1e-9, (category_id, ext_share[category_id])
    for category_id in five_pair_categories:
        assert abs(ext_share[category_id] - 5 / 51) < 1e-9, (category_id, ext_share[category_id])

    # Confirm every category deviates from the reference's flat 1/9 share --
    # i.e. no category keeps the reference's implicit equal weighting.
    assert ((ext_share - 1 / 9).abs() > 1e-9).all()
