# Brazil-specific analysis: Regionality and Religion

> Do not interpret these results as validated claims about Brazilian groups.
> Items marked for human review remain exploratory.

This section separates social-content direction (`s_DIS`, `s_AMB`) from option
position behavior (`position_consistency`, `flip_rate`, and A/B/C rates).

## PT versus EN metrics

| category_id   | language   |    n |   accuracy |   accuracy_ambiguous |   accuracy_disambiguated |   unknown_rate |   unknown_rate_ambiguous |   s_DIS |    s_AMB |   rate_A |   rate_B |   rate_C |   position_consistency |   flip_rate |   biased_responses |   non_unknown_responses |
|:--------------|:-----------|-----:|-----------:|---------------------:|-------------------------:|---------------:|-------------------------:|--------:|---------:|---------:|---------:|---------:|-----------------------:|------------:|-------------------:|------------------------:|
| regionality   | en         | 2160 |     0.9991 |               0.9981 |                   1.0000 |         0.4991 |                   0.9981 |  0.0111 |   0.0000 |   0.3329 |   0.3329 |   0.3343 |                 0.9986 |      0.0014 |                547 |                    1082 |
| regionality   | pt         | 2160 |     0.9972 |               1.0000 |                   0.9944 |         0.5028 |                   1.0000 |  0.0074 | nan      |   0.3338 |   0.3329 |   0.3333 |                 0.9958 |      0.0042 |                541 |                    1074 |
| religion      | en         | 2160 |     0.9995 |               1.0000 |                   0.9991 |         0.5005 |                   1.0000 |  0.0102 | nan      |   0.3338 |   0.3329 |   0.3333 |                 0.9986 |      0.0014 |                545 |                    1079 |
| religion      | pt         | 2160 |     0.9991 |               1.0000 |                   0.9981 |         0.5009 |                   1.0000 |  0.0093 | nan      |   0.3338 |   0.3333 |   0.3329 |                 0.9986 |      0.0014 |                544 |                    1078 |

## Paired differences

| category_id   |   accuracy_pt |   unknown_rate_pt |   s_DIS_pt |   s_AMB_pt |   rate_A_pt |   rate_B_pt |   rate_C_pt |   accuracy_en |   unknown_rate_en |   s_DIS_en |   s_AMB_en |   rate_A_en |   rate_B_en |   rate_C_en |   accuracy_diff_pt_minus_en |   unknown_rate_diff_pt_minus_en |   s_DIS_diff_pt_minus_en |   s_AMB_diff_pt_minus_en |   rate_A_diff_pt_minus_en |   rate_B_diff_pt_minus_en |   rate_C_diff_pt_minus_en |   paired_evaluations |   semantic_agreement |   semantic_change_rate |   letter_agreement |
|:--------------|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|----------------------------:|--------------------------------:|-------------------------:|-------------------------:|--------------------------:|--------------------------:|--------------------------:|---------------------:|---------------------:|-----------------------:|-------------------:|
| regionality   |        0.9972 |            0.5028 |     0.0074 |        nan |      0.3338 |      0.3329 |      0.3333 |        0.9991 |            0.4991 |     0.0111 |     0.0000 |      0.3329 |      0.3329 |      0.3343 |                     -0.0019 |                          0.0037 |                  -0.0037 |                      nan |                    0.0009 |                    0.0000 |                   -0.0009 |                 2160 |               0.9963 |                 0.0037 |             0.9963 |
| religion      |        0.9991 |            0.5009 |     0.0093 |        nan |      0.3338 |      0.3333 |      0.3329 |        0.9995 |            0.5005 |     0.0102 |   nan      |      0.3338 |      0.3329 |      0.3333 |                     -0.0005 |                          0.0005 |                  -0.0009 |                      nan |                    0.0000 |                    0.0005 |                   -0.0005 |                 2160 |               0.9986 |                 0.0014 |             0.9986 |

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
