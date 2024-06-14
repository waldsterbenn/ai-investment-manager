import json
from typing import List
from advisors.stock_advisor import Advisor
from components.analysis_layer import FinancialStatementAnalyst, TechnicalDataAnalyst
from components.data_acq_layer import DataFetcher, FMPDataFetcher, FinnhubDataFetcher
from components.data_fetchers.sec_edgar_fetcher import SecEdgarDataFetcher
from components.data_fetchers.yfin_data_fetcher import YFinanceDataFetcher
from components.report_generator import ReportGenerator
import logging
import logging.config

from tools.llm_config_factory import LlmConfigFactory, LlmModelType

# Load the logging configuration
logging.config.fileConfig('./config/logging.config')

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


class InvestmentPortfolioManager:
    def __init__(self, apiKeys: dict, llmConfigFactory: LlmConfigFactory, ticker_symbol: str):
        self.ticker_symbol = ticker_symbol

        self.ta_fetchers: List[DataFetcher] = []
        self.ta_fetchers.append(FMPDataFetcher())
        self.ta_fetchers.append(FinnhubDataFetcher())
        self.ta_fetchers.append(YFinanceDataFetcher())

        self.technical_analyst = TechnicalDataAnalyst(
            llmConfigFactory.getModel(LlmModelType.techical))

        self.fin_fetchers: List[DataFetcher] = []
        self.fin_fetchers.append(SecEdgarDataFetcher())
        self.financial_analyst = FinancialStatementAnalyst(
            llmConfigFactory.getModel(LlmModelType.finanical))

        self.advisor = Advisor(
            llmConfigFactory.getModel(LlmModelType.advisory))
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

    llm_model_config = app_config["llm_model"]
    llmConfigFactory = LlmConfigFactory(llm_model_config)

    for ticker_symbol in app_config["portfolio_tickers"]:
        manager = InvestmentPortfolioManager(
            api_keys, llmConfigFactory, ticker_symbol)
        manager.run()
