# Brazil-specific analysis: Regionality and Religion

> Do not interpret these results as validated claims about Brazilian groups.
> Items marked for human review remain exploratory.

This section separates social-content direction (`s_DIS`, `s_AMB`) from option
position behavior (`position_consistency`, `flip_rate`, and A/B/C rates).

## PT versus EN metrics

| category_id   | language   |    n |   accuracy |   accuracy_ambiguous |   accuracy_disambiguated |   unknown_rate |   unknown_rate_ambiguous |   s_DIS |   s_AMB |   rate_A |   rate_B |   rate_C |   position_consistency |   flip_rate |   biased_responses |   non_unknown_responses |
|:--------------|:-----------|-----:|-----------:|---------------------:|-------------------------:|---------------:|-------------------------:|--------:|--------:|---------:|---------:|---------:|-----------------------:|------------:|-------------------:|------------------------:|
| regionality   | en         | 2160 |     0.8935 |               0.7944 |                   0.9926 |         0.3981 |                   0.7944 |  0.0167 |  0.0889 |   0.3722 |   0.3375 |   0.2903 |                 0.8014 |      0.1986 |                707 |                    1300 |
| regionality   | pt         | 2160 |     0.8796 |               0.7704 |                   0.9889 |         0.3861 |                   0.7704 |  0.0130 | -0.0056 |   0.3560 |   0.2556 |   0.3884 |                 0.7250 |      0.2750 |                667 |                    1326 |
| religion      | en         | 2160 |     0.8931 |               0.7981 |                   0.9880 |         0.4023 |                   0.7981 |  0.0103 | -0.0333 |   0.3838 |   0.3259 |   0.2903 |                 0.7833 |      0.2167 |                633 |                    1291 |
| religion      | pt         | 2160 |     0.9056 |               0.8241 |                   0.9870 |         0.4144 |                   0.8241 |  0.0251 |  0.0204 |   0.3454 |   0.2718 |   0.3829 |                 0.7778 |      0.2222 |                657 |                    1265 |

## Paired differences

| category_id   |   accuracy_pt |   unknown_rate_pt |   s_DIS_pt |   s_AMB_pt |   rate_A_pt |   rate_B_pt |   rate_C_pt |   accuracy_en |   unknown_rate_en |   s_DIS_en |   s_AMB_en |   rate_A_en |   rate_B_en |   rate_C_en |   accuracy_diff_pt_minus_en |   unknown_rate_diff_pt_minus_en |   s_DIS_diff_pt_minus_en |   s_AMB_diff_pt_minus_en |   rate_A_diff_pt_minus_en |   rate_B_diff_pt_minus_en |   rate_C_diff_pt_minus_en |   paired_evaluations |   semantic_agreement |   semantic_change_rate |   letter_agreement |
|:--------------|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|----------------------------:|--------------------------------:|-------------------------:|-------------------------:|--------------------------:|--------------------------:|--------------------------:|---------------------:|---------------------:|-----------------------:|-------------------:|
| regionality   |        0.8796 |            0.3861 |     0.0130 |    -0.0056 |      0.3560 |      0.2556 |      0.3884 |        0.8935 |            0.3981 |     0.0167 |     0.0889 |      0.3722 |      0.3375 |      0.2903 |                     -0.0139 |                         -0.0120 |                  -0.0037 |                  -0.0944 |                   -0.0162 |                   -0.0819 |                    0.0981 |                 2160 |               0.8366 |                 0.1634 |             0.8366 |
| religion      |        0.9056 |            0.4144 |     0.0251 |     0.0204 |      0.3454 |      0.2718 |      0.3829 |        0.8931 |            0.4023 |     0.0103 |    -0.0333 |      0.3838 |      0.3259 |      0.2903 |                      0.0125 |                          0.0120 |                   0.0149 |                   0.0537 |                   -0.0384 |                   -0.0542 |                    0.0926 |                 2160 |               0.8602 |                 0.1398 |             0.8602 |

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
