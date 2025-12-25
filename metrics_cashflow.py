from utils import safe_get, valid, avg

def analyze_cashflow(cashflow, income):
    r = {}

    capex = safe_get(cashflow, "Capital Expenditure")
    net_income = safe_get(income, "Net Income")
    buybacks = safe_get(cashflow, "Repurchase of Capital Stock")

    if valid(capex, 3) and valid(net_income, 3):
        pct = avg(abs(capex) / net_income, 10)
        r["CapEx <= 25% NI"] = "EXCELLENT" if pct <= 0.25 else "GREAT" if pct <= 0.50 else "BAD"
    else:
        r["CapEx <= 25% NI"] = "N/A"

    if buybacks is not None:
        r["Stock Buybacks"] = avg(buybacks < 0, 10)
    else:
        r["Stock Buybacks"] = "N/A"

    return r
