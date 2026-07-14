from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
for location in (ROOT, ROOT / "src"):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

from brbbq.dataset import build_dataset, load_catalogs  # noqa: E402


@pytest.fixture(scope="session")
def dataset_bundle():
    categories = Path("questions/categories_bilingual.yaml")
    scenarios = Path("questions/scenarios_bilingual.jsonl")
    catalog, scenario_rows = load_catalogs(categories, scenarios)
    templates, logical, expanded = build_dataset(categories, scenarios)
    return catalog, scenario_rows, templates, logical, expanded
