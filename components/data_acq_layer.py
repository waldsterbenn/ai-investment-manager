from abc import ABC, abstractmethod

import pandas as pd


class StockDataTech:
    def __init__(self, info: dict, techical_indicators: pd.DataFrame) -> None:
        self.info = info
        self.techical_indicators = techical_indicators


class StockDataFin:
    def __init__(self, info: dict, financial_indicators: pd.DataFrame) -> None:
        self.info = info
        self.financial_indicators = financial_indicators


class DataFetcher(ABC):
    @abstractmethod
    def fetch_data(self, ticker_symbol: str) -> StockDataTech:
        pass


class FMPDataFetcher(DataFetcher):
    def fetch_data(self, ticker_symbol: str) -> StockDataTech:
        # Implementation for FMP data fetching
        pass


class FinnhubDataFetcher(DataFetcher):
    def fetch_data(self, ticker_symbol: str) -> StockDataTech:
        # Implementation for Finnhub data fetching
        pass
