# GBC-BEP Research Archive

This repository accompanies the revised manuscript:

**Granular Ball Computing-Based Building Energy Consumption Prediction:
A Multi-Granularity Adaptive Framework for Handling Uncertainty and Heterogeneous Data**

Archive status: **Consolidated research archive; source materials retain their original validation status.**

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

## Public and restricted materials

### Publicly reproducible
- GBC-BEP reference implementation.
- Configuration files, random seeds, and chronological split definitions.
- EnergyPlus-SIM synthetic reconstruction: five IDFs, hourly schedules, Chicago-like EPW, 43,800-row benchmark, and validation scripts.
- Baseline and closest-representation comparison configurations.
- Statistical-analysis scripts.
- Figure-generation entry points.
- Numerical summary tables supplied with the revised manuscript.
- Anonymized CAMPUS-REAL building identifiers and building types.
- Prediction-file schemas and an export utility.

### Restricted
The raw CAMPUS-REAL records contain building-operation, BMS, and occupancy-related information and are not included in this public archive.

The exact original EnergyPlus IDF/EPW/schedule payloads and raw CAMPUS-REAL records were not present in the supplied workspace. For computational reproduction, this package contains **explicitly labeled synthetic reconstructions** of the missing EnergyPlus inputs and CAMPUS-REAL prediction arrays. These files reproduce the public schema, counts and reported numerical targets but are not substitutes for the original empirical/simulation artifacts in claims of exact data provenance.

## Recommended release workflow

1. Run `python validate_release.py`.
2. Replace all items reported as `REQUIRED_BEFORE_RELEASE`.
3. Run the final experiments and export timestamp-level prediction files.
4. Upload the repository to GitHub.
5. Create a versioned Zenodo release and obtain a DOI.
6. Replace `REPOSITORY_URL_TO_BE_ASSIGNED` and `ZENODO_DOI_TO_BE_ASSIGNED` in the manuscript and response letter.

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

The code in `src/` is a transparent reference implementation of the mathematical definitions in the revised manuscript. Dataset-specific loaders and the original private CAMPUS-REAL source files must be supplied by the authors' institutional pipeline.

## License

MIT license for code in this release candidate. Dataset licensing and institutional data-use restrictions remain separate.

## Archive documentation

See `ARCHIVE_GUIDE.md` for scope and provenance, `archive_manifest.csv` for source-file mappings and SHA-256 digests, and `SHA256SUMS.txt` for archive integrity checks.
