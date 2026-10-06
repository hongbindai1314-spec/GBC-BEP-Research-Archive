"""Figure 5 reproduction entry point.

Reproduces the interval-coverage / sharpness comparison of probabilistic baselines,
reading `results/probabilistic_interval_summary.csv`.
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


def main():
    df = pd.read_csv(ROOT / "results" / "probabilistic_interval_summary.csv")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(df["pinaw"], df["picp_pct"], s=60)
    for _, r in df.iterrows():
        ax.annotate(r["method"], (r["pinaw"], r["picp_pct"]), fontsize=8,
                    xytext=(4, 4), textcoords="offset points")
    ax.axhline(90.0, ls="--", c="grey", lw=1)
    ax.set_xlabel("PINAW (lower is sharper)")
    ax.set_ylabel("PICP (%)")
    ax.set_title("Probabilistic interval summary")
    fig.tight_layout()
    out = OUT / "fig5.png"
    fig.savefig(out, dpi=200)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
