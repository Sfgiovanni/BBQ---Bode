import bbq_v2_lib
import brbbq_data


def test_legacy_synthetic_builder_still_runs():
    templates = bbq_v2_lib.build_base_templates()
    assert len(templates) == 60
    assert set(templates["category"]) == {"Regionalidade", "Religião"}


def test_legacy_curated_builder_still_runs():
    templates, logical, expanded = brbbq_data.build_all()
    assert (len(templates), len(logical), len(expanded)) == (12, 72, 216)
