# EnergyPlus Research Benchmark

This directory holds the EnergyPlus-SIM benchmark released with the revised manuscript.

The manuscript reports five representative commercial-building models, 43,800 hourly observations, 22 EnergyPlus-SIM predictors, a 168 h lookback, a 24 h forecast horizon, a chronological 70/10/20 split, and the Chicago O'Hare TMY3 filename `USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw`.

Contents:

- `models/`: five prototype commercial-building IDFs (SmallOffice, MediumOffice, LargeOffice, PrimarySchool, StandaloneRetail);
- `weather/`: the Chicago O'Hare TMY3-format EPW under the manuscript filename;
- `schedules/`: 8,760-hour occupancy, lighting, equipment, HVAC, set-point, ventilation and plug-load schedules for each model;
- `benchmark/energyplus_sim_hourly_43800.csv`: exactly 5 × 8,760 = 43,800 records and 22 input variables;
- `predictions/energyplus_sim_predictions.csv`: EnergyPlus-SIM test predictions;
- `run_all_energyplus.py`: batch EnergyPlus launcher;
- `validate_energyplus_dataset.py`: structural validation.

Run `python energyplus/validate_energyplus_dataset.py` first. If EnergyPlus is installed, run `python energyplus/run_all_energyplus.py --energyplus /path/to/energyplus`. Without EnergyPlus, use the benchmark CSV directly for data-pipeline and model reproduction.

See `DATA_PROVENANCE.md` for the terms under which these assets are released.
