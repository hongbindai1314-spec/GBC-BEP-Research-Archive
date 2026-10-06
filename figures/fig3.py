"""Figure 3 reproduction entry point.

Reproduces the ablated-variant comparison for the multi-ball fusion mechanism,
reading `results/multiball_fusion_ablation.csv`.
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


def main():
    df = pd.read_csv(ROOT / "results" / "multiball_fusion_ablation.csv")

    fig, ax = plt.subplots(figsize=(9, 4))
    x = range(len(df))
    w = 0.35
    ax.bar([i - w / 2 for i in x], df["rmse_mean"], w, yerr=df["rmse_std"], label="RMSE (kWh)")
    ax.bar([i + w / 2 for i in x], df["mae_mean"], w, yerr=df["mae_std"], label="MAE (kWh)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(df["variant"], rotation=15, ha="right", fontsize=8)
    ax.set_ylabel("Error (kWh)")
    ax.set_title("Multi-ball fusion ablation")
    ax.legend()
    fig.tight_layout()
    out = OUT / "fig3.png"
    fig.savefig(out, dpi=200)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
