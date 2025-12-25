from yahoo_client import load_company
from metrics_income import analyze_income
from metrics_balance import analyze_balance
from metrics_cashflow import analyze_cashflow

def analyze_company(ticker: str):
    data = load_company(ticker)

    return {
        "ticker": ticker,
        "income": analyze_income(data["income"]),
        "balance": analyze_balance(
            data["balance"],
            data["cashflow"],
            data["income"]
        ),
        "cashflow": analyze_cashflow(
            data["cashflow"],
            data["income"]
        )
    }

def analyze_companies(tickers):
    results = []

    for ticker in tickers:
        print(f"\n📊 ANALYZING {ticker}")
        try:
            result = analyze_company(ticker)
            results.append(result)

            print("\nINCOME STATEMENT")
            for k, v in result["income"].items():
                print(f"{k}: {v}")

            print("\nBALANCE SHEET")
            for k, v in result["balance"].items():
                print(f"{k}: {v}")

            print("\nCASH FLOW")
            for k, v in result["cashflow"].items():
                print(f"{k}: {v}")

        except Exception as e:
            print(f"❌ Failed to analyze {ticker}: {e}")

    return results

if __name__ == "__main__":
    # companies = ["AAPL", "MSFT", "KO", "GOOGL"]
    companies = ["KO"]
    analyze_companies(companies)
