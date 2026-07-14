# Bilingual design

## Stored equivalence

`questions/scenarios_bilingual.jsonl` stores both languages for every scenario.
Portuguese and English share scenario ID, placeholders, negative and positive
actions, question polarity, and logical answer. `questions/categories_bilingual.yaml`
stores canonical group IDs and their language-specific realizations. Umbanda
and Candomblé retain their Brazilian names.

## Identifiers

- `semantic_block_id`: category, scenario, and group pair; bootstrap cluster.
- `semantic_pair_id`: the same question condition in PT and EN.
- `logical_id`: semantic pair plus experimental language.
- `example_id`: logical item plus option rotation.

Only text and language change across a `semantic_pair_id`. Category, scenario,
groups, target, condition, semantic correct answer, biased content, and rotation
remain identical.

## Review protocol

Reviewers should compare paired rows without seeing model predictions. They
should assess semantic equivalence, naturalness, person-centered phrasing,
cultural specificity, question polarity, disambiguating evidence, and the
configured stereotype direction. Any rejected pair must be revised in both
languages and assigned a new catalog version before rerunning the benchmark.
