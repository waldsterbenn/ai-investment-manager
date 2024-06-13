import pandas as pd
from analysts.fin_statement_analyst import FinancialAnalyst
from analysts.techical_analyst import TechnicalAnalyst
import logging
import logging.config

# Load the logging configuration
logging.config.fileConfig('logging.config')

# Get the logger specified in the configuration file
log = logging.getLogger('simpleLogger')


class TechnicalDataAnalyst:
    def analyze(self, data: pd.DataFrame) -> dict:
        # Analyze trends, momentum, volatility, etc.
        return TechnicalAnalyst().analyse_technicals(data)


class FinancialStatementAnalyst:

    def analyze(self, data: dict) -> dict:
        # Analyze profitability, growth, risks, etc.
        return FinancialAnalyst().analyse_financials(data)
