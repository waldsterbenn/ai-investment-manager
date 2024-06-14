from components.data_acq_layer import DataFetcher, StockDataTech
from tools.tecnical_data_tools import fu_stock_analyzer_tool, hum_stock_analyzer_tool


class YFinanceDataFetcher(DataFetcher):
    def fetch_data(self, ticker_symbol: str) -> StockDataTech:

        (info, data_table) = hum_stock_analyzer_tool(ticker_symbol)
        return StockDataTech(YFinanceDataFetcher.__name__, info, data_table)
