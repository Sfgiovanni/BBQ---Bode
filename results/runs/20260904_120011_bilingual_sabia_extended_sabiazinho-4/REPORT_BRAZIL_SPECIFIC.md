# Brazil-specific analysis: Regionality and Religion

> Do not interpret these results as validated claims about Brazilian groups.
> Items marked for human review remain exploratory.

This section separates social-content direction (`s_DIS`, `s_AMB`) from option
position behavior (`position_consistency`, `flip_rate`, and A/B/C rates).

## PT versus EN metrics

| category_id   | language   |    n |   accuracy |   accuracy_ambiguous |   accuracy_disambiguated |   unknown_rate |   unknown_rate_ambiguous |   s_DIS |    s_AMB |   rate_A |   rate_B |   rate_C |   position_consistency |   flip_rate |   biased_responses |   non_unknown_responses |
|:--------------|:-----------|-----:|-----------:|---------------------:|-------------------------:|---------------:|-------------------------:|--------:|---------:|---------:|---------:|---------:|-----------------------:|------------:|-------------------:|------------------------:|
| regionality   | en         | 2160 |     1.0000 |               1.0000 |                   1.0000 |         0.5000 |                   1.0000 |  0.0111 | nan      |   0.3333 |   0.3333 |   0.3333 |                 1.0000 |      0.0000 |                546 |                    1080 |
| regionality   | pt         | 2160 |     0.9963 |               1.0000 |                   0.9926 |         0.5037 |                   1.0000 |  0.0093 | nan      |   0.3338 |   0.3319 |   0.3343 |                 0.9917 |      0.0083 |                541 |                    1072 |
| religion      | en         | 2160 |     0.9847 |               0.9954 |                   0.9741 |         0.5106 |                   0.9954 |  0.0114 |   0.0009 |   0.3394 |   0.3250 |   0.3356 |                 0.9597 |      0.0403 |                535 |                    1057 |
| religion      | pt         | 2160 |     0.9782 |               1.0000 |                   0.9565 |         0.5218 |                   1.0000 |  0.0145 | nan      |   0.3352 |   0.3264 |   0.3384 |                 0.9625 |      0.0375 |                524 |                    1033 |

## Paired differences

| category_id   |   accuracy_pt |   unknown_rate_pt |   s_DIS_pt |   s_AMB_pt |   rate_A_pt |   rate_B_pt |   rate_C_pt |   accuracy_en |   unknown_rate_en |   s_DIS_en |   s_AMB_en |   rate_A_en |   rate_B_en |   rate_C_en |   accuracy_diff_pt_minus_en |   unknown_rate_diff_pt_minus_en |   s_DIS_diff_pt_minus_en |   s_AMB_diff_pt_minus_en |   rate_A_diff_pt_minus_en |   rate_B_diff_pt_minus_en |   rate_C_diff_pt_minus_en |   paired_evaluations |   semantic_agreement |   semantic_change_rate |   letter_agreement |
|:--------------|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|----------------------------:|--------------------------------:|-------------------------:|-------------------------:|--------------------------:|--------------------------:|--------------------------:|---------------------:|---------------------:|-----------------------:|-------------------:|
| regionality   |        0.9963 |            0.5037 |     0.0093 |        nan |      0.3338 |      0.3319 |      0.3343 |        1.0000 |            0.5000 |     0.0111 |   nan      |      0.3333 |      0.3333 |      0.3333 |                     -0.0037 |                          0.0037 |                  -0.0018 |                      nan |                    0.0005 |                   -0.0014 |                    0.0009 |                 2160 |               0.9963 |                 0.0037 |             0.9963 |
| religion      |        0.9782 |            0.5218 |     0.0145 |        nan |      0.3352 |      0.3264 |      0.3384 |        0.9847 |            0.5106 |     0.0114 |     0.0009 |      0.3394 |      0.3250 |      0.3356 |                     -0.0065 |                          0.0111 |                   0.0031 |                      nan |                   -0.0042 |                    0.0014 |                    0.0028 |                 2160 |               0.9685 |                 0.0315 |             0.9685 |

## Ambiguous group coverage

| category_id   | language   | semantic_biased_answer   |   selected_or_present_count |
|:--------------|:-----------|:-------------------------|----------------------------:|
| regionality   | en         | central_west_brazil      |                          90 |
| regionality   | en         | north_brazil             |                         180 |
| regionality   | en         | northeast_brazil         |                         270 |
| regionality   | en         | sao_paulo_state          |                         180 |
| regionality   | en         | south_brazil             |                         180 |
| regionality   | en         | southeast_brazil         |                         180 |
| regionality   | pt         | central_west_brazil      |                          90 |
| regionality   | pt         | north_brazil             |                         180 |
| regionality   | pt         | northeast_brazil         |                         270 |
| regionality   | pt         | sao_paulo_state          |                         180 |
| regionality   | pt         | south_brazil             |                         180 |
| regionality   | pt         | southeast_brazil         |                         180 |
| religion      | en         | candomble                |                         180 |
| religion      | en         | catholic                 |                         180 |
| religion      | en         | evangelical              |                         270 |
| religion      | en         | no_religion              |                         180 |
| religion      | en         | spiritist                |                          90 |
| religion      | en         | umbanda                  |                         180 |
| religion      | pt         | candomble                |                         180 |
| religion      | pt         | catholic                 |                         180 |
| religion      | pt         | evangelical              |                         270 |
| religion      | pt         | no_religion              |                         180 |
| religion      | pt         | spiritist                |                          90 |
| religion      | pt         | umbanda                  |                         180 |

The religion category explicitly includes Umbanda, Candomblé, and people with
no religion. The regionality category includes groups from all five Brazilian
macro-regions. Rows flagged for human validation in these categories: 8640.
