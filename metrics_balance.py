from utils import safe_get, avg, trend_up, valid

def analyze_balance(bs, cf, fin):
    results = {}

    cash = safe_get(bs, "Cash, Cash Equivalents & Short Term Investments")
    inventory = safe_get(bs, "Inventory")
    retained = safe_get(bs, "Retained Earnings")
    total_assets = safe_get(bs, "Total Assets")
    long_term_debt = safe_get(bs, "Long Term Debt")
    current_debt = safe_get(bs, "Current Debt")
    equity = safe_get(bs, "Stockholders' Equity")

    capex = safe_get(cf, "Capital Expenditure")
    depreciation = safe_get(fin, "Depreciation Amortization Depletion")
    net_income = safe_get(fin, "Net Income")

    # Cash trend
    results["Cash Uptrend 7Y"] = (
        valid(cash) and (cash > 0).all() and trend_up(cash, 7)
    )

    # Inventory + Net Income
    results["Inventory & NI Uptrend"] = (
        valid(inventory)
        and valid(net_income)
        and (inventory > 0).all()
        and (net_income > 0).all()
        and trend_up(inventory, 7)
    )

    # CapEx / Depreciation
    if valid(capex) and valid(depreciation):
        capex_ratio = abs(capex / depreciation)
        results["CapEx/Depreciation > 2"] = avg(capex_ratio, 10) > 2
    else:
        results["CapEx/Depreciation > 2"] = "N/A"

    # ROA
    if valid(net_income) and valid(total_assets):
        roa = net_income / total_assets
        results["ROA > 5% & Assets >= 10B"] = (
            avg(roa, 10) > 0.05 and total_assets.iloc[0] >= 10_000_000
        )
    else:
        results["ROA > 5% & Assets >= 10B"] = "N/A"

    # Short vs Long Debt
    if valid(current_debt) and valid(long_term_debt):
        ratio = avg(current_debt / long_term_debt, 10)
        if ratio < 0.6:
            results["Short/Long Debt"] = "EXCELLENT"
        elif ratio < 1:
            results["Short/Long Debt"] = "GREAT"
        else:
            results["Short/Long Debt"] = "BAD"
    else:
        results["Short/Long Debt"] = "N/A"

    # Net Income pays debt
    if valid(net_income) and valid(long_term_debt):
        results["NI x4 >= LTD"] = (
            avg(net_income, 10) * 4 >= avg(long_term_debt, 10)
        )
    else:
        results["NI x4 >= LTD"] = "N/A"

    # Retained earnings
    results["Retained Earnings Uptrend"] = (
        valid(retained) and trend_up(retained, 10)
    )

    return results
