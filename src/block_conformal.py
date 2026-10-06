from collections import defaultdict
import numpy as np
import pandas as pd

class BuildingHorizonBlockConformal:
    """
    Chronological 24-h blocked, building- and horizon-specific calibration.
    This implementation does not claim classical exchangeable finite-sample
    conformal guarantees for temporally dependent building-energy data.
    """
    def __init__(self, nominal_coverage=0.90, block_spacing_hours=24, eps=1e-8):
        self.nominal_coverage = nominal_coverage
        self.alpha = 1.0 - nominal_coverage
        self.block_spacing_hours = block_spacing_hours
        self.eps = eps
        self.quantiles_ = {}

    def fit(self, df):
        req = {"building_id","forecast_origin","horizon","y_true","y_pred","U_raw"}
        missing = req - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {sorted(missing)}")
        data = df.copy()
        data["forecast_origin"] = pd.to_datetime(data["forecast_origin"])
        # non-overlapping forecast origins within each building
        for (b,h), g in data.groupby(["building_id","horizon"]):
            g = g.sort_values("forecast_origin")
            selected = []
            last = None
            for _, row in g.iterrows():
                t = row["forecast_origin"]
                if last is None or (t-last).total_seconds()/3600 >= self.block_spacing_hours:
                    selected.append(row)
                    last = t
            if not selected:
                continue
            z = pd.DataFrame(selected)
            scores = np.abs(z["y_true"].to_numpy() - z["y_pred"].to_numpy()) / (
                np.sqrt(np.clip(z["U_raw"].to_numpy(), 0, None)) + self.eps
            )
            self.quantiles_[(b,int(h))] = float(
                np.quantile(scores, 1-self.alpha, method="higher")
            )
        return self

    def interval(self, building_id, horizon, y_pred, U_raw):
        q = self.quantiles_[(building_id, int(horizon))]
        half = q * np.sqrt(max(float(U_raw), 0.0))
        return float(y_pred-half), float(y_pred+half)
