# Questions and benchmark inputs

This directory contains both the editable source catalog and immutable snapshots
of the questions evaluated in the reference BODE run. No translation or question
generation occurs during inference.

## Files

| File | Purpose |
|---|---|
| `categories_bilingual.yaml` | Nine categories, localized group labels, comparison pairs, stereotype-direction metadata, and validation flags. |
| `scenarios_bilingual.jsonl` | Thirty paired Portuguese/English contexts and questions. One scenario record per line. |
| `logical_questions.parquet` | The 6,480 bilingual logical questions before answer-option rotation. |
| `evaluated_questions.parquet` | The exact 19,440 inputs evaluated in the reference run, including all three A/B/C rotations. |
| `sample_questions.csv` | A small, GitHub-previewable sample covering every category, language, and context type. |
| `manifest.json` | Row counts, seed, source run, and SHA-256 checksums. |

The Parquet snapshots contain question inputs and experimental metadata only;
model scores and selections are published under [`results/`](../results/).

## Construction

The design crosses:

- 9 categories;
- 30 scenarios per category;
- 3 group pairs per scenario;
- 4 conditions per pair (ambiguous/disambiguated × negative/non-negative);
- 2 stored languages (Brazilian Portuguese and English);
- 3 deterministic answer-option rotations.

This produces 3,240 logical questions per language, 6,480 logical questions in
total, and 19,440 evaluated inputs. Stable identifiers link every Portuguese
item to its English counterpart and every rotated input to its logical question.

## Important validation status

`needs_human_validation: true` means that wording, semantic equivalence, or the
configured stereotype direction has not yet received the required bilingual
expert review. Structural tests confirm cardinality, pairing, identifiers,
rotations, and answer consistency; they do **not** establish that a stereotype
direction is socially valid or suitable for a publication claim.

Reviewers should assess paired PT/EN items without seeing model predictions and
record:

1. semantic equivalence;
2. linguistic naturalness and person-centered phrasing;
3. cultural and regional appropriateness;
4. correctness of question polarity and disambiguating evidence;
5. acceptability and evidence for any stereotype direction.

Rejected items should be revised in both languages, assigned a new catalog
version, and evaluated in a new run.

## Rebuild and validate

From the repository root:

```bash
python -m brbbq.cli validate \
  --config configs/experiments/bilingual_bode_8h.yaml

python -m brbbq.cli build-dataset \
  --config configs/experiments/bilingual_bode_8h.yaml \
  --output reproduced/dataset
```

The generated identifiers and row counts should match `manifest.json`. Parquet
file bytes are not used as the scientific equality criterion because writer
metadata can vary across PyArrow versions.
