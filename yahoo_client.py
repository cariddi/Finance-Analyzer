import yfinance as yf

def load_company(ticker: str):
    t = yf.Ticker(ticker)

    return {
        "income": t.income_stmt,
        "balance": t.balance_sheet,
        "cashflow": t.cashflow
    }
