"""Figure 8 reproduction entry point.

Reproduces the horizon- and month-resolved interval coverage profiles, reading
`results/horizon_coverage_summary.csv` and `results/monthly_coverage_summary.csv`.
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


def main():
    h = pd.read_csv(ROOT / "results" / "horizon_coverage_summary.csv")
    m = pd.read_csv(ROOT / "results" / "monthly_coverage_summary.csv")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(h["horizon_h"], h["picp_pct"], marker="o")
    axes[0].axhline(90.0, ls="--", c="grey", lw=1)
    axes[0].set_xlabel("Forecast horizon (h)")
    axes[0].set_ylabel("PICP (%)")
    axes[0].set_title("Coverage vs. horizon")

    axes[1].plot(m["month_2022"], m["picp_pct"], marker="s", color="#c0392b")
    axes[1].axhline(90.0, ls="--", c="grey", lw=1)
    axes[1].set_xlabel("Month (2022)")
    axes[1].set_ylabel("PICP (%)")
    axes[1].set_title("Coverage vs. month")

    fig.tight_layout()
    out = OUT / "fig8.png"
    fig.savefig(out, dpi=200)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
