import pandas as pd
from scipy.stats import friedmanchisquare, rankdata
import argparse

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default="results/per_building_mape.csv")
    p.add_argument("--methods", nargs="+",
                   default=["GBC-BEP","GMM","iTransformer","K-means","PatchTST","Mahalanobis-KNN","TFT"])
    args = p.parse_args()
    df = pd.read_csv(args.csv)
    arrays = [df[m].to_numpy() for m in args.methods]
    stat, pval = friedmanchisquare(*arrays)
    ranks = df[args.methods].rank(axis=1, method="average")
    print(f"Friedman chi2={stat:.6f}, p={pval:.6g}")
    print("Average ranks:")
    print(ranks.mean().sort_values())

if __name__ == "__main__":
    main()
