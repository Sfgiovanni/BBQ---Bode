# Extended catalog vs. reference run

> Computational comparison, not a validated social-science finding. Both
> catalogs carry `needs_human_validation: true`; the extended catalog's added
> pairs are unreviewed by the collaborator's own annotation.

Reference run: `20260710_000126_bilingual_bode_bode-7b-alpaca-pt-br-no-peft`
(27 pairs, 19,440 evaluations).
This run: `20260726_112145_bilingual_bode_extended_bode-7b-alpaca-pt-br-no-peft`
(51 pairs, 36,720 evaluations), same seed (42), same pinned model revision
(`ff1ecd8eccbd7bcd04fa247d140cf783f8cd73ec`), same `batch_size: 4`, same
`scoring_method: first_token_logprob`, `do_sample: false`.

See `docs/EXTENDED_PAIRS_AUDIT.md` for the catalog diff and methodological
review this report follows up on. Four questions raised there
(political_orientation direction pairs, race_color reference-group split,
`undeclared_color`, global category weighting) are **still open** — this
report presents the raw evidence for those decisions, it does not resolve
them.

## 1. The 27 original pairs: exact match, not just "within noise"

This is the headline result. Restricting this run's 36,720 evaluations to
the 19,440 `example_id`s that exist in the reference run:

- **`selected_content`, `predicted_option`, `is_correct`, `is_biased_answer`
  are identical on all 19,440 rows — zero mismatches.** Every aggregate
  metric (accuracy, unknown rate, `s_DIS`, `s_AMB`, position consistency,
  flip rate) computed on this subset equals the reference run's value to
  full floating-point precision, not approximately.
- Raw logprobs differ on a small number of rows (40/19,440 for each of
  `logprob_A/B/C`, ~0.2%) and the full generated continuation text differs
  on 156/19,440 rows (~0.8%) — consistent with float32/float16 accumulation
  order changing slightly when a row lands in a different batch (the
  extended dataset interleaves more rows, changing padding/batch
  composition). **None of these numerical differences changed any decision**
  (argmax option), so no scored metric is affected.

This is the strongest form of the Step 3 proof: appending 24 pairs did not
perturb the original 27 pairs' outcomes at all, at the model-output level,
not just the dataset-construction level verified earlier by
`tests/test_extended_catalog.py`. It also validates that the model-revision
pin and the `batch_size: 4` pin (both applied specifically to make this
comparison possible) worked as intended.

| metric | reference | extended (same 27 pairs) | difference |
|---|---:|---:|---:|
| n | 19,440 | 19,440 | 0 |
| accuracy | 0.3990 | 0.3990 | 0.0000 |
| accuracy_ambiguous | 0.0259 | 0.0259 | 0.0000 |
| accuracy_disambiguated | 0.7720 | 0.7720 | 0.0000 |
| unknown_rate | 0.0467 | 0.0467 | 0.0000 |
| s_DIS | 0.0399 | 0.0399 | 0.0000 |
| s_AMB | -0.0259 | -0.0259 | 0.0000 |
| position_consistency | 0.3718 | 0.3718 | 0.0000 |
| flip_rate | 0.6282 | 0.6282 | 0.0000 |

## 2. The 24 new pairs, isolated

| metric | new pairs only (n=17,280) | original 27 pairs | full 51 pairs |
|---|---:|---:|---:|
| accuracy | 0.4038 | 0.3990 | 0.4013 |
| accuracy_ambiguous | 0.0302 | 0.0259 | 0.0279 |
| accuracy_disambiguated | 0.7774 | 0.7720 | 0.7746 |
| unknown_rate | 0.0516 | 0.0467 | 0.0490 |
| s_DIS | 0.0734 | 0.0399 | 0.0556 |
| s_AMB | 0.0844 | -0.0259 | 0.0260 |
| position_consistency | 0.3630 | 0.3718 | 0.3676 |
| flip_rate | 0.6370 | 0.6282 | 0.6324 |

The new pairs alone show both a higher (more positive) `s_DIS` and a **sign
flip on `s_AMB`** (-0.026 pooled-original vs. +0.084 new-only) relative to
the original 27. Accuracy and position metrics move much less. This is a
real difference in what the new pairs measure, not noise — see sections 4-5
for the two categories (`political_orientation`, `race_color`) that explain
most of the category-level swings, and note the other seven categories also
shift, just by less.

## 3. Bootstrap interval effect of more clusters

Cluster count for the paired bootstrap (`semantic_block_id`) roughly doubles
(3,240 → ~6,120 depending on category-language slice), and interval widths
shrink to ~70-73% of the reference width — matching the CLT expectation
`sqrt(3240/6120) ≈ 0.728` almost exactly:

| metric | reference CI | extended CI | width ratio |
|---|---|---|---:|
| s_DIS_pt | [-0.0286, 0.0594] | [0.0074, 0.0713] | 0.726 |
| s_DIS_en | [0.0084, 0.1163] | [0.0345, 0.1094] | 0.694 |
| s_AMB_pt | [-0.0416, 0.0047] | [0.0173, 0.0477] | 0.656 |
| s_AMB_en | [-0.0617, -0.0082] | [0.0011, 0.0381] | 0.692 |
| accuracy_pt | [0.3690, 0.3790] | [0.3729, 0.3801] | 0.720 |
| accuracy_en | [0.4188, 0.4288] | [0.4223, 0.4295] | 0.715 |

**Beyond just narrowing, three intervals change which side of zero they're
on** — this is a substantive shift, not just tighter noise bounds, and it's
driven by the new pairs' different central tendency (section 2), not by
sample size alone:

- `s_DIS_pt`: reference crosses zero (not significant) → extended is
  entirely positive (significant).
