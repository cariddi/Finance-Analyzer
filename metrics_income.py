from utils import safe_get, avg, trend_up, valid

def analyze_income(fin):
    results = {}

    revenue = safe_get(fin, "Total Revenue")
    gross_profit = safe_get(fin, "Gross Profit")
    operating_income = safe_get(fin, "Operating Income")
    net_income = safe_get(fin, "Net Income")
    interest_expense = safe_get(fin, "Interest Expense Non Operating")
    sga = safe_get(fin, "Selling General and Administrative")
    depreciation = safe_get(fin, "Depreciation Amortization Depletion")
    eps = safe_get(fin, "Basic EPS")

    # Gross Margin
    if valid(revenue) and valid(gross_profit):
        gross_margin = gross_profit / revenue
        results["AVG Gross Margin >= 40%"] = avg(gross_margin, 10) >= 0.40
    else:
        results["AVG Gross Margin >= 40%"] = "N/A"

    # SGA %
    if valid(sga) and valid(gross_profit):
        sga_pct = sga / gross_profit
        sga_avg = avg(sga_pct, 10)

        if sga_avg < 0.30:
            results["SGA"] = "EXCELLENT"
        elif sga_avg <= 0.80:
            results["SGA"] = "GREAT"
        else:
            results["SGA"] = "BAD"
    else:
        results["SGA"] = "N/A"

    # Depreciation
    if valid(depreciation) and valid(gross_profit):
        dep_pct = depreciation / gross_profit
        results["Depreciation <= 10% GP"] = avg(dep_pct, 10) <= 0.10
    else:
        results["Depreciation <= 10% GP"] = "N/A"

    # Interest Expense
    if valid(interest_expense) and valid(operating_income):
        int_pct = interest_expense / operating_income
        results["Interest <= 15% OpIncome"] = avg(int_pct, 10) <= 0.15
    else:
        results["Interest <= 15% OpIncome"] = "N/A"

    # Net Income Margin
    if valid(net_income) and valid(revenue):
        ni_margin = net_income / revenue
        results["Net Income >= 20% Revenue"] = avg(ni_margin, 10) >= 0.20
    else:
        results["Net Income >= 20% Revenue"] = "N/A"

    # EPS
    if valid(eps):
        results["EPS Positive & Uptrend"] = (eps > 0).all() and trend_up(eps, 10)
    else:
        results["EPS Positive & Uptrend"] = "N/A"

    return results
