from utils import safe_get, valid, avg, trend_up, mostly_present, last_n

def analyze_balance(balance, cashflow, income):
    r = {}

    cash = safe_get(balance, "Cash, Cash Equivalents & Short Term Investments")
    capex = safe_get(cashflow, "Capital Expenditure")
    depreciation = safe_get(income, "Depreciation Amortization Depletion")
    assets = safe_get(balance, "Total Assets")
    net_income = safe_get(income, "Net Income")
    current_debt = safe_get(balance, "Current Debt")
    long_debt = safe_get(balance, "Long Term Debt")
    liabilities = safe_get(balance, "Total Liabilities")
    equity = safe_get(balance, "Stockholders' Equity")
    treasury_stock = safe_get(balance, "Treasury Stock")
    retained = safe_get(balance, "Retained Earnings")
    treasury_shares = safe_get(balance, "Treasury Shares")
    borrowings = safe_get(balance, "Other Current Borrowings")

    # Cash trend
    if valid(cash, 7):
        r["Cash Uptrend"] = (cash > 0).all() and trend_up(cash, 7)
    else:
        r["Cash Uptrend"] = "N/A"

    # CapEx / Depreciation
    if valid(capex, 3) and valid(depreciation, 3):
        r["CapEx/Depreciation > 2"] = avg(abs(capex / depreciation), 10) > 2
    else:
        r["CapEx/Depreciation > 2"] = "N/A"

    # ROA
    if valid(assets, 3) and valid(net_income, 3):
        roa = avg(net_income / assets, 10)
        r["ROA > 5% & Assets >= 10B"] = roa > 0.05 and assets.iloc[0] >= 10_000_000_000
    else:
        r["ROA > 5% & Assets >= 10B"] = "N/A"

    # Debt ratios
    if valid(current_debt, 1) and valid(long_debt, 1):
        ratio = current_debt.iloc[0] / long_debt.iloc[0]
        r["Debt Ratio"] = "EXCELLENT" if ratio < 0.6 else "GREAT" if ratio < 1 else "BAD"
    else:
        r["Debt Ratio"] = "N/A"

    # Long term debt levels
    if valid(long_debt, 10):
        avg_debt = avg(long_debt, 10)
        r["LT Debt"] = "EXCELLENT" if avg_debt < 1e9 else "GREAT"
    else:
        r["LT Debt"] = "N/A"

    # Net income coverage
    if valid(net_income, 1) and valid(long_debt, 1):
        r["NI Coverage"] = "EXCELLENT" if net_income.iloc[0] * 2 >= long_debt.iloc[0] else "GREAT" if net_income.iloc[0] * 4 >= long_debt.iloc[0] else "BAD"
    else:
        r["NI Coverage"] = "N/A"

    # Liabilities ratio
    if valid(liabilities, 1) and valid(equity, 1):
        total_equity = equity.iloc[0] + (treasury_stock.iloc[0] if treasury_stock is not None else 0)
        r["Liabilities Ratio"] = liabilities.iloc[0] / total_equity <= 0.8
    else:
        r["Liabilities Ratio"] = "N/A"

    # Retained earnings
    if valid(retained, 5):
        r["Retained Earnings Trend"] = trend_up(retained, 5)
    else:
        r["Retained Earnings Trend"] = "N/A"

    # Buybacks
    if treasury_shares is not None:
        r["Treasury Shares"] = mostly_present(treasury_shares, 10)
    else:
        r["Treasury Shares"] = "N/A"

    if borrowings is not None:
        r["Borrowings <= 6B"] = borrowings.iloc[0] <= 6_000_000_000
    else:
        r["Borrowings <= 6B"] = "N/A"

    return r
