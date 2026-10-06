import numpy as np
import pandas as pd

def add_calendar_features(df, timestamp_col="timestamp"):
    x = df.copy()
    t = pd.to_datetime(x[timestamp_col])
    x["hour_sin"] = np.sin(2*np.pi*t.dt.hour/24)
    x["hour_cos"] = np.cos(2*np.pi*t.dt.hour/24)
    x["dow_sin"] = np.sin(2*np.pi*t.dt.dayofweek/7)
    x["dow_cos"] = np.cos(2*np.pi*t.dt.dayofweek/7)
    x["month"] = t.dt.month
    x["weekend"] = (t.dt.dayofweek >= 5).astype(int)
    return x

def add_energy_history(df, value_col="energy_kwh",
                       lags=(1,2,3,24,48,168),
                       rolling=(6,24,168)):
    x = df.copy()
    for lag in lags:
        x[f"{value_col}_lag_{lag}"] = x[value_col].shift(lag)
    for w in rolling:
        hist = x[value_col].shift(1)
        x[f"{value_col}_mean_{w}"] = hist.rolling(w).mean()
        x[f"{value_col}_std_{w}"] = hist.rolling(w).std()
    return x
