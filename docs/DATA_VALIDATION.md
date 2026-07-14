# Data validation

Run:

```bash
python -m brbbq.cli validate --config configs/experiments/bilingual_bode_8h.yaml
pytest -q
```

Validation enforces nine exact categories, 30 scenarios/templates per category,
12 logical questions per template and language, 3,240 logical questions per
language, 6,480 bilingual logical rows, and 19,440 expanded evaluations.

It also checks paired language coverage, canonical entity and condition
identity, filled placeholders, unique IDs, three rotations, unknown in every
position, recalculated correct and biased letters, unchanged prompt content
between rotations, equal category/language/condition representation, and
balanced group order and negative actor placement.

Structural validation is not social validation. The current catalog marks
unconfirmed pairs with `needs_human_validation: true`. Researchers must record
bilingual expert decisions before publication use; see the review protocol in
[`questions/README.md`](../questions/README.md).
