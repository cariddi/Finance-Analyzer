from utils import safe_get, valid, avg, trend_mostly_up, last_n

def analyze_income(fin, category: str):
    rules = []

    revenue = safe_get(fin, "Total Revenue")
    gross_profit = safe_get(fin, "Gross Profit")
    sga = safe_get(fin, "Selling General And Administration")
    rd = safe_get(fin, "Research & Development")
    depreciation = safe_get(fin, "Depreciation Amortization Depletion")
    interest = safe_get(fin, "Interest Expense Non Operating")
    operating_income = safe_get(fin, "Operating Income")
    net_income = safe_get(fin, "Net Income")
    eps = safe_get(fin, "Basic EPS")

    # Gross Margin
    if valid(revenue, 3) and valid(gross_profit, 3):
        margin = gross_profit / revenue
        value = avg(margin, 10)
        rules.append({
            "title": "Gross Profit Margin",
            "description": "Average Gross Profit / Revenue over last years ≥ 40%",
            "status": "PASS" if value >= 0.40 else "FAIL",
            "values": {
                "avg_margin": round(value, 2),
                "years_used": len(last_n(margin, 10))
            }
        })
    else:
        rules.append({
            "title": "Gross Profit Margin",
            "description": "Average Gross Profit / Revenue over last years ≥ 40%",
            "status": "N/A",
            "values": {}
        })

    # SGA %
    if valid(sga, 3) and valid(gross_profit, 3):
        pct = avg(sga / gross_profit, 10)
        status = "EXCELLENT" if pct < 0.30 else "GREAT" if pct <= 0.80 else "FAIL"
        rules.append({
            "title": "SGA Efficiency",
            "description": "Selling, General & Admin expenses as % of Gross Profit",
            "status": status,
            "values": {"avg_sga_pct": round(pct, 2)}
        })
    else:
        rules.append({
            "title": "SGA Efficiency",
            "description": "Selling, General & Admin expenses as % of Gross Profit",
            "status": "N/A",
            "values": {}
        })

    # R&D
    rules.append({
        "title": "R&D Spending",
        "description": "Research & Development close to zero (or absent)",
        "status": "EXCELLENT" if rd is None else "PASS",
        "values": {"avg_rd": 0 if rd is None else avg(rd, 10)}
    })

    # Depreciation
    if valid(gross_profit, 3):
        pct = avg(depreciation if depreciation is not None else 0 / gross_profit, 10)
        rules.append({
            "title": "Depreciation Load",
            "description": "Depreciation ≤ 10% of Gross Profit",
            "status": "PASS" if pct <= 0.10 else "FAIL",
            "values": {"avg_dep_pct": round(pct, 2)}
        })
    else:
        rules.append({
            "title": "Depreciation Load",
            "description": "Depreciation ≤ 10% of Gross Profit",
            "status": "N/A",
            "values": {}
        })

    # Interest Expense
    if valid(interest, 3) and valid(operating_income, 3):
        pct = avg(interest / operating_income, 10)
        limit = 0.15 if category == "consumer" else 0.30 if category == "banking" else None
        status = "PASS" if limit and pct <= limit else "FAIL"
        rules.append({
            "title": "Interest Burden",
            "description": f"Interest Expense ≤ {int(limit*100)}% of Operating Income",
            "status": status,
            "values": {"avg_interest_pct": round(pct, 2)}
        })
    else:
        rules.append({
            "title": "Interest Burden",
            "description": "Interest Expense vs Operating Income",
            "status": "N/A",
            "values": {}
        })

    # Net Income Margin
    if valid(net_income, 3) and valid(revenue, 3):
        pct = avg(net_income / revenue, 10)
        rules.append({
            "title": "Net Income Margin",
            "description": "Net Income ≥ 20% of Revenue",
            "status": "PASS" if pct >= 0.20 else "FAIL",
            "values": {"avg_net_margin": round(pct, 2)}
        })
    else:
        rules.append({
            "title": "Net Income Margin",
            "description": "Net Income ≥ 20% of Revenue",
            "status": "N/A",
            "values": {}
        })

    # EPS Trend
    if valid(eps, 4):
        status = "PASS" if (eps > 0).all() and trend_mostly_up(eps, 4) else "FAIL"
        rules.append({
            "title": "EPS Growth",
            "description": "Positive EPS with upward trend over 4 years (SHOULD BE 10)",
            "status": status,
            "values": {"eps_0": eps.iloc[3], "eps_1": eps.iloc[2], "eps_2": eps.iloc[1], "eps_3": eps.iloc[0]}
        })
    else:
        rules.append({
            "title": "EPS Growth",
            "description": "Positive EPS with upward trend over 4 years (SHOULD BE 10)",
            "status": "N/A",
            "values": {}
        })

    return rules
