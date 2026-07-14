import re


def test_every_semantic_pair_has_pt_and_en(dataset_bundle):
    _, _, _, logical, _ = dataset_bundle
    grouped = logical.groupby("semantic_pair_id")
    assert grouped.size().eq(2).all()
    assert grouped["language"].apply(set).eq({"pt", "en"}).all()


def test_bilingual_structure_is_equal(dataset_bundle):
    _, _, _, logical, _ = dataset_bundle
    shared = [
        "category_id",
        "scenario_id",
        "pair_id",
        "group1_id",
        "group2_id",
        "bias_target_id",
        "condition_id",
        "correct_content",
        "biased_content",
        "semantic_correct_answer",
        "semantic_biased_answer",
        "negative_actor_content",
    ]
    grouped = logical.groupby("semantic_pair_id")
    for column in shared:
        assert grouped[column].nunique(dropna=False).eq(1).all(), column


def test_placeholders_are_filled(dataset_bundle):
    _, _, _, logical, _ = dataset_bundle
    pattern = re.compile(r"\{[^}]+\}")
    for column in ("context", "question", "group1", "group2"):
        assert not logical[column].str.contains(pattern).any()


def test_no_accidental_duplicates(dataset_bundle):
    _, _, _, logical, expanded = dataset_bundle
    assert logical["logical_id"].is_unique
    assert expanded["example_id"].is_unique
    assert not logical.duplicated(["semantic_pair_id", "language"]).any()
    assert not expanded.duplicated(["logical_id", "permutation_index"]).any()


def test_group_and_negative_actor_balance(dataset_bundle):
    _, _, _, logical, _ = dataset_bundle
    assert logical.groupby(["category_id", "group_order_inverted"]).size().eq(360).all()
    assert logical.groupby(["category_id", "negative_actor_content"]).size().eq(360).all()
