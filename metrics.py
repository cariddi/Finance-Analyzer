from utils import avg, trend_positive, all_positive

def get_first_existing(source: dict, keys: list):
    for k in keys:
        if k in source:
            return source[k]
    return {}

from utils import avg, trend_positive, all_positive

def compute_metrics(fin):
    m = {}

    inc = fin["income"]
    bal = fin["balance"]
    cf  = fin["cashflow"]

    # -------- Years (last 10 complete) --------
    years = sorted(
        [y for y, v in inc.items() if v.get("complete")],
        reverse=True
    )[:10]

    if not years:
        raise ValueError("No complete income statement years")

    def series(src, key):
        return [src.get(y, {}).get(key) for y in years]

    # ---------- Income ----------
    revenue = series(inc, "revenue")
    gross_profit = series(inc, "gross_profit")
    sga = series(inc, "sga")
    rnd = series(inc, "rnd")
    da = series(inc, "depreciation")
    op_income = series(inc, "operating_income")
    interest = series(inc, "interest_expense")
    net_income = series(inc, "net_income")
    eps = series(inc, "eps")

    m["gross_margin_avg"] = avg([
        g / r * 100 for g, r in zip(gross_profit, revenue) if g and r
    ])

    m["sga_pct"] = avg([
        s / g * 100 for s, g in zip(sga, gross_profit) if s and g
    ])

    m["rnd_pct"] = avg([
        r / g * 100 for r, g in zip(rnd, gross_profit) if r and g
    ])

    m["da_pct"] = avg([
        d / g * 100 for d, g in zip(da, gross_profit) if d and g
    ])

    m["interest_pct"] = avg([
        i / o * 100 for i, o in zip(interest, op_income) if i and o
    ])

    m["net_margin"] = avg([
        n / r * 100 for n, r in zip(net_income, revenue) if n and r
    ])

    m["eps_positive_trend"] = all_positive(eps) and trend_positive(eps)

    # ---------- Balance Sheet ----------
    cash = series(bal, "cash")[:7]
    inventory = series(bal, "inventory")[:7]
    total_assets = series(bal, "total_assets")
    current_debt = series(bal, "current_debt")
    lt_debt = series(bal, "long_term_debt")
    liabilities = series(bal, "total_liabilities")
    equity = series(bal, "equity")
    treasury = series(bal, "treasury_stock")
    retained = series(bal, "retained_earnings")
    preferred = series(bal, "preferred_stock")

    m["cash_trend"] = all_positive(cash) and trend_positive(cash)

    m["inventory_and_income_trend"] = (
        all_positive(inventory) and
        all_positive(net_income[:7]) and
        trend_positive(inventory) and
        trend_positive(net_income[:7])
    )

    m["roa_avg"] = avg([
        n / a * 100 for n, a in zip(net_income, total_assets) if n and a
    ])

    m["assets_ok"] = total_assets[0] >= 10_000_000_000

    m["short_vs_long_debt"] = avg([
        c / l for c, l in zip(current_debt, lt_debt) if c and l
    ])

    m["debt_payable"] = avg(net_income) * 4 >= avg(lt_debt)

    m["debt_to_equity"] = avg([
        l / (e + abs(t))
        for l, e, t in zip(liabilities, equity, treasury)
        if l and e is not None and t is not None
    ])

    m["preferred_low"] = avg(preferred) is None or avg(preferred) < 1_000_000_000

    m["retained_trend"] = trend_positive(retained)

    # ---------- Cashflow ----------
    capex = series(cf, "capex")
    repurchase = series(cf, "share_repurchase")

    m["capex_pct"] = avg([
        abs(c) / n * 100 for c, n in zip(capex, net_income) if c and n
    ])

    m["buybacks_present"] = sum(
        1 for r in repurchase if r and r < 0
    ) >= 6

    return m
