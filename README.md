# GBC-BEP Research Archive

This repository accompanies the revised manuscript:

**Granular Ball Computing-Based Building Energy Consumption Prediction:
A Multi-Granularity Adaptive Framework for Handling Uncertainty and Heterogeneous Data**

## Scope

The archive is organized to reproduce the computational workflow described in the revised manuscript:

1. chronological preprocessing and feature construction;
2. adaptive regression-oriented granular-ball construction;
3. Top-K Mahalanobis retrieval;
4. multi-ball query-dependent attention;
5. FusionNet point forecasting;
6. granule-based predictive-dispersion calculation;
7. 24-h blocked, building- and horizon-specific conformal calibration;
8. baseline, robustness, calibration, and statistical analyses.

## Contents

### Released in this archive
- GBC-BEP reference implementation.
- Configuration files, random seeds, and chronological split definitions.
- EnergyPlus-SIM assets: five IDFs, hourly schedules, Chicago O'Hare TMY3-format EPW, 43,800-row benchmark, and validation scripts.
- Baseline and closest-representation comparison configurations.
- Statistical-analysis scripts.
- Figure-generation entry points.
- Numerical summary tables from the revised manuscript.
- Anonymized CAMPUS-REAL building identifiers and building types.
- Prediction-file schemas and an export utility.

### Restricted
The raw CAMPUS-REAL records contain building-operation, BMS, and occupancy-related information. Access is governed by institutional data-use terms; the anonymized and derived products in this archive are released in their place.

## Release workflow

1. Run `python validate_release.py`.
2. Run the final experiments and export timestamp-level prediction files.
3. Upload the repository to GitHub.
4. Create a versioned Zenodo release and obtain a DOI.
5. Insert the repository URL and Zenodo DOI into the manuscript and response letter.

## Environment

The manuscript reports:
- Python 3.9
- PyTorch 2.0
- scikit-learn 1.3
- Optuna
- NumPy / pandas / SciPy
- Matplotlib
- Hardware: dual Intel Xeon Gold 6248R, 512 GB RAM, four NVIDIA A100 40 GB GPUs.

See `environment.yml` and `requirements.txt`.

## Data splits

See `configs/data_splits.yaml` and `campus_real_metadata/split_timestamps.csv`.

## Reproduction notes

The code in `src/` is a transparent reference implementation of the mathematical definitions in the revised manuscript. Dataset-specific loaders and the full CAMPUS-REAL source records are available through the authors' institutional pipeline under the applicable data-use terms.

## License

MIT license for code in this release. Dataset licensing and institutional data-use restrictions remain separate.

## Archive documentation

See `ARCHIVE_GUIDE.md` for scope, `archive_manifest.csv` for source-file mappings and SHA-256 digests, and `SHA256SUMS.txt` for archive integrity checks.
