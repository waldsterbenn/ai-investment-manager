from abc import ABC, abstractmethod


class DataFetcher(ABC):
    @abstractmethod
    def fetch_data(self, ticker_symbol: str) -> dict:
        pass


class FMPDataFetcher(DataFetcher):
    def fetch_data(self, ticker_symbol: str) -> dict:
        # Implementation for FMP data fetching
        pass


class FinnhubDataFetcher(DataFetcher):
    def fetch_data(self, ticker_symbol: str) -> dict:
        # Implementation for Finnhub data fetching
        pass
