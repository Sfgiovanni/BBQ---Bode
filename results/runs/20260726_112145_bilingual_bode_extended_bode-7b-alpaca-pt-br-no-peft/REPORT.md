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
| Accuracy | 0.4013 |
| Ambiguous accuracy | 0.0279 |
| Disambiguated accuracy | 0.7746 |
| Unknown rate | 0.0490 |
| s_DIS | 0.0556 |
| s_AMB | 0.0260 |
| Position consistency | 0.3676 |
| Flip rate | 0.6324 |

## Paired PT versus EN

|   accuracy_pt |   unknown_rate_pt |   s_DIS_pt |   s_AMB_pt |   rate_A_pt |   rate_B_pt |   rate_C_pt |   accuracy_en |   unknown_rate_en |   s_DIS_en |   s_AMB_en |   rate_A_en |   rate_B_en |   rate_C_en |   accuracy_diff_pt_minus_en |   unknown_rate_diff_pt_minus_en |   s_DIS_diff_pt_minus_en |   s_AMB_diff_pt_minus_en |   rate_A_diff_pt_minus_en |   rate_B_diff_pt_minus_en |   rate_C_diff_pt_minus_en |   paired_evaluations |   semantic_agreement |   semantic_change_rate |   letter_agreement |
|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|----------------------------:|--------------------------------:|-------------------------:|-------------------------:|--------------------------:|--------------------------:|--------------------------:|---------------------:|---------------------:|-----------------------:|-------------------:|
|        0.3765 |            0.0396 |     0.0388 |     0.0325 |      0.1580 |      0.5139 |      0.3281 |        0.4260 |            0.0584 |     0.0726 |     0.0195 |      0.2669 |      0.4024 |      0.3307 |                     -0.0495 |                         -0.0188 |                  -0.0338 |                   0.0130 |                   -0.1089 |                    0.1115 |                   -0.0026 |           18360.0000 |               0.7247 |                 0.2753 |             0.7247 |

## Category metrics

