# Bilingual Brazilian BBQ computational report

> This is a computational benchmark run, not publication-ready social evidence.
> Bilingual templates and stereotype directions require expert human validation.

## Scope

- 9 categories; music preference is exploratory cultural content and is excluded from protected-demographic interpretations.
- Paired Brazilian Portuguese and English prompts with three option rotations.
- Social bias metrics and positional metrics are reported separately.

## Overall metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.3990 |
| Ambiguous accuracy | 0.0259 |
| Disambiguated accuracy | 0.7720 |
| Unknown rate | 0.0467 |
| s_DIS | 0.0399 |
| s_AMB | -0.0259 |
| Position consistency | 0.3718 |
| Flip rate | 0.6282 |

## Paired PT versus EN

|   accuracy_pt |   unknown_rate_pt |   s_DIS_pt |   s_AMB_pt |   rate_A_pt |   rate_B_pt |   rate_C_pt |   accuracy_en |   unknown_rate_en |   s_DIS_en |   s_AMB_en |   rate_A_en |   rate_B_en |   rate_C_en |   accuracy_diff_pt_minus_en |   unknown_rate_diff_pt_minus_en |   s_DIS_diff_pt_minus_en |   s_AMB_diff_pt_minus_en |   rate_A_diff_pt_minus_en |   rate_B_diff_pt_minus_en |   rate_C_diff_pt_minus_en |   paired_evaluations |   semantic_agreement |   semantic_change_rate |   letter_agreement |
|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|----------------------------:|--------------------------------:|-------------------------:|-------------------------:|--------------------------:|--------------------------:|--------------------------:|---------------------:|---------------------:|-----------------------:|-------------------:|
|        0.3740 |            0.0390 |     0.0156 |    -0.0177 |      0.1602 |      0.5050 |      0.3348 |        0.4240 |            0.0544 |     0.0644 |    -0.0342 |      0.2680 |      0.3978 |      0.3342 |                     -0.0500 |                         -0.0154 |                  -0.0488 |                   0.0165 |                   -0.1078 |                    0.1072 |                    0.0006 |            9720.0000 |               0.7296 |                 0.2704 |             0.7296 |

## Category metrics

