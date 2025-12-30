from utils import safe_get, valid, avg

def analyze_cashflow(cashflow, income):
    rules = []

    capex = safe_get(cashflow, "Capital Expenditure")
    net_income = safe_get(income, "Net Income")
    buybacks = safe_get(cashflow, "Repurchase Of Capital Stock")
    
    if valid(capex, 3) and valid(net_income, 3):
        pct = avg(abs(capex) / net_income, 10)
        status = "EXCELLENT" if pct <= 0.25 else "GREAT" if pct <= 0.50 else "FAIL"
        rules.append({
            "title": "Capital Expenditures",
            "description": "CapEx relative to Net Income",
            "status": status,
            "values": {"avg_capex_pct": round(pct, 2)}
        })
    else:
        rules.append({
            "title": "Capital Expenditures",
            "description": "CapEx relative to Net Income",
            "status": "N/A",
            "values": {}
        })

    rules.append({
        "title": "Stock Buybacks",
        "description": "Consistent repurchase of capital stock",
        "status": "PASS" if buybacks is not None else "N/A",
        "values": {}
    })

    return rules
