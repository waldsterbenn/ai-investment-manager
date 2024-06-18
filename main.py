import time
import json
import os
from typing import List
from advisors.portfolio_advisor import PortfolioAdvisor
from advisors.stock_advisor import StockAdvisor
from components.analysis_layer import FinancialStatementAnalyst, TechnicalDataAnalyst
from components.data_acq_layer import DataFetcher, FMPDataFetcher, FinnhubDataFetcher
from components.data_fetchers.sec_edgar_fetcher import SecEdgarDataFetcher
from components.data_fetchers.yfin_data_fetcher import YFinanceFinDataFetcher, YFinanceTechicalDataFetcher
from components.report_generator import ReportGenerator
import logging
import logging.config

from tools.llm_config_factory import LlmConfigFactory, LlmModelType

# Load the logging configuration
logging.config.fileConfig('./config/logging.config')

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


class StockInformationProcessor:
    def __init__(self, apiKeys: dict, llmConfigFactory: LlmConfigFactory):

        self.ta_fetchers: List[DataFetcher] = []
        self.ta_fetchers.append(FMPDataFetcher())
        self.ta_fetchers.append(FinnhubDataFetcher())
        self.ta_fetchers.append(YFinanceTechicalDataFetcher())

        llm_tech = llmConfigFactory.getModel(LlmModelType.techical)
        self.technical_analyst = TechnicalDataAnalyst(llm_tech)

        self.fin_fetchers: List[DataFetcher] = []
        self.fin_fetchers.append(YFinanceFinDataFetcher())
        self.fin_fetchers.append(SecEdgarDataFetcher())

        llm_financial = llmConfigFactory.getModel(LlmModelType.finanical)
        self.financial_analyst = FinancialStatementAnalyst(llm_financial)

        llm_advisor = llmConfigFactory.getModel(LlmModelType.advisory)
        self.stock_advisor = StockAdvisor(llm_advisor)

    def process(self, ticker_symbol: str):
        self.ticker_symbol = ticker_symbol
        log.info(f"Running analysis on {self.ticker_symbol}")

        # Fetch techical data
        techical_data = []
        for fetcher in self.ta_fetchers:
            data = fetcher.fetch_data(self.ticker_symbol)
            if (data.info is not None or data.techical_indicators is not None):
                techical_data.append(data)

        # Fetch finanical data
        financial_data = []
        for fetcher in self.fin_fetchers:
            data = fetcher.fetch_data(self.ticker_symbol)
            financial_data.append(data)

        # Analyse the stock based on techicals
        technical_analysis = self.technical_analyst.analyze(
            techical_data, self.ticker_symbol)

        # Do finanical analysis
        financial_analysis = self.financial_analyst.analyze(
            financial_data, self.ticker_symbol)

        # Provide advice for a position in this stock, based on the techical and financial analysies
        advice_on_stock = self.stock_advisor.provide_advice(
            technical_analysis, financial_analysis)

        return advice_on_stock


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
    report_generator = ReportGenerator()
    processor = StockInformationProcessor(api_keys, llmConfigFactory)

    if not os.path.exists("./reports/"):
        os.mkdir("./reports/")

    for ticker_symbol in app_config["portfolio_tickers"]:
        if os.path.exists(f"./reports/{ticker_symbol}_report.md"):
            continue
        advice_on_stock = processor.process(ticker_symbol)
        report_path = report_generator.write_stock_report(
            ticker_symbol, advice_on_stock)

    files = []
    for foldername, subfolders, filenames in os.walk('./reports/'):
        for filename in filenames:
            if filename == "portfolio_advice_report.md" or filename == "portfolio_assesment_report.md":
                continue
            # Get the full path to the file
            files.append(os.path.join(foldername, filename))

    portfolio_advisor = PortfolioAdvisor(
        llmConfigFactory.getModel(LlmModelType.healthcheck))

    advice = portfolio_advisor.provide_advice(files)
    report_generator.write_advice_report(advice)

    assesment = portfolio_advisor.asses_portfolio(advice)
    report_generator.write_assesment_report(assesment)
