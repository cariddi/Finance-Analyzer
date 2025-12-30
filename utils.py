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

def mostly_present(series, n, threshold=0.6):
    s = last_n(series, n)
    return len(s) / n >= threshold

def pct_changes(values):
    return [
        (b - a) / abs(a) if a not in (0, None) else None
        for a, b in zip(values[:-1], values[1:])
    ]

def trend_mostly_up(series, n, min_positive_ratio=0.6, min_total_growth=0.1):
    """
    min_total_growth = 0.1 means at least +10% over the period
    """

    s = last_n(series, n)
    s = [x for x in s if x is not None]

    if len(s) < 2:
        return None

    s = s[::-1]

    total_growth = (s[-1] - s[0]) / abs(s[0])

    if total_growth < min_total_growth:
        return False

    deltas = [b - a for a, b in zip(s[:-1], s[1:])]
    positive_ratio = sum(d > 0 for d in deltas) / len(deltas)

    return positive_ratio >= min_positive_ratio
