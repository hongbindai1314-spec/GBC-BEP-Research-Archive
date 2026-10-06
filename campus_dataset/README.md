# Campus Dataset

These files are synthetic reconstructions for code and pipeline reproducibility only; they are not original institutional BMS/occupancy records.

- `raw_15min/`: B01-B23, 2020-2022, 105,216 rows/building, 28 manuscript-aligned variables plus timestamp.
- `hourly/`: B01-B23, 26,304 rows/building after hourly aggregation semantics.
- Jul-Dec 2022 electricity values are aligned to the synthetic `predictions/B01-B23` target series wherever those target timestamps are present.
- `audits/`: row-count and test-target alignment checks.
