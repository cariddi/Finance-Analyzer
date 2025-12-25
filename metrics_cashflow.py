from utils import safe_get, avg, valid

def analyze_cashflow(cf, fin):
    results = {}

    capex = safe_get(cf, "Capital Expenditure")
    net_income = safe_get(fin, "Net Income")

    if valid(capex) and valid(net_income):
        ratio = avg(abs(capex / net_income), 10)

        if ratio <= 0.25:
            results["CapEx <= 25% NI"] = "EXCELLENT"
        elif ratio <= 0.50:
            results["CapEx <= 50% NI"] = "GREAT"
        else:
            results["CapEx"] = "BAD"
    else:
        results["CapEx"] = "N/A"

    return results
