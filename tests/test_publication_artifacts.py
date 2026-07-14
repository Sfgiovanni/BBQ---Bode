import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RUN_ID = "20260710_000126_bilingual_bode_bode-7b-alpaca-pt-br-no-peft"
RUN_DIR = ROOT / "results" / "runs" / RUN_ID


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def test_question_snapshots_match_publication_manifest():
    question_dir = ROOT / "questions"
    manifest = json.loads((question_dir / "manifest.json").read_text(encoding="utf-8"))

    assert manifest["source_run_id"] == RUN_ID
    assert manifest["logical_questions"] == 6480
    assert manifest["evaluated_questions"] == 19440

    for filename, metadata in manifest["files"].items():
        assert _sha256(question_dir / filename) == metadata["sha256"]

    assert len(pd.read_parquet(question_dir / "logical_questions.parquet")) == 6480
    assert len(pd.read_parquet(question_dir / "evaluated_questions.parquet")) == 19440


def test_reference_predictions_are_complete_and_unique():
    manifest = json.loads((RUN_DIR / "manifest.json").read_text(encoding="utf-8"))
    predictions = pd.read_parquet(RUN_DIR / "raw_predictions.parquet")

    assert manifest["status"] == "completed"
    assert manifest["completed_evaluations"] == 19440
    assert len(predictions) == 19440
    assert predictions["example_id"].is_unique
    assert set(predictions["language"]) == {"pt", "en"}


def test_relative_markdown_links_resolve():
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    missing = []

    markdown_files = [
        ROOT / "README.md",
        ROOT / "questions" / "README.md",
        ROOT / "results" / "README.md",
    ]
    markdown_files.extend(sorted((ROOT / "docs").glob("*.md")))

    for markdown in markdown_files:
        text = markdown.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = markdown.parent / unquote(target)
            if not resolved.exists():
                missing.append("{} -> {}".format(markdown.relative_to(ROOT), target))

    assert not missing, "Broken relative Markdown links:\n{}".format("\n".join(missing))
