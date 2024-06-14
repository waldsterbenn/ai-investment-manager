from components.data_acq_layer import DataFetcher, StockDataFin, StockDataTech
from tools.tecnical_data_tools import get_financial_numbers, hum_stock_analyzer_tool


class YFinanceTechicalDataFetcher(DataFetcher):
    def fetch_data(self, ticker_symbol: str) -> StockDataTech:

        (info, data_table) = hum_stock_analyzer_tool(ticker_symbol)
        return StockDataTech(YFinanceTechicalDataFetcher.__name__, info, data_table)


class YFinanceFinDataFetcher(DataFetcher):
    def fetch_data(self, ticker_symbol: str) -> StockDataFin:

        data_table = get_financial_numbers(ticker_symbol)
        return StockDataFin(YFinanceFinDataFetcher.__name__, None, data_table)
