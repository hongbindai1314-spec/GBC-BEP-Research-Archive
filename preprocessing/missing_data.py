import pandas as pd

def causal_fill(series, short_gap_limit=3, training_median=None):
    s = series.copy()
    # forward-only interpolation avoids use of future values
    s = s.interpolate(method="linear", limit=short_gap_limit,
                      limit_direction="forward")
    if training_median is not None:
        s = s.fillna(training_median)
    return s
