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
| Accuracy | 0.9767 |
| Ambiguous accuracy | 0.9803 |
| Disambiguated accuracy | 0.9731 |
| Unknown rate | 0.5036 |
| s_DIS | -0.0036 |
| s_AMB | 0.0075 |
| Position consistency | 0.9599 |
| Flip rate | 0.0401 |

## Paired PT versus EN

|   accuracy_pt |   unknown_rate_pt |   s_DIS_pt |   s_AMB_pt |   rate_A_pt |   rate_B_pt |   rate_C_pt |   accuracy_en |   unknown_rate_en |   s_DIS_en |   s_AMB_en |   rate_A_en |   rate_B_en |   rate_C_en |   accuracy_diff_pt_minus_en |   unknown_rate_diff_pt_minus_en |   s_DIS_diff_pt_minus_en |   s_AMB_diff_pt_minus_en |   rate_A_diff_pt_minus_en |   rate_B_diff_pt_minus_en |   rate_C_diff_pt_minus_en |   paired_evaluations |   semantic_agreement |   semantic_change_rate |   letter_agreement |
|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|----------------------------:|--------------------------------:|-------------------------:|-------------------------:|--------------------------:|--------------------------:|--------------------------:|---------------------:|---------------------:|-----------------------:|-------------------:|
|        0.9775 |            0.5154 |    -0.0066 |     0.0021 |      0.3338 |      0.3282 |      0.3381 |        0.9759 |            0.4918 |    -0.0007 |     0.0130 |      0.3401 |      0.3253 |      0.3346 |                      0.0016 |                          0.0236 |                  -0.0059 |                  -0.0109 |                   -0.0063 |                    0.0029 |                    0.0034 |           18360.0000 |               0.9630 |                 0.0370 |             0.9630 |

## Category metrics

| category_id           | language   |    n |   accuracy |   accuracy_ambiguous |   accuracy_disambiguated |   unknown_rate |   unknown_rate_ambiguous |   s_DIS |    s_AMB |   rate_A |   rate_B |   rate_C |   position_consistency |   flip_rate |   biased_responses |   non_unknown_responses |
|:----------------------|:-----------|-----:|-----------:|---------------------:|-------------------------:|---------------:|-------------------------:|--------:|---------:|---------:|---------:|---------:|-----------------------:|------------:|-------------------:|------------------------:|
| education             | en         | 1800 |     0.9722 |               0.9522 |                   0.9922 |         0.4800 |                   0.9522 | -0.0034 |   0.0478 |   0.3422 |   0.3261 |   0.3317 |                 0.9633 |      0.0367 |                488 |                     936 |
| education             | pt         | 1800 |     0.9683 |               0.9856 |                   0.9511 |         0.5172 |                   0.9856 | -0.0164 |   0.0144 |   0.3311 |   0.3261 |   0.3428 |                 0.9417 |      0.0583 |                434 |                     869 |
| gender                | en         | 1800 |     0.9717 |               1.0000 |                   0.9433 |         0.5283 |                   1.0000 | -0.0459 | nan      |   0.3361 |   0.3233 |   0.3406 |                 0.9600 |      0.0400 |                405 |                     849 |
| gender                | pt         | 1800 |     0.9250 |               1.0000 |                   0.8500 |         0.5750 |                   1.0000 | -0.0850 | nan      |   0.3339 |   0.3167 |   0.3494 |                 0.8967 |      0.1033 |                350 |                     765 |
| interior_capital      | en         | 2160 |     0.9727 |               0.9454 |                   1.0000 |         0.4727 |                   0.9454 |  0.0111 |   0.0343 |   0.3449 |   0.3204 |   0.3347 |                 0.9458 |      0.0542 |                594 |                    1139 |
| interior_capital      | pt         | 2160 |     0.9917 |               0.9852 |                   0.9981 |         0.4935 |                   0.9852 |  0.0093 |   0.0056 |   0.3343 |   0.3333 |   0.3324 |                 0.9806 |      0.0194 |                555 |                    1094 |
| music_preference      | en         | 2160 |     0.9958 |               0.9917 |                   1.0000 |         0.4958 |                   0.9917 |  0.0111 |   0.0046 |   0.3343 |   0.3310 |   0.3347 |                 0.9889 |      0.0111 |                553 |                    1089 |
| music_preference      | pt         | 2160 |     0.9944 |               0.9991 |                   0.9898 |         0.5046 |                   0.9991 |  0.0140 |   0.0009 |   0.3370 |   0.3301 |   0.3329 |                 0.9847 |      0.0153 |                543 |                    1070 |
| political_orientation | en         | 1800 |     0.9489 |               0.9011 |                   0.9967 |         0.4522 |                   0.9011 | -0.0011 |  -0.0011 |   0.3411 |   0.3256 |   0.3333 |                 0.9317 |      0.0683 |                492 |                     986 |
| political_orientation | pt         | 1800 |     0.9867 |               0.9778 |                   0.9956 |         0.4911 |                   0.9778 |  0.0000 |   0.0000 |   0.3344 |   0.3311 |   0.3344 |                 0.9750 |      0.0250 |                458 |                     916 |
| race_color            | en         | 2160 |     0.9764 |               0.9991 |                   0.9537 |         0.5227 |                   0.9991 | -0.0194 |   0.0009 |   0.3366 |   0.3241 |   0.3394 |                 0.9542 |      0.0458 |                506 |                    1031 |
| race_color            | pt         | 2160 |     0.9681 |               1.0000 |                   0.9361 |         0.5319 |                   1.0000 | -0.0188 | nan      |   0.3338 |   0.3236 |   0.3426 |                 0.9472 |      0.0528 |                496 |                    1011 |
| regionality           | en         | 2160 |     1.0000 |               1.0000 |                   1.0000 |         0.5000 |                   1.0000 |  0.0111 | nan      |   0.3333 |   0.3333 |   0.3333 |                 1.0000 |      0.0000 |                546 |                    1080 |
| regionality           | pt         | 2160 |     0.9963 |               1.0000 |                   0.9926 |         0.5037 |                   1.0000 |  0.0093 | nan      |   0.3338 |   0.3319 |   0.3343 |                 0.9917 |      0.0083 |                541 |                    1072 |
| religion              | en         | 2160 |     0.9847 |               0.9954 |                   0.9741 |         0.5106 |                   0.9954 |  0.0114 |   0.0009 |   0.3394 |   0.3250 |   0.3356 |                 0.9597 |      0.0403 |                535 |                    1057 |
| religion              | pt         | 2160 |     0.9782 |               1.0000 |                   0.9565 |         0.5218 |                   1.0000 |  0.0145 | nan      |   0.3352 |   0.3264 |   0.3384 |                 0.9625 |      0.0375 |                524 |                    1033 |
| socioeconomic_class   | en         | 2160 |     0.9546 |               0.9157 |                   0.9935 |         0.4611 |                   0.9157 |  0.0084 |   0.0306 |   0.3528 |   0.3185 |   0.3287 |                 0.9236 |      0.0764 |                603 |                    1164 |
| socioeconomic_class   | pt         | 2160 |     0.9801 |               0.9861 |                   0.9741 |         0.5060 |                   0.9861 | -0.0095 |  -0.0009 |   0.3301 |   0.3324 |   0.3375 |                 0.9556 |      0.0444 |                528 |                    1067 |

The confidence intervals in `metrics/paired_bootstrap.json` use semantic blocks
that keep both languages, all four logical conditions, and all three option
permutations together during resampling.
