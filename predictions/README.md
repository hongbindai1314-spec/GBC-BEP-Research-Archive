# Campus Timestamp-Level Predictions

`B01_predictions.csv` through `B23_predictions.csv` contain the timestamp-level prediction exports archived with the revised manuscript. They follow the manuscript schema and test-calendar size.

Required columns:
`building_id,timestamp,forecast_origin,horizon,y_true,y_pred,lower_90,upper_90,U_within,U_between,U_raw`

Use these files to exercise the code, regenerate diagnostics, and drive the figure/table pipelines.
