# Release status

## READY
- manuscript equations and key hyperparameter configuration
- GBC-BEP core reference modules
- block-conformal calibration implementation
- baseline summary tables
- closest-representation summary tables
- building-level MAPE table used for non-parametric statistics
- calibration / coverage / ACF numerical summaries
- statistical-analysis scripts
- building metadata (anonymized IDs and functional types)
- prediction-file schemas
- figure entry-point scripts

## REQUIRED_BEFORE_RELEASE
1. Actual EnergyPlus IDF model files.
2. Actual EPW weather files and final schedule inputs used in EnergyPlus-SIM.
3. Final timestamp-level CAMPUS-REAL predictions for B01-B23.
4. Exact private-data feature dictionary if the current institutional data dictionary contains additional fields not represented by the public feature-group schema.
5. Final GitHub URL.
6. Final Zenodo DOI.
7. Run the complete archive from a clean environment and store the resulting checksums.

No placeholder file should be represented to reviewers as an archived experimental artifact until it has been replaced with the corresponding real output.
