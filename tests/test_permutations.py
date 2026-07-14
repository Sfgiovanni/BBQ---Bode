def test_unknown_appears_once_in_each_position(dataset_bundle):
    _, _, _, _, expanded = dataset_bundle
    grouped = expanded.groupby("logical_id")
    assert grouped["unknown_position"].apply(set).eq({"A", "B", "C"}).all()


def test_correct_and_biased_options_are_recalculated(dataset_bundle):
    _, _, _, _, expanded = dataset_bundle
    for row in expanded.to_dict("records"):
        assert row["content_of_{}".format(row["correct_option"])] == row["correct_content"]
        assert row["content_of_{}".format(row["biased_option"])] == row["biased_content"]


def test_rotations_preserve_prompt_content(dataset_bundle):
    _, _, _, _, expanded = dataset_bundle
    grouped = expanded.groupby("logical_id")
    assert grouped["context"].nunique().eq(1).all()
    assert grouped["question"].nunique().eq(1).all()
    assert grouped["group1"].nunique().eq(1).all()
    assert grouped["group2"].nunique().eq(1).all()
    assert grouped["correct_option"].apply(set).eq({"A", "B", "C"}).all()


def test_pt_en_use_same_rotation(dataset_bundle):
    _, _, _, _, expanded = dataset_bundle
    grouped = expanded.groupby(["semantic_pair_id", "permutation_index"])
    for column in (
        "content_of_A",
        "content_of_B",
        "content_of_C",
        "correct_option",
        "biased_option",
    ):
        assert grouped[column].nunique().eq(1).all()
