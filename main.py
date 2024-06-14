from enum import Enum
import json
import string
from typing import List
from advisors.stock_advisor import Advisor
from components.analysis_layer import FinancialStatementAnalyst, TechnicalDataAnalyst
from components.data_acq_layer import DataFetcher, FMPDataFetcher, FinnhubDataFetcher, StockDataFin, StockDataTech
from components.data_fetchers.sec_edgar_fetcher import SecEdgarDataFetcher
from components.data_fetchers.yfin_data_fetcher import YFinanceDataFetcher
from components.report_generator import ReportGenerator
import logging
import logging.config

from tools.llm_config_factory import SupportedModels

# Load the logging configuration
logging.config.fileConfig('./config/logging.config')

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


class InvestmentPortfolioManager:
    def __init__(self, apiKeys: dict, llm_model_to_use, symbol: str):
        self.ticker_symbol = symbol

        self.ta_fetchers: List[DataFetcher] = []
        self.ta_fetchers.append(FMPDataFetcher())
        self.ta_fetchers.append(FinnhubDataFetcher())
        self.ta_fetchers.append(YFinanceDataFetcher())

        self.technical_analyst = TechnicalDataAnalyst(llm_model_to_use)

        self.fin_fetchers: List[DataFetcher] = []
        self.fin_fetchers.append(SecEdgarDataFetcher())
        self.financial_analyst = FinancialStatementAnalyst(llm_model_to_use)

        self.advisor = Advisor(llm_model_to_use)
        self.report_generator = ReportGenerator()

    def run(self):

        # Fetch techical data
        techical_data = {}
        for fetcher in self.ta_fetchers:
            data = fetcher.fetch_data(self.ticker_symbol)
            if (data.info is not None or data.techical_indicators is not None):
                techical_data[data.fetcher_name] = data

        # Analyze data
        technical_analysis = self.technical_analyst.analyze(
            techical_data, self.ticker_symbol)

        # Fetch finanical data
        financial_data = {}
        for fetcher in self.fin_fetchers:
            data = fetcher.fetch_data(self.ticker_symbol)
            financial_data[data.fetcher_name] = data

        # Analyze data
        financial_analysis = self.financial_analyst.analyze(
            financial_data, self.ticker_symbol)

        # Provide advice
        advice = self.advisor.provide_advice(
            technical_analysis, financial_analysis)

        # Generate report
        report_path = self.report_generator.generate_report(
            self.ticker_symbol,
            technical_analysis,
            financial_analysis,
            advice)

        log.debug(f"Report generated at {report_path}")


if __name__ == "__main__":
    try:
        with open("./config/api_keys.json") as keysFile:
            api_keys = json.load(keysFile)
    except FileNotFoundError as e:
        log.error(e)
    try:
        with open("./config/app_config.json") as f:
            app_config = json.load(f)

    except FileNotFoundError as e:
        log.error(e)

    llm_model_to_use = SupportedModels[str(app_config["llm_model"]).lower()]

    for ticker_symbol in app_config["portfolio_tickers"]:
        manager = InvestmentPortfolioManager(
            api_keys, llm_model_to_use, ticker_symbol)
        manager.run()
