"""Metrics persistence, reports, and figures."""

import json
from pathlib import Path
from typing import Dict

import pandas as pd

from brbbq.metrics import metrics_table, paired_analysis
from brbbq.reporting.figures import generate_figures
from brbbq.utils.io import atomic_csv, atomic_json


GROUPINGS = {
    "overall": [],
    "by_category": ["category_id"],
    "by_group": ["category_id", "bias_target_id"],
    "by_scenario": ["scenario_id"],
    "by_language": ["language"],
    "by_context": ["context_type"],
    "by_question_type": ["question_type"],
    "by_unknown_position": ["unknown_position"],
    "by_model": ["model_name"],
    "by_language_context": ["language", "context_type"],
    "by_category_language": ["category_id", "language"],
    "by_unknown_position_language": ["unknown_position", "language"],
}


def _f(value) -> str:
    return "NA" if pd.isna(value) else "{:.4f}".format(float(value))


def _markdown_table(frame: pd.DataFrame) -> str:
    return frame.to_markdown(index=False, floatfmt=".4f")


def _main_report(tables: Dict[str, pd.DataFrame], paired: pd.DataFrame) -> str:
    overall = tables["overall"].iloc[0]
    return """# Bilingual Brazilian BBQ computational report

> This is a computational benchmark run, not publication-ready social evidence.
> Bilingual templates and stereotype directions require expert human validation.

## Scope

- 9 categories; music preference is exploratory cultural content and is excluded from protected-demographic interpretations.
- Paired Brazilian Portuguese and English prompts with three option rotations.
- Social bias metrics and positional metrics are reported separately.

## Overall metrics

| Metric | Value |
|---|---:|
| Accuracy | {accuracy} |
| Ambiguous accuracy | {accuracy_ambiguous} |
| Disambiguated accuracy | {accuracy_disambiguated} |
| Unknown rate | {unknown_rate} |
| s_DIS | {s_dis} |
| s_AMB | {s_amb} |
| Position consistency | {consistency} |
| Flip rate | {flip} |

## Paired PT versus EN

{paired_table}

## Category metrics

{category_table}

The confidence intervals in `metrics/paired_bootstrap.json` use semantic blocks
that keep both languages, all four logical conditions, and all three option
permutations together during resampling.
""".format(
        accuracy=_f(overall["accuracy"]),
        accuracy_ambiguous=_f(overall["accuracy_ambiguous"]),
        accuracy_disambiguated=_f(overall["accuracy_disambiguated"]),
        unknown_rate=_f(overall["unknown_rate"]),
        s_dis=_f(overall["s_DIS"]),
        s_amb=_f(overall["s_AMB"]),
        consistency=_f(overall["position_consistency"]),
        flip=_f(overall["flip_rate"]),
        paired_table=_markdown_table(paired),
        category_table=_markdown_table(tables["by_category_language"]),
    )


def _brazil_report(
    predictions: pd.DataFrame, tables: Dict[str, pd.DataFrame], paired_category: pd.DataFrame
) -> str:
    relevant = tables["by_category_language"][
        tables["by_category_language"]["category_id"].isin(["regionality", "religion"])
    ]
    ambiguous = predictions[
        (predictions["category_id"].isin(["regionality", "religion"]))
        & (predictions["context_type"] == "ambiguous")
    ]
    selections = (
        ambiguous.groupby(["category_id", "language", "semantic_biased_answer"])
        .size()
        .reset_index(name="selected_or_present_count")
    )
    validation_count = int(
        predictions[predictions["category_id"].isin(["regionality", "religion"])][
            "needs_human_validation"
        ].sum()
    )
    return """# Brazil-specific analysis: Regionality and Religion

> Do not interpret these results as validated claims about Brazilian groups.
> Items marked for human review remain exploratory.

This section separates social-content direction (`s_DIS`, `s_AMB`) from option
position behavior (`position_consistency`, `flip_rate`, and A/B/C rates).

## PT versus EN metrics

{metrics}

## Paired differences

{paired}

## Ambiguous group coverage

{selections}

The religion category explicitly includes Umbanda, Candomblé, and people with
no religion. The regionality category includes groups from all five Brazilian
macro-regions. Rows flagged for human validation in these categories: {validation_count}.
""".format(
        metrics=_markdown_table(relevant),
        paired=_markdown_table(
            paired_category[paired_category["category_id"].isin(["regionality", "religion"])]
        ),
        selections=_markdown_table(selections),
        validation_count=validation_count,
    )


def generate_reports(
    run_dir: Path, config: Dict, with_bootstrap: bool = True
) -> Dict[str, pd.DataFrame]:
    predictions = pd.read_parquet(run_dir / "raw_predictions.parquet")
    metrics_dir = run_dir / "metrics"
    metrics_dir.mkdir(exist_ok=True)
    tables = {}
    for name, grouping in GROUPINGS.items():
        table = metrics_table(predictions, grouping)
        tables[name] = table
        atomic_csv(table, metrics_dir / "{}.csv".format(name))
    aggregation_frame = predictions.copy()
    aggregation_frame["aggregation"] = aggregation_frame.apply(
        lambda row: "brazil_specific" if row["brazil_specific"] else row["aggregation"], axis=1
    )
    tables["by_aggregation_language"] = metrics_table(
        aggregation_frame, ["aggregation", "language"]
    )
    atomic_csv(tables["by_aggregation_language"], metrics_dir / "by_aggregation_language.csv")
    paired, paired_category, transition, bootstrap = paired_analysis(
        predictions,
        bootstrap_samples=int(config["metrics"].get("bootstrap_samples", 1000)),
        seed=int(config["experiment"].get("seed", 42)),
        confidence=float(config["metrics"].get("confidence_level", 0.95)),
        with_bootstrap=with_bootstrap,
    )
    tables["paired_by_category"] = paired_category
    tables["transition"] = transition
    atomic_csv(paired, metrics_dir / "paired_overall.csv")
    atomic_csv(paired_category, metrics_dir / "paired_by_category.csv")
    atomic_csv(transition, metrics_dir / "pt_en_transition.csv")
    atomic_json(bootstrap, metrics_dir / "paired_bootstrap.json")
    generate_figures(predictions, tables, run_dir / "figures")
    (run_dir / "REPORT.md").write_text(_main_report(tables, paired), encoding="utf-8")
    (run_dir / "REPORT_BRAZIL_SPECIFIC.md").write_text(
        _brazil_report(predictions, tables, paired_category), encoding="utf-8"
    )
    summary = """# Executive summary

Computational BODE run over the complete bilingual design. Review `REPORT.md`,
`REPORT_BRAZIL_SPECIFIC.md`, and `metrics/paired_bootstrap.json` for results.
The dataset contains unvalidated stereotype directions and is not ready for
publication claims until bilingual expert review is complete.
"""
    (run_dir / "EXECUTIVE_SUMMARY.md").write_text(summary, encoding="utf-8")
    manifest_path = run_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update({"status": "completed", "reports_generated": True})
    atomic_json(manifest, manifest_path)
    return tables
