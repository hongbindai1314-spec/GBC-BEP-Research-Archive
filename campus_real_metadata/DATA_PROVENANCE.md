# SYNTHETIC CAMPUS-REAL REPRODUCTION DATA

These files are deterministic **synthetic/reconstructed data for software and result-reproduction testing**. They are **not** the original CAMPUS-REAL measurements and must not be described or deposited as measured campus BMS/occupancy data.

Generation seed: 20260912

The reconstruction follows the manuscript's public constraints: 23 anonymized buildings, approximately 287,000 m2 total floor area, the reported functional-type composition, July--December 2022 held-out period, 4,380 valid 24-h forecast origins per building, and 2,417,760 scalar building-origin-horizon prediction rows. Point-error magnitudes, building difficulty, empirical interval coverage and interval sharpness are calibrated to the manuscript's reported aggregate scale.

Because rounded manuscript summaries contain small internal inconsistencies, the generator prioritizes the headline CAMPUS-REAL results (RMSE 56.8 kWh, MAE 40.5 kWh, micro-MAPE 12.1%, CV-RMSE about 19.8%, PICP 90.5%, PINAW about 0.319) while preserving the relative building patterns in the supplied summary tables.

Raw CAMPUS-REAL data remain restricted and are not reconstructed here.
