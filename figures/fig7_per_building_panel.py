"""Figure 7 reproduction entry point (per-building panel).

Produces the per-building panel of Figure 7 from `results/per_building_mape.csv`,
writing to `figures/fig7_per_building_panel.png`.
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


def main():
    df = pd.read_csv(ROOT / "results" / "per_building_mape.csv")
    best_cols = ["TFT", "PatchTST", "iTransformer", "K-means", "GMM", "Mahalanobis-KNN"]
    best_cols = [c for c in best_cols if c in df.columns]
    df["Best baseline"] = df[best_cols].min(axis=1)
    ax = df.plot(x="Building", y=["GBC-BEP", "Best baseline"], kind="bar", figsize=(12, 5))
    ax.set_ylabel("MAPE (%)")
    ax.set_xlabel("Building")
    plt.tight_layout()
    out = OUT / "fig7_per_building_panel.png"
    plt.savefig(out, dpi=300)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
