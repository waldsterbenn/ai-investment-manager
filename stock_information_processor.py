from typing import List
from advisors.stock_advisor import StockAdvisor
from components.analysis_layer import FinancialStatementAnalyst, TechnicalDataAnalyst
from components.data_acq_layer import DataFetcher, FMPDataFetcher, FinnhubDataFetcher
from components.data_fetchers.sec_edgar_fetcher import SecEdgarDataFetcher
from components.data_fetchers.yfin_data_fetcher import YFinanceFinDataFetcher, YFinanceTechicalDataFetcher
from tools.llm_config_factory import LlmConfigFactory, LlmModelType
import logging
import logging.config

# Load the logging configuration
logging.config.fileConfig('./config/logging.config')

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


class StockInformationProcessor:
    # Setup data fetchers and configure which LLM are used for each step in the process
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

    # Run techical analysis and gather fundamental data. Make advice for the stock
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
