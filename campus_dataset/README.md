# Campus Dataset

Archived campus time series and alignment audits released with the revised manuscript. The full raw institutional records remain restricted; the material here supports code and pipeline reproduction.

- `raw_15min/`: B01-B23, 2020-2022, 105,216 rows/building, 28 manuscript-aligned variables plus timestamp.
- `hourly/`: B01-B23, 26,304 rows/building after hourly aggregation semantics.
- Jul-Dec 2022 electricity values are aligned to the archived `predictions/B01-B23` target series wherever those target timestamps are present.
- `audits/`: row-count and test-target alignment checks.
