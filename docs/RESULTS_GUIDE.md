# Results guide

Each `results/runs/<run_id>/` directory contains immutable input snapshots,
raw predictions, runtime state, aggregate metrics, figures, and reports. Use
`manifest.json` to determine whether a run is initialized, running,
interrupted, failed, scored, or completed.

`raw_predictions.parquet` is the authoritative row-level output and is included
for the reference run. A duplicate CSV is written locally during inference but
is not published. `dataset_manifest.json` records expected cardinalities.
`metrics/option_token_audit.json` records A/B/C token IDs and neutral language
baselines. `runtime.json` and `token_usage.json` capture speed and token counts.

`REPORT.md` covers the complete benchmark. `REPORT_BRAZIL_SPECIFIC.md` isolates
Regionality and Religion without conflating social and positional effects.
`EXECUTIVE_SUMMARY.md` is a concise entry point, not a substitute for detailed
tables or validation notes.

To reproduce the reference reports from preserved predictions without changing
the published artifact:

```bash
scripts/reproduce_reports.sh
```
