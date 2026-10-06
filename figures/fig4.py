"""Figure 4 reproduction entry point.

Reproduces the predictive-dispersion / absolute-error rank correlation analysis,
reading `results/dispersion_error_correlation.csv`.
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


def main():
    df = pd.read_csv(ROOT / "results" / "dispersion_error_correlation.csv")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(df["indicator"], df["spearman_rho"])
    for i, v in enumerate(df["spearman_rho"]):
        ax.text(v + 0.005, i, f"{v:.3f}", va="center", fontsize=8)
    ax.set_xlabel("Spearman rho vs. absolute error")
    ax.set_xlim(0, max(df["spearman_rho"]) * 1.2)
    ax.set_title("Predictive-dispersion / error correlation")
    ax.invert_yaxis()
    fig.tight_layout()
    out = OUT / "fig4.png"
    fig.savefig(out, dpi=200)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
