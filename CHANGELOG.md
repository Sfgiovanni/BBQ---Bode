# Changelog

## Unreleased

### Added

- Extended bilingual catalog (`questions/categories_bilingual_extended.yaml`,
  51 pairs across the same 9 categories/6 groups, up from 27) contributed by a
  paper collaborator, pending expert review (`needs_human_validation: true`,
  `source: null` on every added pair, unchanged from the reference catalog).
- `configs/experiments/bilingual_bode_extended.yaml`, deriving expected
  counts (6,120 logical/language, 12,240 logical total, 36,720 expanded)
  directly from the extended catalog, pinned to `batch_size: 4` to match the
  reference run. `configs/models/bode.yaml` now pins the exact model/
  tokenizer revision (`ff1ecd8eccbd7bcd04fa247d140cf783f8cd73ec`, unchanged
  since 2024-10-25, confirmed same weights as the reference run's unpinned
  `revision: null`), closing a known provenance gap.
- Extended run executed: `results/runs/20260726_112145_bilingual_bode_extended_bode-7b-alpaca-pt-br-no-peft/`
  (36,720 evaluations, 5h29m on the same RTX 3080 Ti). The 19,440 evaluations
  shared with the reference run are bit-identical in every scored decision
  (selected answer, correctness, bias flag) — see
  `REPORT_EXTENDED_VS_REFERENCE.md` in that run directory for the full
  comparison, including the political_orientation direction-cancellation and
  race_color reference-group-mixing effects predicted in
  `docs/EXTENDED_PAIRS_AUDIT.md`. Four aggregation questions from the audit
  remain open pending collaborator/author review before these numbers can be
  used in the paper.
- `brbbq.dataset.validation.category_pair_counts` / `category_balance`
  helpers, and generalized `validate_catalog`/`validate_dataset` to derive
  expected cardinalities from the catalog's own per-category pair counts
  instead of hardcoded literals, so catalogs no longer need a uniform pair
  count per category.
- Regression tests (`tests/test_extended_catalog.py`) proving the extended
  catalog is a true content superset of the published reference run
  (20260710_000126): all 6,480 original `logical_id`s and 19,440 original
  `example_id`s reappear with byte-identical content, not just matching IDs.
  Also pins down category-level schedule balance and the cross-category row
  share each category gets in a pooled global metric (6-pair categories
  11.76%, 5-pair categories 9.80%, versus the reference's uniform 11.11%) —
  see `docs/EXTENDED_PAIRS_AUDIT.md` question 4.

### Fixed

- `src/brbbq/dataset/builder.py`: the group-order-inversion and
  negative/positive-actor schedules were keyed off the *live*
  `len(category["pairs"])`, so appending pairs to a category silently
  changed the group order, actor assignment, and correct answer for
  previously-existing rows even though their content-hashed IDs stayed the
  same. Froze the stride to `REFERENCE_PAIRS_PER_CATEGORY = 3` (the
  reference catalog's uniform pair count), which keeps the reference
  catalog's output byte-identical and makes appending pairs a genuine
  superset. Only valid because new pairs are appended, never inserted or
  reordered, within each category — verified against the extended catalog.

## 0.2.0 - 2026-07-14

### Added

- Deterministic bilingual catalog covering nine requested categories and 30 legacy-based scenarios.
- Paired semantic, logical, and permutation-level identifiers.
- Configuration-driven model adapters for Hugging Face causal LMs and BODE Alpaca.
- Atomic checkpoints, exclusive locks, OOM batch reduction, and resume by example ID.
- Paired PT/EN metrics, clustered bootstrap, Brazil-specific reporting, and ten figures.
- CLI commands, persistent launcher, monitor, documentation, and automated tests.
- Publication-oriented `questions/` and `results/` artifacts with row-level
  Parquet inputs and predictions.
- Isolated report-reproduction and conflict-safe GitHub publication scripts.
- Citation metadata and a paper-oriented repository README.

### Compatibility

- Legacy synthetic and curated Portuguese drivers and tracked results are preserved.
