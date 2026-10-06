"""Figure 2 reproduction entry point.

Reproduces the CAMPUS-REAL baseline comparison of point-error metrics, reading
`results/campus_real_complete_baselines.csv`.
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


def main():
    df = pd.read_csv(ROOT / "results" / "campus_real_complete_baselines.csv")

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, col, label in zip(
        axes,
        ["rmse_mean", "mae_mean", "mape_mean_pct"],
        ["RMSE (kWh)", "MAE (kWh)", "MAPE (%)"],
    ):
        ax.barh(df["method"], df[col])
        ax.set_xlabel(label)
        ax.invert_yaxis()
    fig.suptitle("CAMPUS-REAL baseline comparison")
    fig.tight_layout()
    out = OUT / "fig2.png"
    fig.savefig(out, dpi=200)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
