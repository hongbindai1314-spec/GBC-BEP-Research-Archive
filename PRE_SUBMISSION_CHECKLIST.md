# Pre-submission reproducibility checklist

- [ ] Replace `REPOSITORY_URL_TO_BE_ASSIGNED`.
- [ ] Replace `ZENODO_DOI_TO_BE_ASSIGNED`.
- [ ] Add final EnergyPlus IDF files.
- [ ] Add final EPW weather files.
- [ ] Add final EnergyPlus schedules and simulation configuration.
- [ ] Export B01-B23 timestamp-level predictions.
- [ ] Verify `y_true`, `y_pred`, `lower_90`, and `upper_90` columns.
- [ ] Confirm the final model outputs RMSE = 56.8 ± 4.6 kWh, MAE = 40.5 ± 3.4 kWh, MAPE = 12.1 ± 1.5% on CAMPUS-REAL.
- [ ] Confirm final PICP = 90.5% and PINAW = 0.319.
- [ ] Re-run building-level Friedman and Holm-adjusted Wilcoxon tests.
- [ ] Re-run figure scripts from archived outputs.
- [ ] Run `python validate_release.py`.
- [ ] Generate checksums with `python make_checksums.py`.
- [ ] Tag release `v1.0.0`.
- [ ] Upload release to Zenodo and insert DOI into manuscript and response letter.