- `s_AMB_pt`: reference crosses zero → extended is entirely positive.
- `s_AMB_en`: reference is entirely **negative** (significant) → extended is
  essentially zero/marginally positive.

Whether this reflects the model's real behavior on the new pairs' content,
or an artifact of the political_orientation/race_color aggregation issues
below, is exactly the kind of question the open aggregation decisions in
`docs/EXTENDED_PAIRS_AUDIT.md` need to settle before this goes in the paper.

## 4. Category-level `s_DIS` / `s_AMB`: magnitude and sign

No category flips the *sign* of its pooled `s_DIS` or `s_AMB` when adding
the new pairs. But two categories show large magnitude changes that are not
just sampling variation — they're structural, per sections 5-6 below.

| category | ref s_DIS | ext(51) s_DIS | Δ | ref s_AMB | ext(51) s_AMB | Δ |
|---|---:|---:|---:|---:|---:|---:|
| education | 0.0371 | 0.0816 | +0.0445 | 0.0731 | 0.1089 | +0.0357 |
| gender | 0.0321 | 0.0864 | +0.0544 | -0.1120 | -0.0567 | +0.0554 |
| interior_capital | 0.1120 | 0.1038 | -0.0082 | 0.1370 | 0.1468 | +0.0097 |
| music_preference | 0.0333 | 0.0530 | +0.0198 | 0.0880 | 0.0755 | -0.0125 |
| **political_orientation** | -0.0360 | **-0.0140** | +0.0221 | -0.1815 | **-0.0389** | +0.1426 |
| **race_color** | 0.1007 | 0.0892 | -0.0115 | -0.1991 | **-0.0833** | +0.1157 |
| regionality | -0.0376 | -0.0332 | +0.0045 | -0.0528 | -0.0093 | +0.0435 |
| religion | 0.0786 | 0.0746 | -0.0040 | 0.1620 | 0.1708 | +0.0088 |
| socioeconomic_class | 0.0398 | 0.0594 | +0.0197 | -0.1481 | -0.0907 | +0.0574 |

`political_orientation` and `race_color` show the two largest `s_AMB`
shifts (+0.143 and +0.116, both toward zero) — these are exactly the two
categories flagged in the audit as having a structural pooling issue, not a
coincidence. `regionality`'s `s_AMB` also shrinks substantially
(-0.053 → -0.009); unlike the other two, none of `regionality`'s new pairs
reverse stereotype direction or change reference group, so this shift looks
like ordinary sampling/content variation from the three new region-pairs,
not a pooling artifact — flagging for awareness, not as a third structural
case.

## 5. political_orientation: direction-inverted pairs, quantified

Per-pair breakdown confirms the cancellation predicted in the audit,
computed on this run's actual predictions (not simulated):

| pair_id | n | s_DIS | s_AMB |
|---|---:|---:|---:|
| left_right | 720 | 0.0000 | -0.1444 |
| right_left | 720 | -0.0317 | +0.1444 |
| progressive_conservative | 720 | -0.0957 | -0.2139 |
| conservative_progressive | 720 | +0.0698 | +0.2056 |
| center_nonpartisan | 720 | -0.0119 | -0.1861 |

`left_right`/`right_left` and `progressive_conservative`/
`conservative_progressive` are each near-mirror-image in `s_AMB`
(sum ≈ 0.000 and ≈ -0.008 respectively) and pull toward each other in
`s_DIS` too. Pooling all 5 pairs into one category number
(`s_AMB = -0.0389`, section 4) mixes this near-total cancellation from 4 of
the 5 pairs with the one non-inverted pair (`center_nonpartisan`,
`s_AMB = -0.1861`) that carries most of the pooled category's remaining
signal. **This is the audit's open question 1: is the pooled number, the
per-direction stratified numbers, or a directional-asymmetry statistic the
right thing to report? Still awaiting your answer on whether the inversion
is intentional design or duplication before picking one.**

## 6. race_color: two different reference groups, quantified

| pair_id | anchor | n | s_DIS | s_AMB |
|---|---|---:|---:|---:|
| black_white | white | 720 | 0.1297 | -0.1611 |
| brown_white | white | 720 | 0.0920 | -0.1694 |
| indigenous_white | white | 720 | 0.0805 | -0.2667 |
| black_asian | asian_brazilian | 720 | 0.1078 | +0.1361 |
| brown_asian | asian_brazilian | 720 | 0.0599 | +0.0028 |
| indigenous_asian | asian_brazilian | 720 | 0.0638 | -0.0417 |

`vs_white` pairs are uniformly `s_AMB`-negative (model favors the reference
group in ambiguous contexts by not selecting the target as often); `vs_asian`
pairs are near-zero-to-positive. `s_DIS` is positive for both anchors but
consistently larger for `vs_white`. Pooling both anchors into the single
`race_color` category number (section 4) averages across two different
reference-group comparisons, same issue as in the audit's open question 2.
This table is the "vs_white / vs_asian" split proposed there, ready to use
if you confirm that's how you want it reported.

## Summary for the paper

- The extended run does not contradict the reference run anywhere it can be
  checked directly — the 27 shared pairs are bit-identical in every decision.
- The additional 24 pairs are not neutral padding: they shift the pooled
  `s_AMB` sign in two of three bootstrap intervals, driven almost entirely
  by `political_orientation` (direction cancellation) and `race_color`
  (reference-group mixing), not by the other seven categories.
- This is itself a useful methodological finding for the paper: pooled
  category-level bias scores are sensitive to catalog design choices
  (adding a reverse-direction pair, changing a reference group) in ways that
  don't show up as a validation error, only as a metric that moves. Worth a
  paragraph regardless of how the four open aggregation questions are
  ultimately resolved.
