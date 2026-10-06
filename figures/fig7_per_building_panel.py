import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv("results/per_building_mape.csv")
    best_cols = ["TFT","PatchTST","iTransformer","K-means","GMM","Mahalanobis-KNN"]
    df["Best baseline"] = df[best_cols].min(axis=1)
    ax = df.plot(x="Building", y=["GBC-BEP","Best baseline"], kind="bar", figsize=(12,5))
    ax.set_ylabel("MAPE (%)")
    ax.set_xlabel("Building")
    plt.tight_layout()
    plt.savefig("outputs/fig7_per_building_panel.png", dpi=300)

if __name__ == "__main__":
    main()
