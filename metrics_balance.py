from utils import safe_get, valid, avg, trend_mostly_up, mostly_present

def analyze_balance(balance, cashflow, income):
    rules = []

    cash = safe_get(balance, "Cash Cash Equivalents And Short Term Investments")
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
    
    # print(cash)

    # Cash trend
    rules.append({
        "title": "Cash Growth",
        "description": "Cash balance positive and increasing over 4 years (SHOULD BE 7)",
        "status": "PASS" if valid(cash, 4) and (cash > 0).all() and trend_mostly_up(cash, 4) else "FAIL",
        "values": {"cash_0": cash.iloc[3], "cash_1": cash.iloc[2], "cash_2": cash.iloc[1], "cash_3": cash.iloc[0]}
    })

    # CapEx / Depreciation
    if valid(capex, 3) and valid(depreciation, 3):
        ratio = avg(abs(capex / depreciation), 10)
        rules.append({
            "title": "CapEx vs Depreciation",
            "description": "CapEx / Depreciation > 2 indicates frequent asset replacement",
            "status": "FAIL" if ratio > 2 else "PASS",
            "values": {"avg_ratio": round(ratio, 2)}
        })
    else:
        rules.append({
            "title": "CapEx vs Depreciation",
            "description": "CapEx / Depreciation",
            "status": "N/A",
            "values": {}
        })

    # ROA
    if valid(assets, 3) and valid(net_income, 3):
        roa = avg(net_income / assets, 10)
        rules.append({
            "title": "Return on Assets",
            "description": "ROA > 5% and Total Assets ≥ 10B",
            "status": "PASS" if roa > 0.05 and assets.iloc[0] >= 10_000_000_000 else "FAIL",
            "values": {
                "avg_roa": round(roa, 2),
                "current_assets": assets.iloc[0]
            }
        })
    else:
        rules.append({
            "title": "Return on Assets",
            "description": "ROA > 5% and Total Assets ≥ 10B",
            "status": "N/A",
            "values": {}
        })

    # Debt Ratio
    if valid(current_debt, 1) and valid(long_debt, 1):
        ratio = current_debt.iloc[0] / long_debt.iloc[0]
        status = "EXCELLENT" if ratio < 0.6 else "GREAT" if ratio < 1 else "FAIL"
        rules.append({
            "title": "Debt Structure",
            "description": "Short-term debt vs long-term debt",
            "status": status,
            "values": {"current_to_long_ratio": round(ratio, 2)}
        })
    else:
        rules.append({
            "title": "Debt Structure",
            "description": "Short-term debt vs long-term debt",
            "status": "N/A",
            "values": {}
        })

    # Retained Earnings
    rules.append({
        "title": "Retained Earnings Trend",
        "description": "Retained earnings showing upward trend",
        "status": "PASS" if valid(retained, 5) and trend_mostly_up(retained, 5) else "N/A",
        "values": {}
    })

    # Borrowings
    rules.append({
        "title": "Borrowings Level",
        "description": "Other current borrowings ≤ 6B",
        "status": "PASS" if borrowings is not None and borrowings.iloc[0] <= 6_000_000_000 else "FAIL",
        "values": {"current_borrowings": borrowings.iloc[0] if borrowings is not None else None}
    })

    return rules
