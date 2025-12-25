import yfinance as yf

def load_company(ticker: str):
    t = yf.Ticker(ticker.upper())
    return {
        "income": t.financials,
        "balance": t.balance_sheet,
        "cashflow": t.cashflow
    }
