from brbbq.dataset.validation import validate_dataset


def test_exact_experiment_counts(dataset_bundle):
    catalog, scenarios, templates, logical, expanded = dataset_bundle
    result = validate_dataset(catalog, scenarios, templates, logical, expanded)
    assert result == {
        "categories": 9,
        "scenarios": 30,
        "templates": 270,
        "semantic_pairs": 3240,
        "logical_examples": 6480,
        "expanded_evaluations": 19440,
    }


def test_exact_counts_by_language_template_and_condition(dataset_bundle):
    _, _, templates, logical, expanded = dataset_bundle
    assert templates.groupby("category_id").size().eq(30).all()
    assert logical.groupby("language").size().to_dict() == {"en": 3240, "pt": 3240}
    assert logical.groupby(["template_id", "language"]).size().eq(12).all()
    assert logical.groupby(["language", "condition_id"]).size().eq(810).all()
    assert expanded.groupby("logical_id").size().eq(3).all()


def test_music_is_exploratory(dataset_bundle):
    catalog, _, _, _, _ = dataset_bundle
    music = next(item for item in catalog["categories"] if item["id"] == "music_preference")
    assert music["aggregation"] == "exploratory_cultural"
    assert music["protected_demographic"] is False