| category_id           | language   |    n |   accuracy |   accuracy_ambiguous |   accuracy_disambiguated |   unknown_rate |   unknown_rate_ambiguous |   s_DIS |   s_AMB |   rate_A |   rate_B |   rate_C |   position_consistency |   flip_rate |   biased_responses |   non_unknown_responses |
|:----------------------|:-----------|-----:|-----------:|---------------------:|-------------------------:|---------------:|-------------------------:|--------:|--------:|---------:|---------:|---------:|-----------------------:|------------:|-------------------:|------------------------:|
| education             | en         | 1080 |     0.4074 |               0.0463 |                   0.7685 |         0.0639 |                   0.0463 |  0.0242 |  0.1093 |   0.2213 |   0.4000 |   0.3787 |                 0.4278 |      0.5722 |                541 |                    1011 |
| education             | pt         | 1080 |     0.3620 |               0.0074 |                   0.7167 |         0.0398 |                   0.0074 |  0.0499 |  0.0370 |   0.1769 |   0.5139 |   0.3093 |                 0.3556 |      0.6444 |                541 |                    1037 |
| gender                | en         | 1080 |     0.4065 |               0.0352 |                   0.7778 |         0.0611 |                   0.0352 |  0.0832 | -0.1796 |   0.2611 |   0.4037 |   0.3352 |                 0.4083 |      0.5917 |                479 |                    1014 |
| gender                | pt         | 1080 |     0.3528 |               0.0111 |                   0.6944 |         0.0380 |                   0.0111 | -0.0178 | -0.0444 |   0.1361 |   0.4769 |   0.3870 |                 0.2778 |      0.7222 |                503 |                    1039 |
| interior_capital      | en         | 1080 |     0.4361 |               0.0407 |                   0.8315 |         0.0565 |                   0.0407 |  0.1457 |  0.1667 |   0.2537 |   0.4083 |   0.3380 |                 0.4194 |      0.5806 |                591 |                    1019 |
| interior_capital      | pt         | 1080 |     0.3657 |               0.0111 |                   0.7204 |         0.0519 |                   0.0111 |  0.0776 |  0.1074 |   0.1287 |   0.5556 |   0.3157 |                 0.2194 |      0.7806 |                560 |                    1024 |
| music_preference      | en         | 1080 |     0.4315 |               0.0704 |                   0.7926 |         0.0870 |                   0.0704 |  0.0702 |  0.1148 |   0.2167 |   0.4880 |   0.2954 |                 0.4417 |      0.5583 |                541 |                     986 |
| music_preference      | pt         | 1080 |     0.3620 |               0.0463 |                   0.6778 |         0.0806 |                   0.0463 | -0.0042 |  0.0611 |   0.1389 |   0.6028 |   0.2583 |                 0.2056 |      0.7944 |                512 |                     993 |
| political_orientation | en         | 1080 |     0.4315 |               0.0463 |                   0.8167 |         0.0574 |                   0.0463 |  0.0020 | -0.2204 |   0.3370 |   0.3769 |   0.2861 |                 0.4417 |      0.5583 |                450 |                    1018 |
| political_orientation | pt         | 1080 |     0.3907 |               0.0056 |                   0.7759 |         0.0176 |                   0.0056 | -0.0725 | -0.1426 |   0.1917 |   0.4907 |   0.3176 |                 0.3639 |      0.6361 |                473 |                    1061 |
| race_color            | en         | 1080 |     0.4176 |               0.0130 |                   0.8222 |         0.0306 |                   0.0130 |  0.1167 | -0.2685 |   0.3056 |   0.3593 |   0.3352 |                 0.5000 |      0.5000 |                481 |                    1047 |
| race_color            | pt         | 1080 |     0.4009 |               0.0000 |                   0.8019 |         0.0102 |                   0.0000 |  0.0851 | -0.1296 |   0.1593 |   0.4056 |   0.4352 |                 0.3417 |      0.6583 |                522 |                    1069 |
| regionality           | en         | 1080 |     0.4333 |               0.0611 |                   0.8056 |         0.0731 |                   0.0611 | -0.0405 | -0.0574 |   0.2093 |   0.4148 |   0.3759 |                 0.3917 |      0.6083 |                475 |                    1001 |
| regionality           | pt         | 1080 |     0.3731 |               0.0000 |                   0.7463 |         0.0222 |                   0.0000 | -0.0349 | -0.0481 |   0.1481 |   0.4648 |   0.3870 |                 0.2750 |      0.7250 |                506 |                    1056 |
| religion              | en         | 1080 |     0.4333 |               0.0259 |                   0.8407 |         0.0398 |                   0.0259 |  0.0802 |  0.1370 |   0.3157 |   0.3685 |   0.3157 |                 0.4556 |      0.5444 |                576 |                    1037 |
| religion              | pt         | 1080 |     0.3843 |               0.0352 |                   0.7333 |         0.0602 |                   0.0352 |  0.0769 |  0.1870 |   0.1880 |   0.5370 |   0.2750 |                 0.2861 |      0.7139 |                577 |                    1015 |
| socioeconomic_class   | en         | 1080 |     0.4185 |               0.0056 |                   0.8315 |         0.0204 |                   0.0056 |  0.0940 | -0.1093 |   0.2917 |   0.3611 |   0.3472 |                 0.5389 |      0.4611 |                524 |                    1058 |
| socioeconomic_class   | pt         | 1080 |     0.3741 |               0.0056 |                   0.7426 |         0.0306 |                   0.0056 | -0.0157 | -0.1870 |   0.1741 |   0.4981 |   0.3278 |                 0.3417 |      0.6583 |                469 |                    1047 |

The confidence intervals in `metrics/paired_bootstrap.json` use semantic blocks
that keep both languages, all four logical conditions, and all three option
permutations together during resampling.
