import pandas as pd

def aggregate_hourly(df, timestamp_col="timestamp",
                     sum_cols=("energy_kwh",),
                     mean_cols=(),
                     mode_cols=()):
    x = df.copy()
    x[timestamp_col] = pd.to_datetime(x[timestamp_col])
    x = x.set_index(timestamp_col).sort_index()
    parts = {}
    for c in sum_cols:
        if c in x:
            parts[c] = x[c].resample("1h").sum(min_count=1)
    for c in mean_cols:
        if c in x:
            parts[c] = x[c].resample("1h").mean()
    for c in mode_cols:
        if c in x:
            parts[c] = x[c].resample("1h").agg(
                lambda s: s.mode().iloc[0] if not s.mode().empty else None
            )
    return pd.DataFrame(parts)
