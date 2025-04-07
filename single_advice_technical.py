from infrence_provider.infrence_provider_factory import InferenceProviderFactory
from stock_information_processor import StockInformationProcessor
from portfolio_item import PortfolioItem
import logging.config
import logging
import json
import os
import sys

from tools.unicode_safety import UnicodeSafety


config_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), './config/'))

logging.config.fileConfig(os.path.join(config_path, "logging.config"))

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


def main():
    # Expected string: "{'name':'John Deere','ticker_symbol':'DE','buy_price':386.12,'currency':'USD','buy_date':'2024-06-18'}"
    arg = sys.argv[1].replace("'", '"')
    jsonstr = json.loads(arg)
    stock = PortfolioItem(jsonstr)
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

    llm_provider = InferenceProviderFactory().create_provider(app_config)

    processor = StockInformationProcessor(api_keys, llm_provider)

    advice_on_stock = processor.runTechicalAnalysis(stock)
    print(UnicodeSafety().makeSafe("TECHREPORT:" + advice_on_stock))


if __name__ == "__main__":
    main()
