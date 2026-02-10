import os
import pandas as pd
import yfinance as yf

def load_market_data(tickers, start="2022-01-01"):
    raw = yf.download(tickers, start=start, auto_adjust=True)

    if isinstance(raw.columns, pd.MultiIndex):
        prices = raw["Close"]
    else:
        prices = raw[["Close"]]

    returns = prices.pct_change().dropna()
    return prices, returns


def load_portfolio():
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "sample_data.csv")
    return pd.read_csv(file_path)

