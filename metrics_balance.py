from utils import (
    safe_get,
    valid,
    avg,
    trend_mostly_up,
    mostly_present,
    series_values_by_year,
)

def analyze_balance(balance, cashflow, income):
    rules = []

    cash = safe_get(balance, "Cash Cash Equivalents And Short Term Investments")
    capex = safe_get(cashflow, "Capital Expenditure")
    depreciation = (
        safe_get(income, "Depreciation Amortization Depletion")
        if safe_get(income, "Depreciation Amortization Depletion")
        else safe_get(income, "Reconciled Depreciation")
    )
    assets = safe_get(balance, "Total Assets")
    net_income = safe_get(income, "Net Income")
    current_debt = safe_get(balance, "Current Debt And Capital Lease Obligation")
    long_debt = safe_get(balance, "Long Term Debt And Capital Lease Obligation")
    liabilities = safe_get(balance, "Total Liabilities")
    equity = safe_get(balance, "Stockholders' Equity")
    treasury_stock = safe_get(balance, "Treasury Stock")
    retained = safe_get(balance, "Retained Earnings")
    treasury_shares = safe_get(balance, "Treasury Shares Number")
    borrowings = safe_get(balance, "Other Current Borrowings")
    buybacks = safe_get(cashflow, "Repurchase Of Capital Stock")
    
    print("Treasury Shares Number", treasury_shares)

    # Cash trend
    rules.append({
        "title": "Cash Growth",
        "description": "Cash balance positive and increasing over 4 years (SHOULD BE 7)",
        "status": "PASS" if valid(cash, 4) and (cash > 0).all() and trend_mostly_up(cash, 4) else "FAIL",
        "values": series_values_by_year(cash, 4, "cash") if valid(cash, 4) else {}
    })

    # CapEx / Depreciation
    if valid(capex, 3) and valid(depreciation, 3):
        ratio = avg(abs(capex / depreciation), 10)
        rules.append({
            "title": "CapEx vs Depreciation",
            "description": "CapEx / Depreciation > 2 indicates frequent asset replacement; between 1-2 means normal growth / modernization over last 4 years (SHOULD BE 10)",
            "status": "FAIL" if ratio > 2 else "PASS",
            "values": {"avg_ratio": round(ratio, 2)}
        })
    else:
        rules.append({
            "title": "CapEx vs Depreciation",
            "description": "CapEx / Depreciation > 2 indicates frequent asset replacement; between 1-2 means normal growth / modernization over last 4 years (SHOULD BE 10)",
            "status": "N/A",
            "values": {}
        })

    # ROA
    if valid(assets, 3) and valid(net_income, 3):
        roa = avg(net_income / assets, 10)
        rules.append({
            "title": "Return on Assets",
            "description": "ROA > 5% and Total Assets ≥ 10B over last 4 years (SHOULD BE 10)",
            "status": "PASS" if roa > 0.05 and assets.iloc[0] >= 10_000_000_000 else "FAIL",
            "values": {
                "avg_roa": round(roa, 2),
                "current_assets": assets.iloc[0]
            }
        })
    else:
        rules.append({
            "title": "Return on Assets",
            "description": "ROA > 5% and Total Assets ≥ 10B over last 4 years (SHOULD BE 10)",
            "status": "N/A",
            "values": {}
        })

    # Debt structure
    if valid(current_debt, 1) and valid(long_debt, 1):
        ratio = current_debt.iloc[0] / long_debt.iloc[0]
        status = "EXCELLENT" if ratio < 0.6 else "GREAT" if ratio < 1 else "FAIL"
        rules.append({
            "title": "Debt Structure",
            "description": "Short-term debt compared to long-term debt",
            "status": status,
            "values": {"current_to_long_ratio": round(ratio, 2)},
        })
    else:
        rules.append({
            "title": "Debt Structure",
            "description": "Short-term debt compared to long-term debt",
            "status": "N/A",
            "values": {},
        })

    # Long-term debt level
    if valid(long_debt, 4):
        avg_debt = avg(long_debt, 4)
        status = (
            "EXCELLENT" if avg_debt < 1_000_000_000
            else "GREAT" if avg_debt < 10_000_000_000
            else "FAIL"
        )
        rules.append({
            "title": "Long-Term Debt Level",
            "description": "Average long-term debt over last 4 years (SHOULD BE 10)",
            "status": status,
            "values": {"avg_long_term_debt_4y": round(avg_debt)},
        })
    else:
        rules.append({
            "title": "Long-Term Debt Level",
            "description": "Average long-term debt over last 4 years (SHOULD BE 10)",
            "status": "N/A",
            "values": {},
        })

    # Net income coverage of debt
    if valid(net_income, 1) and valid(long_debt, 1):
        ni = net_income.iloc[0]
        ltd = long_debt.iloc[0]
        status = (
            "EXCELLENT" if ni * 2 >= ltd
            else "GREAT" if ni * 4 >= ltd
            else "FAIL"
        )
        rules.append({
            "title": "Net Income Coverage",
            "description": "Net income coverage of long-term debt",
            "status": status,
            "values": {"net_income": ni, "long_term_debt": ltd},
        })
    else:
        rules.append({
            "title": "Net Income Coverage",
            "description": "Net income coverage of long-term debt",
            "status": "N/A",
            "values": {},
        })

    # Liabilities ratio
    if valid(liabilities, 1) and valid(equity, 1):
        base = equity.iloc[0] + (treasury_stock.iloc[0] if treasury_stock is not None else 0)
        ratio = liabilities.iloc[0] / base if base else None
        rules.append({
            "title": "Liabilities Ratio",
            "description": "Total liabilities relative to equity + treasury stock",
            "status": "PASS" if ratio is not None and ratio <= 0.8 else "FAIL",
            "values": {"liabilities_ratio": round(ratio, 2) if ratio else None},
        })
    else:
        rules.append({
            "title": "Liabilities Ratio",
            "description": "Total liabilities relative to equity + treasury stock",
            "status": "N/A",
            "values": {},
        })

    # Retained earnings trend
    rules.append({
        "title": "Retained Earnings Trend",
        "description": "Retained earnings showing upward trend over 4 years (SHOULD BE 5)",
        "status": "PASS" if valid(retained, 4) and trend_mostly_up(retained, 4) else "FAIL",
        "values": series_values_by_year(retained, 4, "retained") if valid(retained, 4) else {}
    })

    # Treasury shares presence
    rules.append({
        "title": "Treasury Shares Presence",
        "description": "Treasury shares present in most of last 4 years (SHOULD BE 10)",
        "status": "GREAT" if mostly_present(treasury_shares, 4) else "FAIL",
        "values": series_values_by_year(treasury_shares, 4, "treasury_shares")
        if valid(treasury_shares, 4)
        else {},
    })

    # Stock buybacks
    rules.append({
        "title": "Stock Buybacks",
        "description": "Repurchase of capital stock seen in most of last 4 years (SHOULD BE 10)",
        "status": "GREAT" if mostly_present(buybacks, 4) else "FAIL",
        "values": series_values_by_year(buybacks, 4, "buybacks")
        if valid(buybacks, 4)
        else {},
    })

    # ROE quality
    if valid(net_income, 4) and valid(equity, 4):
        roe = avg(net_income / equity, 4)
        rules.append({
            "title": "Return on Equity Quality",
            "description": "Average ROE ≥ 20% with strong earnings even during negative equity years over last 4 years (SHOULD BE 10)",
            "status": "PASS" if roe >= 0.2 else "FAIL",
            "values": {"avg_roe_4y": round(roe, 2)},
        })
    else:
        rules.append({
            "title": "Return on Equity Quality",
            "description": "Average ROE ≥ 20% with strong earnings even during negative equity years over last 4 years (SHOULD BE 10)",
            "status": "N/A",
            "values": {},
        })

    # Borrowings
    rules.append({
        "title": "Borrowings Level",
        "description": "Other current borrowings ≤ 6B",
        "status": "PASS"
        if borrowings is None or borrowings.iloc[0] <= 6_000_000_000
        else "FAIL",
        "values": {
            "current_borrowings": borrowings.iloc[0] if borrowings is not None else None
        },
    })

    return rules
