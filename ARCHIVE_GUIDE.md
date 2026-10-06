# GBC-BEP Research Archive

## Scope / 适用范围

This archive consolidates the companion materials for the revised manuscript. Directory structure, file names and path references have been normalized; data values and source documentation are retained.

The archive documents the computational workflow, configuration and numerical summaries reported in the revised manuscript. Reported validation results are those supplied with the submission. Consultation of the per-dataset README and provenance files is recommended for dataset-specific terms of use.

## Contents

- `campus_dataset/`: campus time series and alignment audits.
- `campus_real_metadata/`: building metadata and diagnostics.
- `predictions/`, `baseline_predictions/`: prediction arrays.
- `bdg2/`: six-site benchmark material and audits.
- `energyplus/`: model inputs, weather, schedules and benchmark assets.
- `src/`, `scripts/`, `configs/`: implementation and configuration.
- `results/`: numerical summaries.

## Packaging

Identical repeated files were merged. Python bytecode caches were omitted. Human-readable file references were updated to match renamed files; computational logic was retained. Source filenames remain in `archive_manifest.csv` for traceability. `SHA256SUMS.txt` covers every packaged file except itself.
