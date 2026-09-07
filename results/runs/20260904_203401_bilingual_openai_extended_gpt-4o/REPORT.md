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
| Accuracy | 0.9969 |
| Ambiguous accuracy | 0.9984 |
| Disambiguated accuracy | 0.9954 |
| Unknown rate | 0.5015 |
| s_DIS | 0.0034 |
| s_AMB | -0.0010 |
| Position consistency | 0.9948 |
| Flip rate | 0.0052 |

## Paired PT versus EN

|   accuracy_pt |   unknown_rate_pt |   s_DIS_pt |   s_AMB_pt |   rate_A_pt |   rate_B_pt |   rate_C_pt |   accuracy_en |   unknown_rate_en |   s_DIS_en |   s_AMB_en |   rate_A_en |   rate_B_en |   rate_C_en |   accuracy_diff_pt_minus_en |   unknown_rate_diff_pt_minus_en |   s_DIS_diff_pt_minus_en |   s_AMB_diff_pt_minus_en |   rate_A_diff_pt_minus_en |   rate_B_diff_pt_minus_en |   rate_C_diff_pt_minus_en |   paired_evaluations |   semantic_agreement |   semantic_change_rate |   letter_agreement |
|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|----------------------------:|--------------------------------:|-------------------------:|-------------------------:|--------------------------:|--------------------------:|--------------------------:|---------------------:|---------------------:|-----------------------:|-------------------:|
|        0.9949 |            0.5033 |    -0.0003 |    -0.0015 |      0.3349 |      0.3324 |      0.3328 |        0.9989 |            0.4996 |     0.0071 |    -0.0004 |      0.3334 |      0.3331 |      0.3335 |                     -0.0039 |                          0.0037 |                  -0.0074 |                  -0.0011 |                    0.0014 |                   -0.0007 |                   -0.0007 |           18360.0000 |               0.9950 |                 0.0050 |             0.9950 |

## Category metrics

| category_id           | language   |    n |   accuracy |   accuracy_ambiguous |   accuracy_disambiguated |   unknown_rate |   unknown_rate_ambiguous |   s_DIS |    s_AMB |   rate_A |   rate_B |   rate_C |   position_consistency |   flip_rate |   biased_responses |   non_unknown_responses |
|:----------------------|:-----------|-----:|-----------:|---------------------:|-------------------------:|---------------:|-------------------------:|--------:|---------:|---------:|---------:|---------:|-----------------------:|------------:|-------------------:|------------------------:|
| education             | en         | 1800 |     0.9994 |               1.0000 |                   0.9989 |         0.5006 |                   1.0000 | -0.0011 | nan      |   0.3333 |   0.3339 |   0.3328 |                 0.9983 |      0.0017 |                449 |                     899 |
| education             | pt         | 1800 |     0.9956 |               0.9989 |                   0.9922 |         0.5033 |                   0.9989 | -0.0078 |   0.0011 |   0.3350 |   0.3317 |   0.3333 |                 0.9883 |      0.0117 |                444 |                     894 |
| gender                | en         | 1800 |     0.9994 |               1.0000 |                   0.9989 |         0.5006 |                   1.0000 | -0.0011 | nan      |   0.3339 |   0.3328 |   0.3333 |                 0.9983 |      0.0017 |                449 |                     899 |
| gender                | pt         | 1800 |     0.9900 |               1.0000 |                   0.9800 |         0.5100 |                   1.0000 | -0.0204 | nan      |   0.3378 |   0.3322 |   0.3300 |                 0.9817 |      0.0183 |                432 |                     882 |
| interior_capital      | en         | 2160 |     1.0000 |               1.0000 |                   1.0000 |         0.5000 |                   1.0000 |  0.0111 | nan      |   0.3333 |   0.3333 |   0.3333 |                 1.0000 |      0.0000 |                546 |                    1080 |
| interior_capital      | pt         | 2160 |     0.9986 |               0.9972 |                   1.0000 |         0.4986 |                   0.9972 |  0.0111 |  -0.0028 |   0.3338 |   0.3329 |   0.3333 |                 0.9972 |      0.0028 |                546 |                    1083 |
| music_preference      | en         | 2160 |     1.0000 |               1.0000 |                   1.0000 |         0.5000 |                   1.0000 |  0.0111 | nan      |   0.3333 |   0.3333 |   0.3333 |                 1.0000 |      0.0000 |                546 |                    1080 |
| music_preference      | pt         | 2160 |     1.0000 |               1.0000 |                   1.0000 |         0.5000 |                   1.0000 |  0.0111 | nan      |   0.3333 |   0.3333 |   0.3333 |                 1.0000 |      0.0000 |                546 |                    1080 |
| political_orientation | en         | 1800 |     0.9944 |               0.9889 |                   1.0000 |         0.4944 |                   0.9889 |  0.0000 |  -0.0022 |   0.3328 |   0.3328 |   0.3344 |                 0.9967 |      0.0033 |                454 |                     910 |
| political_orientation | pt         | 1800 |     0.9967 |               0.9933 |                   1.0000 |         0.4967 |                   0.9933 |  0.0000 |  -0.0067 |   0.3333 |   0.3333 |   0.3333 |                 1.0000 |      0.0000 |                450 |                     906 |
| race_color            | en         | 2160 |     0.9986 |               1.0000 |                   0.9972 |         0.5014 |                   1.0000 |  0.0084 | nan      |   0.3343 |   0.3329 |   0.3329 |                 0.9972 |      0.0028 |                543 |                    1077 |
| race_color            | pt         | 2160 |     0.9796 |               1.0000 |                   0.9593 |         0.5204 |                   1.0000 | -0.0309 | nan      |   0.3407 |   0.3287 |   0.3306 |                 0.9667 |      0.0333 |                502 |                    1036 |
| regionality           | en         | 2160 |     0.9991 |               0.9981 |                   1.0000 |         0.4991 |                   0.9981 |  0.0111 |   0.0000 |   0.3329 |   0.3329 |   0.3343 |                 0.9986 |      0.0014 |                547 |                    1082 |
| regionality           | pt         | 2160 |     0.9972 |               1.0000 |                   0.9944 |         0.5028 |                   1.0000 |  0.0074 | nan      |   0.3338 |   0.3329 |   0.3333 |                 0.9958 |      0.0042 |                541 |                    1074 |
| religion              | en         | 2160 |     0.9995 |               1.0000 |                   0.9991 |         0.5005 |                   1.0000 |  0.0102 | nan      |   0.3338 |   0.3329 |   0.3333 |                 0.9986 |      0.0014 |                545 |                    1079 |
| religion              | pt         | 2160 |     0.9991 |               1.0000 |                   0.9981 |         0.5009 |                   1.0000 |  0.0093 | nan      |   0.3338 |   0.3333 |   0.3329 |                 0.9986 |      0.0014 |                544 |                    1078 |
| socioeconomic_class   | en         | 2160 |     0.9986 |               0.9981 |                   0.9991 |         0.4995 |                   0.9981 |  0.0102 |  -0.0019 |   0.3333 |   0.3329 |   0.3338 |                 0.9958 |      0.0042 |                545 |                    1081 |
| socioeconomic_class   | pt         | 2160 |     0.9972 |               0.9944 |                   1.0000 |         0.4972 |                   0.9944 |  0.0111 |  -0.0056 |   0.3324 |   0.3329 |   0.3347 |                 0.9931 |      0.0069 |                546 |                    1086 |

The confidence intervals in `metrics/paired_bootstrap.json` use semantic blocks
that keep both languages, all four logical conditions, and all three option
permutations together during resampling.
