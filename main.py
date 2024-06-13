import json
from advisors.stock_advisor import Advisor
from components.analysis_layer import FinancialStatementAnalyst, TechnicalDataAnalyst
from components.data_acq_layer import FMPDataFetcher, FinnhubDataFetcher
from components.data_fetchers.sec_data_fetcher import SECDataFetcher
from components.data_fetchers.yfin_data_fetcher import YFinanceDataFetcher
from components.report_generator import ReportGenerator
import logging
import logging.config

# Load the logging configuration
logging.config.fileConfig('logging.config')

# Get the logger specified in the configuration file
log = logging.getLogger('simpleLogger')

sec_data_api_key = "SEC_API_KEY"  # Must match dict in config file


class InvestmentPortfolioManager:
    def __init__(self, apiKeys: dict, symbol: str):
        self.symbol = symbol
        self.sec_fetcher = SECDataFetcher(apiKeys[sec_data_api_key])
        self.fmp_fetcher = FMPDataFetcher()
        self.finnhub_fetcher = FinnhubDataFetcher()
        self.yfinance_fetcher = YFinanceDataFetcher()
        self.technical_analyst = TechnicalDataAnalyst()
        self.financial_analyst = FinancialStatementAnalyst()
        self.advisor = Advisor()
        self.report_generator = ReportGenerator()

    def run(self):
        # Fetch data
        sec_data = self.sec_fetcher.fetch_data(self.symbol)
        fmp_data = self.fmp_fetcher.fetch_data(self.symbol)
        finnhub_data = self.finnhub_fetcher.fetch_data(self.symbol)
        yfinance_data = self.yfinance_fetcher.fetch_data(self.symbol)

        # Analyze data
        techical_data = {}
        techical_data["sec"] = sec_data
        techical_data["yfinance"] = yfinance_data
        technical_analysis = self.technical_analyst.analyze(techical_data)

        financial_data = {}
        financial_data["sec"] = sec_data
        financial_analysis = self.financial_analyst.analyze(financial_data)

        # Provide advice
        advice = self.advisor.provide_advice(
            technical_analysis, financial_analysis)

        # Generate report
        report = self.report_generator.generate_report(
            financial_analysis, advice)

        # Output report
        with open(f"{self.symbol}_report.md", "w") as file:
            file.write(report)


if __name__ == "__main__":
    try:
        with open("api_keys.json") as keysFile:
            apiKeys = json.load(keysFile)
    except FileNotFoundError as e:
        log.error(e)
    manager = InvestmentPortfolioManager(apiKeys, "NOVOB")
    manager.run()
