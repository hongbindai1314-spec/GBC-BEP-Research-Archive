from pathlib import Path
import csv,re,hashlib
ROOT=Path(__file__).resolve().parent
issues=[]
epw=ROOT/'weather'/'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw'
if sum(1 for _ in epw.open(encoding='utf-8'))!=8768: issues.append('EPW must contain 8 header + 8760 data lines')
for f in sorted((ROOT/'schedules').glob('EP??_*_schedulefile.csv')):
    if sum(1 for _ in f.open())!=8760: issues.append(f'{f.name}: expected 8760 rows')
for f in sorted((ROOT/'models').glob('EP??_*.idf')):
    t=f.read_text(encoding='utf-8')
    if 'SYNTHETIC RECONSTRUCTION' not in t: issues.append(f'{f.name}: provenance marker missing')
    if 'Schedule:File' not in t: issues.append(f'{f.name}: schedule references missing')
if len(list((ROOT/'models').glob('EP??_*.idf')))!=5: issues.append('expected 5 IDFs')
print('EnergyPlus synthetic artifact check:', 'PASS' if not issues else 'FAIL')
for x in issues: print('-',x)
raise SystemExit(1 if issues else 0)
