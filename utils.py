import numpy as np

def safe_get(df, field):
    try:
        series = df.loc[field].dropna()
        if series.empty:
            return None
        return series
    except KeyError:
        return None

def valid(series, min_years=1):
    return series is not None and len(series) >= min_years

def last_n(series, n):
    return series.iloc[:n]

def avg(series, n):
    return last_n(series, n).mean()

def trend_up(series, n):
    s = last_n(series, n)
    return all(x < y for x, y in zip(s[::-1][:-1], s[::-1][1:]))

def mostly_present(series, n, threshold=0.6):
    s = last_n(series, n)
    return len(s) / n >= threshold
