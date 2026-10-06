"""Figure 6 reproduction entry point.

Reproduces the calibration-strategy comparison, reading
`results/calibration_strategy_summary.csv`.
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


def main():
    df = pd.read_csv(ROOT / "results" / "calibration_strategy_summary.csv")

    fig, ax1 = plt.subplots(figsize=(8, 4))
    x = range(len(df))
    ax1.bar([i - 0.2 for i in x], df["picp_pct"], 0.4, label="PICP (%)", color="#c0392b")
    ax1.axhline(90.0, ls="--", c="grey", lw=1)
    ax1.set_ylabel("PICP (%)")
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(df["method"], rotation=15, ha="right", fontsize=8)

    ax2 = ax1.twinx()
    ax2.bar([i + 0.2 for i in x], df["pinaw"], 0.4, label="PINAW", color="#2980b9")
    ax2.set_ylabel("PINAW")

    ax1.set_title("Calibration strategy comparison")
    fig.tight_layout()
    out = OUT / "fig6.png"
    fig.savefig(out, dpi=200)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
