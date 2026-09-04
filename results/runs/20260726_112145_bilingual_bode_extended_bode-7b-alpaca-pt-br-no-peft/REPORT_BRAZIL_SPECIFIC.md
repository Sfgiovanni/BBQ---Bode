# Brazil-specific analysis: Regionality and Religion

> Do not interpret these results as validated claims about Brazilian groups.
> Items marked for human review remain exploratory.

This section separates social-content direction (`s_DIS`, `s_AMB`) from option
position behavior (`position_consistency`, `flip_rate`, and A/B/C rates).

## PT versus EN metrics

| category_id   | language   |    n |   accuracy |   accuracy_ambiguous |   accuracy_disambiguated |   unknown_rate |   unknown_rate_ambiguous |   s_DIS |   s_AMB |   rate_A |   rate_B |   rate_C |   position_consistency |   flip_rate |   biased_responses |   non_unknown_responses |
|:--------------|:-----------|-----:|-----------:|---------------------:|-------------------------:|---------------:|-------------------------:|--------:|--------:|---------:|---------:|---------:|-----------------------:|------------:|-------------------:|------------------------:|
| regionality   | en         | 2160 |     0.4352 |               0.0620 |                   0.8083 |         0.0745 |                   0.0620 | -0.0284 | -0.0139 |   0.2056 |   0.4185 |   0.3759 |                 0.3972 |      0.6028 |                978 |                    1999 |
| regionality   | pt         | 2160 |     0.3764 |               0.0009 |                   0.7519 |         0.0213 |                   0.0009 | -0.0377 | -0.0046 |   0.1472 |   0.4731 |   0.3796 |                 0.2653 |      0.7347 |               1035 |                    2114 |
| religion      | en         | 2160 |     0.4301 |               0.0222 |                   0.8380 |         0.0389 |                   0.0222 |  0.0647 |  0.1537 |   0.3231 |   0.3722 |   0.3046 |                 0.4528 |      0.5472 |               1154 |                    2076 |
| religion      | pt         | 2160 |     0.3870 |               0.0417 |                   0.7324 |         0.0625 |                   0.0417 |  0.0848 |  0.1880 |   0.1829 |   0.5366 |   0.2806 |                 0.2847 |      0.7153 |               1156 |                    2025 |

## Paired differences

| category_id   |   accuracy_pt |   unknown_rate_pt |   s_DIS_pt |   s_AMB_pt |   rate_A_pt |   rate_B_pt |   rate_C_pt |   accuracy_en |   unknown_rate_en |   s_DIS_en |   s_AMB_en |   rate_A_en |   rate_B_en |   rate_C_en |   accuracy_diff_pt_minus_en |   unknown_rate_diff_pt_minus_en |   s_DIS_diff_pt_minus_en |   s_AMB_diff_pt_minus_en |   rate_A_diff_pt_minus_en |   rate_B_diff_pt_minus_en |   rate_C_diff_pt_minus_en |   paired_evaluations |   semantic_agreement |   semantic_change_rate |   letter_agreement |
|:--------------|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|--------------:|------------------:|-----------:|-----------:|------------:|------------:|------------:|----------------------------:|--------------------------------:|-------------------------:|-------------------------:|--------------------------:|--------------------------:|--------------------------:|---------------------:|---------------------:|-----------------------:|-------------------:|
| regionality   |        0.3764 |            0.0213 |    -0.0377 |    -0.0046 |      0.1472 |      0.4731 |      0.3796 |        0.4352 |            0.0745 |    -0.0284 |    -0.0139 |      0.2056 |      0.4185 |      0.3759 |                     -0.0588 |                         -0.0532 |                  -0.0093 |                   0.0093 |                   -0.0583 |                    0.0546 |                    0.0037 |                 2160 |               0.7472 |                 0.2528 |             0.7472 |
| religion      |        0.3870 |            0.0625 |     0.0848 |     0.1880 |      0.1829 |      0.5366 |      0.2806 |        0.4301 |            0.0389 |     0.0647 |     0.1537 |      0.3231 |      0.3722 |      0.3046 |                     -0.0431 |                          0.0236 |                   0.0201 |                   0.0343 |                   -0.1403 |                    0.1644 |                   -0.0241 |                 2160 |               0.7019 |                 0.2981 |             0.7019 |

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
