from pathlib import Path
import argparse, subprocess, shutil

ROOT=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--energyplus', default=shutil.which('energyplus'), help='Path to EnergyPlus executable')
    p.add_argument('--out-root', default=str(ROOT/'sim_outputs'))
    a=p.parse_args()
    if not a.energyplus:
        raise SystemExit('EnergyPlus executable not found. Install EnergyPlus or use benchmark/energyplus_sim_hourly_43800.csv directly.')
    epw=ROOT/'weather'/'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw'
    for idf in sorted((ROOT/'models').glob('EP??_*.idf')):
        out=Path(a.out_root)/idf.stem; out.mkdir(parents=True,exist_ok=True)
        subprocess.run([a.energyplus,'-w',str(epw),'-d',str(out),str(idf)],check=True,cwd=ROOT)
        print('completed',idf.name,'->',out)
if __name__=='__main__': main()
