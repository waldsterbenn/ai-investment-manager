import json
import logging
import logging.config

from portfolio_item import PortfolioItem

# Load the logging configuration
logging.config.fileConfig(os.path.abspath(os.path.join(
    os.path.dirname(__file__), './config/logging.config')))

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


class PortfolioLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path

    def load(self) -> list[PortfolioItem]:
        try:
            with open(self.config_path) as f:
                stock_data = json.load(f)

        except FileNotFoundError as e:
            log.error(e)

        stocks = [PortfolioItem(info) for info in stock_data['portfolio']]
        return stocks