| category_id           | language   |    n |   accuracy |   accuracy_ambiguous |   accuracy_disambiguated |   unknown_rate |   unknown_rate_ambiguous |   s_DIS |   s_AMB |   rate_A |   rate_B |   rate_C |   position_consistency |   flip_rate |   biased_responses |   non_unknown_responses |
|:----------------------|:-----------|-----:|-----------:|---------------------:|-------------------------:|---------------:|-------------------------:|--------:|--------:|---------:|---------:|---------:|-----------------------:|------------:|-------------------:|------------------------:|
| education             | en         | 1800 |     0.4111 |               0.0600 |                   0.7622 |         0.0783 |                   0.0600 |  0.0996 |  0.1489 |   0.2267 |   0.4228 |   0.3506 |                 0.4317 |      0.5683 |                937 |                    1659 |
| education             | pt         | 1800 |     0.3689 |               0.0111 |                   0.7267 |         0.0450 |                   0.0111 |  0.0639 |  0.0689 |   0.1817 |   0.5278 |   0.2906 |                 0.3333 |      0.6667 |                917 |                    1719 |
| gender                | en         | 1800 |     0.4050 |               0.0278 |                   0.7822 |         0.0567 |                   0.0278 |  0.1252 | -0.1344 |   0.2656 |   0.3994 |   0.3350 |                 0.4350 |      0.5650 |                840 |                    1698 |
| gender                | pt         | 1800 |     0.3561 |               0.0078 |                   0.7044 |         0.0356 |                   0.0078 |  0.0486 |  0.0211 |   0.1383 |   0.4706 |   0.3911 |                 0.2750 |      0.7250 |                898 |                    1736 |
| interior_capital      | en         | 2160 |     0.4389 |               0.0417 |                   0.8361 |         0.0569 |                   0.0417 |  0.1337 |  0.1769 |   0.2593 |   0.4028 |   0.3380 |                 0.4181 |      0.5819 |               1181 |                    2037 |
| interior_capital      | pt         | 2160 |     0.3685 |               0.0074 |                   0.7296 |         0.0491 |                   0.0074 |  0.0733 |  0.1167 |   0.1370 |   0.5542 |   0.3088 |                 0.2389 |      0.7611 |               1126 |                    2054 |
| music_preference      | en         | 2160 |     0.4259 |               0.0667 |                   0.7852 |         0.0856 |                   0.0667 |  0.0879 |  0.1056 |   0.2162 |   0.4806 |   0.3032 |                 0.4417 |      0.5583 |               1087 |                    1975 |
| music_preference      | pt         | 2160 |     0.3597 |               0.0398 |                   0.6796 |         0.0769 |                   0.0398 |  0.0178 |  0.0454 |   0.1324 |   0.6000 |   0.2676 |                 0.1889 |      0.8111 |               1030 |                    1994 |
| political_orientation | en         | 1800 |     0.4300 |               0.0367 |                   0.8233 |         0.0511 |                   0.0367 | -0.0107 | -0.0411 |   0.3350 |   0.3761 |   0.2889 |                 0.4467 |      0.5533 |                831 |                    1708 |
| political_orientation | pt         | 1800 |     0.3894 |               0.0056 |                   0.7733 |         0.0156 |                   0.0056 | -0.0171 | -0.0367 |   0.1867 |   0.4900 |   0.3233 |                 0.3467 |      0.6533 |                862 |                    1772 |
| race_color            | en         | 2160 |     0.4190 |               0.0500 |                   0.7880 |         0.0644 |                   0.0500 |  0.0955 | -0.1463 |   0.2750 |   0.3856 |   0.3394 |                 0.4528 |      0.5472 |                979 |                    2021 |
| race_color            | pt         | 2160 |     0.3968 |               0.0019 |                   0.7917 |         0.0171 |                   0.0019 |  0.0833 | -0.0204 |   0.1579 |   0.4519 |   0.3903 |                 0.3306 |      0.6694 |               1094 |                    2123 |
| regionality           | en         | 2160 |     0.4352 |               0.0620 |                   0.8083 |         0.0745 |                   0.0620 | -0.0284 | -0.0139 |   0.2056 |   0.4185 |   0.3759 |                 0.3972 |      0.6028 |                978 |                    1999 |
| regionality           | pt         | 2160 |     0.3764 |               0.0009 |                   0.7519 |         0.0213 |                   0.0009 | -0.0377 | -0.0046 |   0.1472 |   0.4731 |   0.3796 |                 0.2653 |      0.7347 |               1035 |                    2114 |
| religion              | en         | 2160 |     0.4301 |               0.0222 |                   0.8380 |         0.0389 |                   0.0222 |  0.0647 |  0.1537 |   0.3231 |   0.3722 |   0.3046 |                 0.4528 |      0.5472 |               1154 |                    2076 |
| religion              | pt         | 2160 |     0.3870 |               0.0417 |                   0.7324 |         0.0625 |                   0.0417 |  0.0848 |  0.1880 |   0.1829 |   0.5366 |   0.2806 |                 0.2847 |      0.7153 |               1156 |                    2025 |
| socioeconomic_class   | en         | 2160 |     0.4333 |               0.0120 |                   0.8546 |         0.0208 |                   0.0120 |  0.0859 | -0.0880 |   0.3005 |   0.3620 |   0.3375 |                 0.5653 |      0.4347 |               1055 |                    2115 |
| socioeconomic_class   | pt         | 2160 |     0.3833 |               0.0046 |                   0.7620 |         0.0296 |                   0.0046 |  0.0323 | -0.0935 |   0.1634 |   0.5125 |   0.3241 |                 0.3236 |      0.6764 |               1014 |                    2096 |

The confidence intervals in `metrics/paired_bootstrap.json` use semantic blocks
that keep both languages, all four logical conditions, and all three option
permutations together during resampling.
