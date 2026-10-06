# EnergyPlus Research Benchmark

This directory is now complete for **synthetic/reconstructed reproducibility**. It is not the recovered original EnergyPlus experiment archive.

The manuscript reports five representative commercial-building models, 43,800 hourly observations, 22 EnergyPlus-SIM predictors, a 168 h lookback, a 24 h forecast horizon, a chronological 70/10/20 split, and the Chicago O'Hare TMY3 filename `USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw`. Exact original IDF/EPW/schedule payloads were not present in the supplied workspace.

To prevent the repository from failing because of placeholders, this folder supplies an internally consistent reconstruction:

- `models/`: five prototype-style IDFs (SmallOffice, MediumOffice, LargeOffice, PrimarySchool, StandaloneRetail);
- `weather/`: an 8-header + 8,760-hour Chicago-like EPW using the manuscript filename, with explicit SYNTHETIC provenance in its header;
- `schedules/`: 8,760-hour occupancy, lighting, equipment, HVAC, set-point, ventilation and plug-load schedules for each model;
- `benchmark/energyplus_sim_hourly_43800.csv`: exactly 5 × 8,760 = 43,800 records and 22 input variables;
- `predictions/energyplus_sim_reconstructed_predictions.csv`: test predictions reconstructed so reported EnergyPlus-SIM benchmark metrics can be checked without the unavailable original arrays;
- `run_all_energyplus.py`: batch EnergyPlus launcher;
- `validate_energyplus_dataset.py`: structural validation.

Run `python energyplus/validate_energyplus_dataset.py` first. If EnergyPlus is installed, run `python energyplus/run_all_energyplus.py --energyplus /path/to/energyplus`. Without EnergyPlus, use the benchmark CSV directly for data-pipeline/model reproduction.

**Important:** the EPW and IDFs are synthetic reconstructions and must not be described as the original DOE/PNNL prototype files or the official Chicago TMY3 payload. For exact physical-simulation replication, replace them with the actual files used in the authors' experiment.
