import os
from typing import Dict
from agents.analysts.fin_statement_analyst import FinancialAnalyst
from agents.analysts.techical_analyst import TechnicalAnalyst
import logging
import logging.config

from components.data_acq_layer import StockDataFin, StockDataTech
from portfolio_item import PortfolioItem
from tools.llm_config_factory import LlmModelConfig

# Load the logging configuration
logging.config.fileConfig(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../config/logging.config')))

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


class TechnicalDataAnalyst:
    def __init__(self, llm_model_to_use: LlmModelConfig):
        self.llm_model_to_use = llm_model_to_use

    def analyze(self, data: list[StockDataTech], stock: PortfolioItem) -> Dict[str, str]:
        # Analyze trends, momentum, volatility, etc.
        return TechnicalAnalyst(self.llm_model_to_use).analyse_technicals(data, stock)


class FinancialStatementAnalyst:
    def __init__(self, llm_model_to_use: LlmModelConfig):
        self.llm_model_to_use = llm_model_to_use

    def analyze(self, data: list[StockDataFin], stock: PortfolioItem) -> Dict[str, str]:
        # Analyze profitability, growth, risks, etc.
        return FinancialAnalyst(self.llm_model_to_use).analyse_financials(data, stock)
