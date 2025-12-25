from yahoo_client import load_company
from metrics_income import analyze_income
from metrics_balance import analyze_balance
from metrics_cashflow import analyze_cashflow

COMPANY_CATEGORIES = {
    "AAPL": "consumer",
    "KO": "consumer",
    "JPM": "banking",
    "PLTR": "tech"
}

def analyze_company(ticker):
    data = load_company(ticker)
    category = COMPANY_CATEGORIES.get(ticker, "unknown")

    return {
        "ticker": ticker,
        "income": analyze_income(data["income"], category),
        "balance": analyze_balance(data["balance"], data["cashflow"], data["income"]),
        "cashflow": analyze_cashflow(data["cashflow"], data["income"])
    }

if __name__ == "__main__":
    companies = ["AAPL", "KO", "JPM", "PLTR"]

    for c in companies:
        print(f"\n📊 {c}")
        result = analyze_company(c)
        for section, rules in result.items():
            if section == "ticker":
                continue
            print(f"\n{section.upper()}")
            for k, v in rules.items():
                print(f"{k}: {v}")
