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
| Accuracy | 0.9727 |
| Ambiguous accuracy | 0.9547 |
| Disambiguated accuracy | 0.9907 |
| Unknown rate | 0.4815 |
| s_DIS | 0.0052 |
| s_AMB | 0.0304 |
| Position consistency | 0.9409 |
| Flip rate | 0.0591 |

## Paired PT versus EN

|   accuracy_pt |   unknown_rate_pt |   s_DIS_pt |   s_AMB_pt |   rate_A_pt |   rate_B_pt |   rate_C_pt |   accuracy_en |   unknown_rate_en |   s_DIS_en |   s_AMB_en |   rate_A_en |   rate_B_en |   rate_C_en |   accuracy_diff_pt_minus_en |   unknown_rate_diff_pt_minus_en |   s_DIS_diff_pt_minus_en |   s_AMB_diff_pt_minus_en |   rate_A_diff_pt_minus_en |   rate_B_diff_pt_minus_en |   rate_C_diff_pt_minus_en |   paired_evaluations |   semantic_agreement |   semantic_change_rate |   letter_agreement |
|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|----------------------------:|--------------------------------:|-------------------------:|-------------------------:|--------------------------:|--------------------------:|--------------------------:|---------------------:|---------------------:|-----------------------:|-------------------:|
|        0.9662 |            0.4761 |     0.0048 |     0.0395 |      0.3478 |      0.3353 |      0.3169 |        0.9792 |            0.4870 |     0.0055 |     0.0212 |      0.3423 |      0.3361 |      0.3217 |                     -0.0131 |                         -0.0109 |                  -0.0006 |                   0.0183 |                    0.0055 |                   -0.0008 |                   -0.0047 |           18360.0000 |               0.9673 |                 0.0327 |             0.9673 |

## Category metrics

| category_id           | language   |    n |   accuracy |   accuracy_ambiguous |   accuracy_disambiguated |   unknown_rate |   unknown_rate_ambiguous |   s_DIS |    s_AMB |   rate_A |   rate_B |   rate_C |   position_consistency |   flip_rate |   biased_responses |   non_unknown_responses |
|:----------------------|:-----------|-----:|-----------:|---------------------:|-------------------------:|---------------:|-------------------------:|--------:|---------:|---------:|---------:|---------:|-----------------------:|------------:|-------------------:|------------------------:|
| education             | en         | 1800 |     0.9661 |               0.9400 |                   0.9922 |         0.4728 |                   0.9400 |  0.0034 |   0.0578 |   0.3467 |   0.3344 |   0.3189 |                 0.9367 |      0.0633 |                502 |                     949 |
| education             | pt         | 1800 |     0.9383 |               0.8844 |                   0.9922 |         0.4456 |                   0.8844 |  0.0067 |   0.1000 |   0.3511 |   0.3383 |   0.3106 |                 0.8933 |      0.1067 |                547 |                     998 |
| gender                | en         | 1800 |     0.9917 |               0.9978 |                   0.9856 |         0.5050 |                   0.9978 | -0.0079 |   0.0000 |   0.3367 |   0.3328 |   0.3306 |                 0.9800 |      0.0200 |                442 |                     891 |
| gender                | pt         | 1800 |     0.9872 |               0.9956 |                   0.9789 |         0.5083 |                   0.9956 | -0.0057 |   0.0022 |   0.3394 |   0.3333 |   0.3272 |                 0.9717 |      0.0283 |                441 |                     885 |
| interior_capital      | en         | 2160 |     0.9602 |               0.9259 |                   0.9944 |         0.4657 |                   0.9259 |  0.0074 |   0.0704 |   0.3481 |   0.3421 |   0.3097 |                 0.9111 |      0.0889 |                619 |                    1154 |
| interior_capital      | pt         | 2160 |     0.9148 |               0.8343 |                   0.9954 |         0.4194 |                   0.8343 |  0.0084 |   0.1250 |   0.3611 |   0.3588 |   0.2801 |                 0.8056 |      0.1944 |                699 |                    1254 |
| music_preference      | en         | 2160 |     0.9856 |               0.9731 |                   0.9981 |         0.4875 |                   0.9731 |  0.0093 |   0.0028 |   0.3370 |   0.3389 |   0.3241 |                 0.9667 |      0.0333 |                560 |                    1107 |
| music_preference      | pt         | 2160 |     0.9690 |               0.9426 |                   0.9954 |         0.4731 |                   0.9426 |  0.0112 |   0.0259 |   0.3509 |   0.3241 |   0.3250 |                 0.9306 |      0.0694 |                589 |                    1138 |
| political_orientation | en         | 1800 |     0.9761 |               0.9611 |                   0.9911 |         0.4833 |                   0.9611 |  0.0056 |  -0.0122 |   0.3444 |   0.3339 |   0.3217 |                 0.9533 |      0.0467 |                462 |                     930 |
| political_orientation | pt         | 1800 |     0.9878 |               0.9789 |                   0.9967 |         0.4911 |                   0.9789 | -0.0011 |   0.0011 |   0.3406 |   0.3317 |   0.3278 |                 0.9783 |      0.0217 |                458 |                     916 |
| race_color            | en         | 2160 |     0.9903 |               0.9991 |                   0.9815 |         0.5083 |                   0.9991 |  0.0009 |  -0.0009 |   0.3366 |   0.3338 |   0.3296 |                 0.9819 |      0.0181 |                531 |                    1062 |
| race_color            | pt         | 2160 |     0.9866 |               1.0000 |                   0.9731 |         0.5130 |                   1.0000 | -0.0019 | nan      |   0.3407 |   0.3301 |   0.3292 |                 0.9736 |      0.0264 |                525 |                    1052 |
| regionality           | en         | 2160 |     0.9829 |               0.9676 |                   0.9981 |         0.4847 |                   0.9676 |  0.0093 |   0.0250 |   0.3403 |   0.3370 |   0.3227 |                 0.9611 |      0.0389 |                575 |                    1113 |
| regionality           | pt         | 2160 |     0.9944 |               0.9917 |                   0.9972 |         0.4963 |                   0.9917 |  0.0120 |   0.0028 |   0.3366 |   0.3338 |   0.3296 |                 0.9833 |      0.0167 |                552 |                    1088 |
| religion              | en         | 2160 |     0.9912 |               0.9861 |                   0.9963 |         0.4949 |                   0.9861 |  0.0093 |   0.0083 |   0.3403 |   0.3338 |   0.3259 |                 0.9750 |      0.0250 |                555 |                    1091 |
| religion              | pt         | 2160 |     0.9898 |               0.9861 |                   0.9935 |         0.4963 |                   0.9861 |  0.0065 |   0.0028 |   0.3366 |   0.3356 |   0.3278 |                 0.9750 |      0.0250 |                549 |                    1088 |
| socioeconomic_class   | en         | 2160 |     0.9685 |               0.9500 |                   0.9870 |         0.4806 |                   0.9500 |  0.0094 |   0.0370 |   0.3505 |   0.3366 |   0.3130 |                 0.9306 |      0.0694 |                586 |                    1122 |
| socioeconomic_class   | pt         | 2160 |     0.9301 |               0.8750 |                   0.9852 |         0.4444 |                   0.8750 |  0.0047 |   0.0935 |   0.3708 |   0.3315 |   0.2977 |                 0.8403 |      0.1597 |                653 |                    1200 |

The confidence intervals in `metrics/paired_bootstrap.json` use semantic blocks
that keep both languages, all four logical conditions, and all three option
permutations together during resampling.
