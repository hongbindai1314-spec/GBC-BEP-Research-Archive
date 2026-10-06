from pathlib import Path
import csv
root=Path(__file__).resolve().parent
issues=[]
for d in [root/'energyplus/models',root/'energyplus/weather',root/'energyplus/schedules']:
    if not any(p.is_file() and p.suffix.lower() not in {'.md'} for p in d.iterdir()): issues.append(f'no data files in {d.relative_to(root)}')
for pred in sorted((root/'predictions').glob('B??_predictions.csv')):
    with pred.open(encoding='utf-8-sig') as f:
        n=sum(1 for _ in f)
    if n<=1: issues.append(f'{pred.name} contains schema only')
epw=root/'energyplus/weather/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw'
if not epw.exists() or sum(1 for _ in epw.open(encoding='utf-8'))!=8768: issues.append('synthetic EPW missing/invalid line count')
bm=root/'energyplus/benchmark/energyplus_sim_hourly_43800.csv'
if not bm.exists() or sum(1 for _ in bm.open(encoding='utf-8-sig'))!=43801: issues.append('43,800-row EnergyPlus benchmark missing')
if issues:
    print('\n'.join(issues)); raise SystemExit(1)
print('Synthetic reproduction validation passed. Provenance: reconstructed, not original experimental data.')
