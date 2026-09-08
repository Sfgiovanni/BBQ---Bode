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
| Accuracy | 0.8658 |
| Ambiguous accuracy | 0.7473 |
| Disambiguated accuracy | 0.9843 |
| Unknown rate | 0.3778 |
| s_DIS | 0.0045 |
| s_AMB | 0.0011 |
| Position consistency | 0.7486 |
| Flip rate | 0.2514 |

## Paired PT versus EN

|   accuracy_pt |   unknown_rate_pt |   s_DIS_pt |   s_AMB_pt |   rate_A_pt |   rate_B_pt |   rate_C_pt |   accuracy_en |   unknown_rate_en |   s_DIS_en |   s_AMB_en |   rate_A_en |   rate_B_en |   rate_C_en |   accuracy_diff_pt_minus_en |   unknown_rate_diff_pt_minus_en |   s_DIS_diff_pt_minus_en |   s_AMB_diff_pt_minus_en |   rate_A_diff_pt_minus_en |   rate_B_diff_pt_minus_en |   rate_C_diff_pt_minus_en |   paired_evaluations |   semantic_agreement |   semantic_change_rate |   letter_agreement |
|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|----------------------------:|--------------------------------:|-------------------------:|-------------------------:|--------------------------:|--------------------------:|--------------------------:|---------------------:|---------------------:|-----------------------:|-------------------:|
|        0.8613 |            0.3746 |     0.0021 |     0.0094 |      0.3660 |      0.2769 |      0.3571 |        0.8702 |            0.3811 |     0.0069 |    -0.0072 |      0.3716 |      0.3448 |      0.2836 |                     -0.0089 |                         -0.0065 |                  -0.0048 |                   0.0166 |                   -0.0056 |                   -0.0679 |                    0.0735 |           18360.0000 |               0.8416 |                 0.1584 |             0.8416 |

## Category metrics

| category_id           | language   |    n |   accuracy |   accuracy_ambiguous |   accuracy_disambiguated |   unknown_rate |   unknown_rate_ambiguous |   s_DIS |   s_AMB |   rate_A |   rate_B |   rate_C |   position_consistency |   flip_rate |   biased_responses |   non_unknown_responses |
|:----------------------|:-----------|-----:|-----------:|---------------------:|-------------------------:|---------------:|-------------------------:|--------:|--------:|---------:|---------:|---------:|-----------------------:|------------:|-------------------:|------------------------:|
| education             | en         | 1800 |     0.8772 |               0.7644 |                   0.9900 |         0.3856 |                   0.7644 |  0.0089 |  0.0689 |   0.3744 |   0.3389 |   0.2867 |                 0.7700 |      0.2300 |                588 |                    1106 |
| education             | pt         | 1800 |     0.8022 |               0.6111 |                   0.9933 |         0.3067 |                   0.6111 | -0.0022 |  0.0889 |   0.3961 |   0.2839 |   0.3200 |                 0.6950 |      0.3050 |                663 |                    1248 |
| gender                | en         | 1800 |     0.8778 |               0.8000 |                   0.9556 |         0.4183 |                   0.8000 | -0.0058 | -0.0356 |   0.3550 |   0.3583 |   0.2867 |                 0.7417 |      0.2583 |                505 |                    1047 |
| gender                | pt         | 1800 |     0.8817 |               0.8289 |                   0.9344 |         0.4344 |                   0.8289 | -0.0417 | -0.0511 |   0.3450 |   0.2783 |   0.3767 |                 0.7317 |      0.2683 |                468 |                    1018 |
| interior_capital      | en         | 2160 |     0.7931 |               0.5981 |                   0.9880 |         0.3000 |                   0.5981 |  0.0019 | -0.0130 |   0.3685 |   0.3519 |   0.2796 |                 0.6750 |      0.3250 |                750 |                    1512 |
| interior_capital      | pt         | 2160 |     0.8051 |               0.6231 |                   0.9870 |         0.3148 |                   0.6231 |  0.0028 |  0.0213 |   0.3829 |   0.2574 |   0.3597 |                 0.6333 |      0.3667 |                753 |                    1480 |
| music_preference      | en         | 2160 |     0.8944 |               0.7935 |                   0.9954 |         0.3981 |                   0.7935 |  0.0121 |  0.0583 |   0.3718 |   0.3681 |   0.2602 |                 0.7556 |      0.2444 |                688 |                    1300 |
| music_preference      | pt         | 2160 |     0.9315 |               0.8676 |                   0.9954 |         0.4352 |                   0.8676 |  0.0139 |  0.0028 |   0.3532 |   0.3139 |   0.3329 |                 0.8472 |      0.1528 |                619 |                    1220 |
| political_orientation | en         | 1800 |     0.8872 |               0.7822 |                   0.9922 |         0.3950 |                   0.7822 |  0.0011 |  0.0311 |   0.3733 |   0.3228 |   0.3039 |                 0.8217 |      0.1783 |                559 |                    1089 |
| political_orientation | pt         | 1800 |     0.8711 |               0.7544 |                   0.9878 |         0.3800 |                   0.7544 |  0.0034 |  0.0700 |   0.3600 |   0.2717 |   0.3683 |                 0.7583 |      0.2417 |                591 |                    1116 |
| race_color            | en         | 2160 |     0.9301 |               0.8750 |                   0.9852 |         0.4444 |                   0.8750 |  0.0066 | -0.0731 |   0.3412 |   0.3435 |   0.3153 |                 0.8875 |      0.1125 |                564 |                    1200 |
| race_color            | pt         | 2160 |     0.9069 |               0.8546 |                   0.9593 |         0.4329 |                   0.8546 | -0.0169 | -0.0657 |   0.3389 |   0.2782 |   0.3829 |                 0.7806 |      0.2194 |                568 |                    1225 |
| regionality           | en         | 2160 |     0.8935 |               0.7944 |                   0.9926 |         0.3981 |                   0.7944 |  0.0167 |  0.0889 |   0.3722 |   0.3375 |   0.2903 |                 0.8014 |      0.1986 |                707 |                    1300 |
| regionality           | pt         | 2160 |     0.8796 |               0.7704 |                   0.9889 |         0.3861 |                   0.7704 |  0.0130 | -0.0056 |   0.3560 |   0.2556 |   0.3884 |                 0.7250 |      0.2750 |                667 |                    1326 |
| religion              | en         | 2160 |     0.8931 |               0.7981 |                   0.9880 |         0.4023 |                   0.7981 |  0.0103 | -0.0333 |   0.3838 |   0.3259 |   0.2903 |                 0.7833 |      0.2167 |                633 |                    1291 |
| religion              | pt         | 2160 |     0.9056 |               0.8241 |                   0.9870 |         0.4144 |                   0.8241 |  0.0251 |  0.0204 |   0.3454 |   0.2718 |   0.3829 |                 0.7778 |      0.2222 |                657 |                    1265 |
| socioeconomic_class   | en         | 2160 |     0.7907 |               0.5889 |                   0.9926 |         0.2972 |                   0.5889 |  0.0074 | -0.1426 |   0.4023 |   0.3542 |   0.2435 |                 0.6653 |      0.3347 |                686 |                    1518 |
| socioeconomic_class   | pt         | 2160 |     0.7634 |               0.5315 |                   0.9954 |         0.2662 |                   0.5315 |  0.0120 |  0.0167 |   0.4171 |   0.2819 |   0.3009 |                 0.6292 |      0.3708 |                808 |                    1585 |

The confidence intervals in `metrics/paired_bootstrap.json` use semantic blocks
that keep both languages, all four logical conditions, and all three option
permutations together during resampling.
