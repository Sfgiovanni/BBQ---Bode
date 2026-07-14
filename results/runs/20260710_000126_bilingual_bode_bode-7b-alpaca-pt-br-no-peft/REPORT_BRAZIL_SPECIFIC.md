# Brazil-specific analysis: Regionality and Religion

> Do not interpret these results as validated claims about Brazilian groups.
> Items marked for human review remain exploratory.

This section separates social-content direction (`s_DIS`, `s_AMB`) from option
position behavior (`position_consistency`, `flip_rate`, and A/B/C rates).

## PT versus EN metrics

| category_id   | language   |    n |   accuracy |   accuracy_ambiguous |   accuracy_disambiguated |   unknown_rate |   unknown_rate_ambiguous |   s_DIS |   s_AMB |   rate_A |   rate_B |   rate_C |   position_consistency |   flip_rate |   biased_responses |   non_unknown_responses |
|:--------------|:-----------|-----:|-----------:|---------------------:|-------------------------:|---------------:|-------------------------:|--------:|--------:|---------:|---------:|---------:|-----------------------:|------------:|-------------------:|------------------------:|
| regionality   | en         | 1080 |     0.4333 |               0.0611 |                   0.8056 |         0.0731 |                   0.0611 | -0.0405 | -0.0574 |   0.2093 |   0.4148 |   0.3759 |                 0.3917 |      0.6083 |                475 |                    1001 |
| regionality   | pt         | 1080 |     0.3731 |               0.0000 |                   0.7463 |         0.0222 |                   0.0000 | -0.0349 | -0.0481 |   0.1481 |   0.4648 |   0.3870 |                 0.2750 |      0.7250 |                506 |                    1056 |
| religion      | en         | 1080 |     0.4333 |               0.0259 |                   0.8407 |         0.0398 |                   0.0259 |  0.0802 |  0.1370 |   0.3157 |   0.3685 |   0.3157 |                 0.4556 |      0.5444 |                576 |                    1037 |
| religion      | pt         | 1080 |     0.3843 |               0.0352 |                   0.7333 |         0.0602 |                   0.0352 |  0.0769 |  0.1870 |   0.1880 |   0.5370 |   0.2750 |                 0.2861 |      0.7139 |                577 |                    1015 |

## Paired differences

| category_id   |   accuracy_pt |   unknown_rate_pt |   s_DIS_pt |   s_AMB_pt |   rate_A_pt |   rate_B_pt |   rate_C_pt |   accuracy_en |   unknown_rate_en |   s_DIS_en |   s_AMB_en |   rate_A_en |   rate_B_en |   rate_C_en |   accuracy_diff_pt_minus_en |   unknown_rate_diff_pt_minus_en |   s_DIS_diff_pt_minus_en |   s_AMB_diff_pt_minus_en |   rate_A_diff_pt_minus_en |   rate_B_diff_pt_minus_en |   rate_C_diff_pt_minus_en |   paired_evaluations |   semantic_agreement |   semantic_change_rate |   letter_agreement |
|:--------------|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|----------------------------:|--------------------------------:|-------------------------:|-------------------------:|--------------------------:|--------------------------:|--------------------------:|---------------------:|---------------------:|-----------------------:|-------------------:|
| regionality   |        0.3731 |            0.0222 |    -0.0349 |    -0.0481 |      0.1481 |      0.4648 |      0.3870 |        0.4333 |            0.0731 |    -0.0405 |    -0.0574 |      0.2093 |      0.4148 |      0.3759 |                     -0.0602 |                         -0.0509 |                   0.0056 |                   0.0093 |                   -0.0611 |                    0.0500 |                    0.0111 |                 1080 |               0.7398 |                 0.2602 |             0.7398 |
| religion      |        0.3843 |            0.0602 |     0.0769 |     0.1870 |      0.1880 |      0.5370 |      0.2750 |        0.4333 |            0.0398 |     0.0802 |     0.1370 |      0.3157 |      0.3685 |      0.3157 |                     -0.0491 |                          0.0204 |                  -0.0033 |                   0.0500 |                   -0.1278 |                    0.1685 |                   -0.0407 |                 1080 |               0.7102 |                 0.2898 |             0.7102 |

## Ambiguous group coverage

| category_id   | language   | semantic_biased_answer   |   selected_or_present_count |
|:--------------|:-----------|:-------------------------|----------------------------:|
| regionality   | en         | central_west_brazil      |                          90 |
| regionality   | en         | north_brazil             |                          90 |
| regionality   | en         | northeast_brazil         |                          90 |
| regionality   | en         | sao_paulo_state          |                          90 |
| regionality   | en         | south_brazil             |                          90 |
| regionality   | en         | southeast_brazil         |                          90 |
| regionality   | pt         | central_west_brazil      |                          90 |
| regionality   | pt         | north_brazil             |                          90 |
| regionality   | pt         | northeast_brazil         |                          90 |
| regionality   | pt         | sao_paulo_state          |                          90 |
| regionality   | pt         | south_brazil             |                          90 |
| regionality   | pt         | southeast_brazil         |                          90 |
| religion      | en         | candomble                |                          90 |
| religion      | en         | catholic                 |                          90 |
| religion      | en         | evangelical              |                          90 |
| religion      | en         | no_religion              |                          90 |
| religion      | en         | spiritist                |                          90 |
| religion      | en         | umbanda                  |                          90 |
| religion      | pt         | candomble                |                          90 |
| religion      | pt         | catholic                 |                          90 |
| religion      | pt         | evangelical              |                          90 |
| religion      | pt         | no_religion              |                          90 |
| religion      | pt         | spiritist                |                          90 |
| religion      | pt         | umbanda                  |                          90 |

The religion category explicitly includes Umbanda, Candomblé, and people with
no religion. The regionality category includes groups from all five Brazilian
macro-regions. Rows flagged for human validation in these categories: 4320.
