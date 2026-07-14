# Results

This directory separates the reference bilingual experiment from historical
Portuguese-only outputs.

## Reference bilingual run

The paper-oriented artifact is:

```text
results/runs/20260710_000126_bilingual_bode_bode-7b-alpaca-pt-br-no-peft/
```

It contains the complete 19,440-row prediction table in compact Parquet format,
aggregate metrics, paired bootstrap intervals, publication figures, resolved
configuration, manifests, runtime metadata, and reports.

| Entry | Description |
|---|---|
| `raw_predictions.parquet` | Authoritative row-level model outputs used to calculate every reported metric. |
| `config_resolved.yaml` | Configuration resolved when the run directory was initialized. |
| `manifest.json` | Completion state, timestamps, duration, batch size, and evaluation counts. |
| `dataset_manifest.json` | Dataset cardinalities and evaluated categories. |
| `metrics/` | Overall, stratified, paired PT/EN, bootstrap, and token-audit outputs. |
| `figures/` | Ten paper-oriented PNG figures. |
| `REPORT.md` | Complete computational report. |
| `REPORT_BRAZIL_SPECIFIC.md` | Separate analysis of Regionality and Religion. |
| `EXECUTIVE_SUMMARY.md` | Short entry point and interpretation warning. |

Large duplicate CSV predictions, transient checkpoints, logs, and PID/lock
files remain excluded from version control. The Parquet predictions are enough
to reproduce all aggregate metrics, reports, and figures with the published
code.

Run the isolated report reproduction workflow from the repository root:

```bash
scripts/reproduce_reports.sh
```

Generated artifacts are written to `reproduced/reference_report/` so the
published run remains unchanged.

## Historical Portuguese run

`legacy_portuguese/` preserves the canonical lightweight output of the earlier
Portuguese-only pipeline. It is retained for historical comparison and is not
the reference result of the bilingual experiment.

## Interpretation warning

Computational completion is not equivalent to social validation. Current
question metadata include unvalidated stereotype directions and translations.
Do not use these outputs as claims about Brazilian social groups until the
bilingual expert-review protocol in [`questions/README.md`](../questions/README.md)
has been completed.
