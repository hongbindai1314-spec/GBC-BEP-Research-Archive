from pathlib import Path
import pandas as pd
import argparse

REQUIRED = [
    "building_id","timestamp","forecast_origin","horizon",
    "y_true","y_pred","lower_90","upper_90",
    "U_within","U_between","U_raw"
]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True,
                   help="Final combined experiment-output CSV")
    p.add_argument("--outdir", default="predictions")
    args = p.parse_args()
    df = pd.read_csv(args.input)
    miss = [c for c in REQUIRED if c not in df.columns]
    if miss:
        raise SystemExit(f"Missing required columns: {miss}")
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    for b, g in df.groupby("building_id"):
        g[REQUIRED].to_csv(out/f"{b}_predictions.csv", index=False)

if __name__ == "__main__":
    main()
