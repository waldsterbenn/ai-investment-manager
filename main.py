from datetime import date
import json
import os
import time
from agents.advisors.portfolio_advisor import PortfolioAdvisor
from agents.advisors.report_summarizer import ReportSummarizer
from components.report_generator import ReportGenerator
import logging
import logging.config

from stock_information_processor import StockInformationProcessor
from tools.llm_config_factory import LlmConfigFactory, LlmModelType

# Load the logging configuration
logging.config.fileConfig('./config/logging.config')

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


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

    base_folder = "reports"
    if not os.path.exists(base_folder):
        os.mkdir(base_folder)

    fmt = "%Y-%m-%d"
    date_str = f"{time.strftime(fmt, time.gmtime())}"
    report_folder = os.path.join(base_folder, f"report_{date_str}")

    if not os.path.exists(report_folder):
        os.mkdir(report_folder)

    for ticker_symbol in app_config["portfolio_tickers"]:
        if os.path.exists(f"{report_folder}/{ticker_symbol}_report.md"):
            continue  # Skip existing reports
        advice_on_stock = processor.process(ticker_symbol)
        report_path = report_generator.write_stock_report(
            report_folder,            ticker_symbol, advice_on_stock)

    files = []
    for foldername, subfolders, filenames in os.walk(report_folder):
        for filename in filenames:
            if filename == "portfolio_advice_report.md" or filename == "portfolio_assesment_report.md":
                continue
            # Get the full path to the file
            files.append(os.path.join(foldername, filename))

    summarizer = ReportSummarizer(
        llmConfigFactory.getModel(LlmModelType.summarizer))

    portfolio_advisor = PortfolioAdvisor(
        llmConfigFactory.getModel(LlmModelType.healthcheck), summarizer)

    advice = portfolio_advisor.provide_advice(files)
    advice_file = report_generator.write_advice_report(report_folder, advice)
    log.info(f"Portfolio investment advice: {advice_file}")

    assesment = portfolio_advisor.asses_portfolio(advice)
    assesment_file = report_generator.write_assesment_report(
        report_folder, assesment)
    log.info(f"Portfolio assesment: {assesment_file}")
