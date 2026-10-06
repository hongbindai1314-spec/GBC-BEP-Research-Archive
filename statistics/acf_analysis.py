import argparse
import pandas as pd
from statsmodels.tsa.stattools import acf

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    p.add_argument("--column", default="nonconformity_score")
    p.add_argument("--nlags", type=int, default=168)
    args = p.parse_args()
    x = pd.read_csv(args.csv)[args.column].dropna().to_numpy()
    vals = acf(x, nlags=args.nlags, fft=True)
    for lag in [1,24,48,168]:
        if lag < len(vals):
            print(lag, vals[lag])

if __name__ == "__main__":
    main()
