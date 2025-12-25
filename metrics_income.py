from utils import safe_get, valid, avg, trend_up, last_n

def analyze_income(fin, category: str):
    r = {}

    revenue = safe_get(fin, "Total Revenue")
    gross_profit = safe_get(fin, "Gross Profit")
    sga = safe_get(fin, "Selling General and Administrative")
    rd = safe_get(fin, "Research & Development")
    depreciation = safe_get(fin, "Depreciation Amortization Depletion")
    interest = safe_get(fin, "Interest Expense Non Operating")
    operating_income = safe_get(fin, "Operating Income")
    net_income = safe_get(fin, "Net Income")
    eps = safe_get(fin, "Basic EPS")

    # Gross Margin
    if valid(revenue, 3) and valid(gross_profit, 3):
        margin = gross_profit / revenue
        r["Gross Margin >= 40%"] = {
            "value": avg(margin, 10) >= 0.40,
            "years": len(last_n(margin, 10))
        }
    else:
        r["Gross Margin >= 40%"] = "N/A"

    # SGA %
    if valid(sga, 3) and valid(gross_profit, 3):
        pct = sga / gross_profit
        v = avg(pct, 10)
        r["SGA"] = "EXCELLENT" if v < 0.30 else "GREAT" if v <= 0.80 else "BAD"
    else:
        r["SGA"] = "N/A"

    # R&D
    if rd is None:
        r["R&D"] = "EXCELLENT"
    else:
        r["R&D"] = abs(avg(rd, 10))

    # Depreciation
    if valid(depreciation, 3) and valid(gross_profit, 3):
        r["Depreciation <= 10% GP"] = avg(depreciation / gross_profit, 10) <= 0.10
    else:
        r["Depreciation <= 10% GP"] = "N/A"

    # Interest Expense (category-specific)
    if valid(interest, 3) and valid(operating_income, 3):
        pct = avg(interest / operating_income, 10)
        if category == "consumer":
            r["Interest Expense"] = pct <= 0.15
        elif category == "banking":
            r["Interest Expense"] = pct <= 0.30
        else:
            r["Interest Expense"] = "N/A"
    else:
        r["Interest Expense"] = "N/A"

    # Net Income Margin
    if valid(net_income, 3) and valid(revenue, 3):
        r["Net Income >= 20% Revenue"] = avg(net_income / revenue, 10) >= 0.20
    else:
        r["Net Income >= 20% Revenue"] = "N/A"

    # EPS Trend
    if valid(eps, 10):
        r["EPS Uptrend"] = (eps > 0).all() and trend_up(eps, 10)
    else:
        r["EPS Uptrend"] = "N/A"

    return r
