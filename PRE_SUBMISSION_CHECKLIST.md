# Pre-submission reproducibility checklist

- [ ] Insert the final repository URL.
- [ ] Insert the final Zenodo DOI.
- [ ] Verify `y_true`, `y_pred`, `lower_90`, and `upper_90` columns in the prediction exports.
- [ ] Confirm the model outputs RMSE = 56.8 ± 4.6 kWh, MAE = 40.5 ± 3.4 kWh, MAPE = 12.1 ± 1.5% on CAMPUS-REAL.
- [ ] Confirm PICP = 90.5% and PINAW = 0.319.
- [ ] Re-run building-level Friedman and Holm-adjusted Wilcoxon tests.
- [ ] Re-run figure scripts from archived outputs.
- [ ] Run `python validate_release.py`.
- [ ] Generate checksums with `python make_checksums.py`.
- [ ] Tag release `v1.0.0`.
- [ ] Upload release to Zenodo and insert the DOI into the manuscript and response letter.
