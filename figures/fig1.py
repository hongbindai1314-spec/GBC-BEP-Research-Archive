"""Figure 1 reproduction entry point.

Reproduces the archived building-level MAPE comparison across GBC-BEP and the
comparison methods, reading `results/per_building_mape.csv`.
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
    methods = [c for c in df.columns if c not in ("Building", "Type")]

    fig, ax = plt.subplots(figsize=(10, 4.5))
    x = range(len(df))
    width = 0.8 / len(methods)
    for i, m in enumerate(methods):
        ax.bar([p + i * width for p in x], df[m], width, label=m)
    ax.set_xticks([p + 0.4 - width / 2 for p in x])
    ax.set_xticklabels(df["Building"], rotation=90, fontsize=7)
    ax.set_ylabel("MAPE (%)")
    ax.set_xlabel("Building")
    ax.set_title("Building-level MAPE by method (CAMPUS-REAL)")
    ax.legend(fontsize=7, ncol=4)
    fig.tight_layout()
    out = OUT / "fig1.png"
    fig.savefig(out, dpi=200)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
