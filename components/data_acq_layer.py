from abc import ABC, abstractmethod

import pandas as pd


class StockDataTech:
    def __init__(self, fetcher_name: str, info: dict, techical_indicators: pd.DataFrame) -> None:
        self.fetcher_name = fetcher_name
        self.info = info
        self.techical_indicators = techical_indicators


class StockDataFin:
    def __init__(self, fetcher_name: str, info: dict, financial_indicators: pd.DataFrame) -> None:
        self.fetcher_name = fetcher_name
        self.info = info
        self.financial_indicators = financial_indicators


class DataFetcher(ABC):

    @abstractmethod
    def fetch_data(self, ticker_symbol: str) -> StockDataTech:
        pass


class FMPDataFetcher(DataFetcher):
    def fetch_data(self, ticker_symbol: str) -> StockDataTech:
        # Implementation for FMP data fetching
        return StockDataTech(FMPDataFetcher.__name__, None, None)


class FinnhubDataFetcher(DataFetcher):
    def fetch_data(self, ticker_symbol: str) -> StockDataTech:
        # Implementation for Finnhub data fetching
        return StockDataTech(FinnhubDataFetcher.__name__, None, None)
