import json
import os
import time
from agents.advisors.portfolio_advisor import PortfolioAdvisor
from agents.advisors.report_summarizer import ReportSummarizer
from components.report_generator import ReportGenerator
import logging
import logging.config

from infrence_provider.infrence_provider_factory import InferenceProviderFactory
from portfolio_loader import PortfolioLoader
from stock_information_processor import StockInformationProcessor

config_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), './config/'))

# Load the logging configuration
logging.config.fileConfig(os.path.join(config_path, "logging.config"))

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')

if __name__ == "__main__":
    try:
        with open(os.path.join(config_path, "api_keys.json")) as keysFile:
            api_keys = json.load(keysFile)
    except FileNotFoundError as e:
        log.error(e)
    try:
        with open(os.path.join(config_path, "app_config.json")) as f:
            app_config = json.load(f)

    except FileNotFoundError as e:
        log.error(e)

    report_generator = ReportGenerator()
    llm_provider = InferenceProviderFactory().create_provider(app_config)
    processor = StockInformationProcessor(api_keys, llm_provider)

    base_folder = "reports"
    if not os.path.exists(base_folder):
        os.mkdir(base_folder)

    fmt = "%Y-%m-%d"
    date_str = f"{time.strftime(fmt, time.gmtime())}"
    report_folder = os.path.join(base_folder, f"report_{date_str}")

    if not os.path.exists(report_folder):
        os.mkdir(report_folder)

    stocks = PortfolioLoader(os.path.join(
        config_path, "portfolio.json")).load()

    for stock in stocks:
        if os.path.exists(f"{report_folder}/{stock.ticker_symbol}_report.md"):
            continue  # Skip existing reports
        advice_on_stock = processor.process(stock)
        report_path = report_generator.write_stock_report(
            report_folder, stock.ticker_symbol, advice_on_stock["advice_on_stock"])

    files = []
    for foldername, subfolders, filenames in os.walk(report_folder):
        for filename in filenames:
            if filename == "portfolio_advice_report.md" or filename == "portfolio_assesment_report.md":
                continue
            # Get the full path to the file
            files.append(os.path.join(foldername, filename))

    summarizer = ReportSummarizer(llm_provider)

    portfolio_advisor = PortfolioAdvisor(llm_provider, summarizer)

    advice = portfolio_advisor.provide_advice(files)
    advice_file = report_generator.write_advice_report(report_folder, advice)
    log.info(f"Portfolio investment advice: {advice_file}")

    assesment = portfolio_advisor.asses_portfolio(advice)
    assesment_file = report_generator.write_assesment_report(
        report_folder, assesment)
    log.info(f"Portfolio assesment: {assesment_file}")
