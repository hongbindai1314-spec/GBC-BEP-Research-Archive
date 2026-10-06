import argparse
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

def holm_adjust(pvals):
    m = len(pvals)
    order = np.argsort(pvals)
    adj = np.empty(m, float)
    running = 0.0
    for rank, idx in enumerate(order):
        val = (m-rank) * pvals[idx]
        running = max(running, val)
        adj[idx] = min(running, 1.0)
    return adj

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default="results/per_building_mape.csv")
    p.add_argument("--reference", default="GBC-BEP")
    p.add_argument("--comparators", nargs="+",
                   default=["GMM","iTransformer","K-means","PatchTST","Mahalanobis-KNN","TFT"])
    args = p.parse_args()
    df = pd.read_csv(args.csv)
    raw = []
    rows = []
    for m in args.comparators:
        res = wilcoxon(df[args.reference], df[m], alternative="two-sided",
                       zero_method="wilcox", method="auto")
        raw.append(res.pvalue)
        rows.append([m, res.statistic, res.pvalue])
    adj = holm_adjust(np.asarray(raw))
    for row, pa in zip(rows, adj):
        print(f"{args.reference} vs {row[0]}: W={row[1]}, p={row[2]:.6g}, Holm={pa:.6g}")

if __name__ == "__main__":
    main()
