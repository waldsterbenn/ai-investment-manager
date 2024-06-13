from components.data_acq_layer import DataFetcher
import yfinance as yf
import pandas as pd


class YFinanceDataFetcher(DataFetcher):
    def fetch_data(self, ticker_symbol: str) -> pd.DataFrame:
        stock = yf.Ticker(ticker_symbol)
        hist = stock.history(period="1y")  # Fetch 1 year of historical data
        # TODO: use the tools we already have
        return hist
