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
| Accuracy | 0.9957 |
| Ambiguous accuracy | 0.9985 |
| Disambiguated accuracy | 0.9929 |
| Unknown rate | 0.5028 |
| s_DIS | 0.0010 |
| s_AMB | -0.0002 |
| Position consistency | 0.9918 |
| Flip rate | 0.0082 |

## Paired PT versus EN

|   accuracy_pt |   unknown_rate_pt |   s_DIS_pt |   s_AMB_pt |   rate_A_pt |   rate_B_pt |   rate_C_pt |   accuracy_en |   unknown_rate_en |   s_DIS_en |   s_AMB_en |   rate_A_en |   rate_B_en |   rate_C_en |   accuracy_diff_pt_minus_en |   unknown_rate_diff_pt_minus_en |   s_DIS_diff_pt_minus_en |   s_AMB_diff_pt_minus_en |   rate_A_diff_pt_minus_en |   rate_B_diff_pt_minus_en |   rate_C_diff_pt_minus_en |   paired_evaluations |   semantic_agreement |   semantic_change_rate |   letter_agreement |
|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|----------------------------:|--------------------------------:|-------------------------:|-------------------------:|--------------------------:|--------------------------:|--------------------------:|---------------------:|---------------------:|-----------------------:|-------------------:|
|        0.9947 |            0.5047 |    -0.0022 |    -0.0004 |      0.3338 |      0.3331 |      0.3331 |        0.9967 |            0.5009 |     0.0043 |     0.0000 |      0.3336 |      0.3327 |      0.3337 |                     -0.0020 |                          0.0038 |                  -0.0065 |                  -0.0004 |                    0.0002 |                    0.0004 |                   -0.0006 |           18360.0000 |               0.9937 |                 0.0063 |             0.9937 |

## Category metrics

| category_id           | language   |    n |   accuracy |   accuracy_ambiguous |   accuracy_disambiguated |   unknown_rate |   unknown_rate_ambiguous |   s_DIS |    s_AMB |   rate_A |   rate_B |   rate_C |   position_consistency |   flip_rate |   biased_responses |   non_unknown_responses |
|:----------------------|:-----------|-----:|-----------:|---------------------:|-------------------------:|---------------:|-------------------------:|--------:|---------:|---------:|---------:|---------:|-----------------------:|------------:|-------------------:|------------------------:|
| education             | en         | 1800 |     0.9983 |               0.9967 |                   1.0000 |         0.4983 |                   0.9967 |  0.0000 |   0.0033 |   0.3344 |   0.3328 |   0.3328 |                 0.9967 |      0.0033 |                453 |                     903 |
| education             | pt         | 1800 |     0.9922 |               0.9978 |                   0.9867 |         0.5056 |                   0.9978 | -0.0135 |   0.0000 |   0.3328 |   0.3339 |   0.3333 |                 0.9850 |      0.0150 |                439 |                     890 |
| gender                | en         | 1800 |     0.9961 |               1.0000 |                   0.9922 |         0.5039 |                   1.0000 | -0.0078 | nan      |   0.3333 |   0.3339 |   0.3328 |                 0.9917 |      0.0083 |                443 |                     893 |
| gender                | pt         | 1800 |     0.9894 |               0.9978 |                   0.9811 |         0.5083 |                   0.9978 | -0.0193 |  -0.0022 |   0.3339 |   0.3322 |   0.3339 |                 0.9867 |      0.0133 |                433 |                     885 |
| interior_capital      | en         | 2160 |     0.9995 |               0.9991 |                   1.0000 |         0.4995 |                   0.9991 |  0.0111 |   0.0009 |   0.3338 |   0.3329 |   0.3333 |                 0.9986 |      0.0014 |                547 |                    1081 |
| interior_capital      | pt         | 2160 |     0.9995 |               1.0000 |                   0.9991 |         0.5005 |                   1.0000 |  0.0102 | nan      |   0.3329 |   0.3333 |   0.3338 |                 0.9986 |      0.0014 |                545 |                    1079 |
| music_preference      | en         | 2160 |     0.9981 |               0.9963 |                   1.0000 |         0.4981 |                   0.9963 |  0.0111 |  -0.0037 |   0.3324 |   0.3329 |   0.3347 |                 0.9958 |      0.0042 |                546 |                    1084 |
| music_preference      | pt         | 2160 |     1.0000 |               1.0000 |                   1.0000 |         0.5000 |                   1.0000 |  0.0111 | nan      |   0.3333 |   0.3333 |   0.3333 |                 1.0000 |      0.0000 |                546 |                    1080 |
| political_orientation | en         | 1800 |     0.9944 |               0.9889 |                   1.0000 |         0.4944 |                   0.9889 |  0.0000 |  -0.0044 |   0.3350 |   0.3294 |   0.3356 |                 0.9883 |      0.0117 |                453 |                     910 |
| political_orientation | pt         | 1800 |     1.0000 |               1.0000 |                   1.0000 |         0.5000 |                   1.0000 |  0.0000 | nan      |   0.3333 |   0.3333 |   0.3333 |                 1.0000 |      0.0000 |                450 |                     900 |
| race_color            | en         | 2160 |     0.9921 |               0.9991 |                   0.9852 |         0.5069 |                   0.9991 | -0.0019 |   0.0009 |   0.3347 |   0.3324 |   0.3329 |                 0.9847 |      0.0153 |                532 |                    1065 |
| race_color            | pt         | 2160 |     0.9847 |               1.0000 |                   0.9694 |         0.5153 |                   1.0000 | -0.0201 | nan      |   0.3366 |   0.3324 |   0.3310 |                 0.9708 |      0.0292 |                513 |                    1047 |
| regionality           | en         | 2160 |     0.9986 |               1.0000 |                   0.9972 |         0.5014 |                   1.0000 |  0.0084 | nan      |   0.3338 |   0.3333 |   0.3329 |                 0.9972 |      0.0028 |                543 |                    1077 |
| regionality           | pt         | 2160 |     0.9935 |               1.0000 |                   0.9870 |         0.5065 |                   1.0000 | -0.0019 | nan      |   0.3329 |   0.3343 |   0.3329 |                 0.9944 |      0.0056 |                532 |                    1066 |
| religion              | en         | 2160 |     0.9949 |               0.9981 |                   0.9917 |         0.5032 |                   0.9981 |  0.0065 |   0.0019 |   0.3329 |   0.3338 |   0.3333 |                 0.9861 |      0.0139 |                541 |                    1073 |
| religion              | pt         | 2160 |     0.9972 |               1.0000 |                   0.9944 |         0.5028 |                   1.0000 |  0.0056 | nan      |   0.3343 |   0.3324 |   0.3333 |                 0.9931 |      0.0069 |                540 |                    1074 |
| socioeconomic_class   | en         | 2160 |     0.9977 |               0.9991 |                   0.9963 |         0.5014 |                   0.9991 |  0.0074 |   0.0009 |   0.3324 |   0.3329 |   0.3347 |                 0.9931 |      0.0069 |                543 |                    1077 |
| socioeconomic_class   | pt         | 2160 |     0.9949 |               0.9981 |                   0.9917 |         0.5032 |                   0.9981 |  0.0028 |  -0.0019 |   0.3343 |   0.3329 |   0.3329 |                 0.9917 |      0.0083 |                537 |                    1073 |

The confidence intervals in `metrics/paired_bootstrap.json` use semantic blocks
that keep both languages, all four logical conditions, and all three option
permutations together during resampling.
