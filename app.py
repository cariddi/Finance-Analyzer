from yahoo_client import load_company
from metrics_income import analyze_income
from metrics_balance import analyze_balance
from metrics_cashflow import analyze_cashflow
from markdown_exporter import export_to_markdown

COMPANY_CATEGORIES = {
    "AAPL": "consumer",
    "KO": "consumer",
    "JPM": "banking",
    "PLTR": "tech",
    "NESN.SW": "consumer",
    "SBUX": "consumer",
}

def analyze_company(ticker):
    data = load_company(ticker)
    category = COMPANY_CATEGORIES.get(ticker, "unknown")

    return {
        "ticker": ticker,
        "income": analyze_income(data["income"], category),
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

if __name__ == "__main__":
    companies = [
        # "AAPL",
        # "KO",
        # "JPM",
        # "PLTR",
        "NESN.SW",
        # "SBUX"
    ]

    all_results = []

    for c in companies:
        print(f"\n📊 {c}")
        result = analyze_company(c)
        all_results.append(result)

        for section, rules in result.items():
            if section == "ticker":
                continue

            print(f"\n{section.upper()}")

            for rule in rules:
                print(f"- {rule['title']}")
                print(f"  {rule['description']}")
                print(f"  Status: {rule['status']}")

                if rule["values"]:
                    for k, v in rule["values"].items():
                        print(f"    {k}: {v}")

    # 📄 Export Markdown report
    md_file = export_to_markdown(all_results)
    print(f"\n📝 Markdown report generated: {md_file}")
