# Brazil-specific analysis: Regionality and Religion

> Do not interpret these results as validated claims about Brazilian groups.
> Items marked for human review remain exploratory.

This section separates social-content direction (`s_DIS`, `s_AMB`) from option
position behavior (`position_consistency`, `flip_rate`, and A/B/C rates).

## PT versus EN metrics

| category_id   | language   |    n |   accuracy |   accuracy_ambiguous |   accuracy_disambiguated |   unknown_rate |   unknown_rate_ambiguous |   s_DIS |   s_AMB |   rate_A |   rate_B |   rate_C |   position_consistency |   flip_rate |   biased_responses |   non_unknown_responses |
|:--------------|:-----------|-----:|-----------:|---------------------:|-------------------------:|---------------:|-------------------------:|--------:|--------:|---------:|---------:|---------:|-----------------------:|------------:|-------------------:|------------------------:|
| regionality   | en         | 2160 |     0.9829 |               0.9676 |                   0.9981 |         0.4847 |                   0.9676 |  0.0093 |  0.0250 |   0.3403 |   0.3370 |   0.3227 |                 0.9611 |      0.0389 |                575 |                    1113 |
| regionality   | pt         | 2160 |     0.9944 |               0.9917 |                   0.9972 |         0.4963 |                   0.9917 |  0.0120 |  0.0028 |   0.3366 |   0.3338 |   0.3296 |                 0.9833 |      0.0167 |                552 |                    1088 |
| religion      | en         | 2160 |     0.9912 |               0.9861 |                   0.9963 |         0.4949 |                   0.9861 |  0.0093 |  0.0083 |   0.3403 |   0.3338 |   0.3259 |                 0.9750 |      0.0250 |                555 |                    1091 |
| religion      | pt         | 2160 |     0.9898 |               0.9861 |                   0.9935 |         0.4963 |                   0.9861 |  0.0065 |  0.0028 |   0.3366 |   0.3356 |   0.3278 |                 0.9750 |      0.0250 |                549 |                    1088 |

## Paired differences

| category_id   |   accuracy_pt |   unknown_rate_pt |   s_DIS_pt |   s_AMB_pt |   rate_A_pt |   rate_B_pt |   rate_C_pt |   accuracy_en |   unknown_rate_en |   s_DIS_en |   s_AMB_en |   rate_A_en |   rate_B_en |   rate_C_en |   accuracy_diff_pt_minus_en |   unknown_rate_diff_pt_minus_en |   s_DIS_diff_pt_minus_en |   s_AMB_diff_pt_minus_en |   rate_A_diff_pt_minus_en |   rate_B_diff_pt_minus_en |   rate_C_diff_pt_minus_en |   paired_evaluations |   semantic_agreement |   semantic_change_rate |   letter_agreement |
|:--------------|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|----------------------------:|--------------------------------:|-------------------------:|-------------------------:|--------------------------:|--------------------------:|--------------------------:|---------------------:|---------------------:|-----------------------:|-------------------:|
| regionality   |        0.9944 |            0.4963 |     0.0120 |     0.0028 |      0.3366 |      0.3338 |      0.3296 |        0.9829 |            0.4847 |     0.0093 |     0.0250 |      0.3403 |      0.3370 |      0.3227 |                      0.0116 |                          0.0116 |                   0.0028 |                  -0.0222 |                   -0.0037 |                   -0.0032 |                    0.0069 |                 2160 |               0.9801 |                 0.0199 |             0.9801 |
| religion      |        0.9898 |            0.4963 |     0.0065 |     0.0028 |      0.3366 |      0.3356 |      0.3278 |        0.9912 |            0.4949 |     0.0093 |     0.0083 |      0.3403 |      0.3338 |      0.3259 |                     -0.0014 |                          0.0014 |                  -0.0028 |                  -0.0056 |                   -0.0037 |                    0.0019 |                    0.0019 |                 2160 |               0.9838 |                 0.0162 |             0.9838 |

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
