import argparse
import pandas as pd
import numpy as np

def metrics(df):
    cover = ((df["y_true"] >= df["lower_90"]) &
             (df["y_true"] <= df["upper_90"])).mean()*100
    denom = df["y_true"].max()-df["y_true"].min()
    pinaw = (df["upper_90"]-df["lower_90"]).mean()/denom
    return cover, pinaw

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    args = p.parse_args()
    df = pd.read_csv(args.csv)
    p_all, w_all = metrics(df)
    print(f"Overall PICP={p_all:.3f}%, PINAW={w_all:.6f}")
    for h,g in df.groupby("horizon"):
        p,w=metrics(g)
        print(f"h={h}: PICP={p:.3f}%, PINAW={w:.6f}")

if __name__ == "__main__":
    main()
