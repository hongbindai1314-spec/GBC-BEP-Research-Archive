# Campus Timestamp-Level Predictions

`B01_predictions.csv` through `B23_predictions.csv` contain deterministic synthetic/reconstructed values generated for reproducibility testing. They follow the manuscript schema and test-calendar size, but they are **not original CAMPUS-REAL measurements or final experimental exports**.

Required columns:
`building_id,timestamp,forecast_origin,horizon,y_true,y_pred,lower_90,upper_90,U_within,U_between,U_raw`

Use these files to exercise the code, regenerate diagnostics, and test figure/table pipelines. Do not cite them as institutional observations.
