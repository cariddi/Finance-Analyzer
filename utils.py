import numpy as np
import pandas as pd

def safe_get(df: pd.DataFrame, field: str):
    if df is None or field not in df.index:
        return None
    return df.loc[field].dropna()

def valid(series):
    return series is not None and len(series) > 0

def avg(series: pd.Series, years: int):
    return series.head(years).mean()

def trend_up(series: pd.Series, years: int):
    s = series.head(years)
    if len(s) < 3:
        return False
    x = np.arange(len(s))
    y = s.values
    slope = np.polyfit(x, y, 1)[0]
    return slope > 0
