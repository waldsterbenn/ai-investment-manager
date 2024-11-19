"""
    # Financial statement analyst
    Will analyse a company's financial statements and provide insights into its performance.
    Provided official financial statements and documents,
    it will analyse the company's financial reality. And provide perspctives for the company's future.

    ## Output
    Will generate a report (markdown format) containing:
    - Profitability.
    - Growth.
    - Upside and downside risk.
    - Market and competition.
"""


import os
from typing import Dict
from llama_index.llms.ollama import Ollama
from components.data_acq_layer import StockDataFin
from portfolio_item import PortfolioItem
from tools.llm_config_factory import LlmModelConfig
import logging
import logging.config

try:
    # Load the logging configuration
    logging.config.fileConfig(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../../config/logging.config')))

    # Get the logger specified in the configuration file
    log = logging.getLogger('sampleLogger')
except FileNotFoundError:
    error = "#ignore"


class FinancialAnalyst:

    def __init__(self, llm_model_to_use: LlmModelConfig, dry_run: bool = False) -> None:
        self.llm_model_to_use = llm_model_to_use
        self.llm_temperature = 0.2
        self.dry_run = dry_run

    def analyse_financials(self, data: list[StockDataFin], stock: PortfolioItem) -> Dict[str, str]:

        if self.dry_run:
            {"financial_report":
                f"This is a report containing Financial Analysis of the stock {stock.name} ({stock.ticker_symbol})"}

        log.info(
            f"Financial statement analysis of {stock.name} ({stock.ticker_symbol}). LLM: {self.llm_model_to_use.name}. Context Window: {self.llm_model_to_use.context_window}. Temperature: {self.llm_temperature}")

        ollama_client = Ollama(
            model=self.llm_model_to_use.name,
            request_timeout=15000.0,
            temperature=self.llm_temperature,
            stream=False,
            context_window=self.llm_model_to_use.context_window
        )

        data_inject = ""
        for value in data:
            if value.fetcher_name is not None and (value.info is not None or value.financial_indicators is not None):
                data_element = f"{value.fetcher_name}:\n"
                if value.info is not None:
                    data_element += f"{value.info}\n"
                if value.financial_indicators is not None:
                    for dataframe in value.financial_indicators:
                        data_element += f"{dataframe.head(50).to_markdown(index=True)}\n"

                data_inject += data_element.replace(
                    ' ', '').replace('\n', '').replace('nan', '') + '\n\n'

        buy_info = (
            (f"It was bought on {stock.buy_date}." if stock.buy_date else "")
            + ("Buy price: " +
               (f"{stock.buy_price} {stock.currency}" if stock.buy_price and stock.currency else ""))
        )
        user_prompt = f"""
            You are an expert financial analyst.
            Analyse this financial statement for the stock {stock.name} ({stock.ticker_symbol}).
            {buy_info if buy_info else ""}
            Focus on the newest data, but also consider historical data.
            Be concrete, precise and use human readable numbers (no scientific notation). 
            Generic answers and disclaimers are strictly forbidden.

            Make a beautiful and concise report in Markdown format containing:
            - Profitability.
            - Growth.
            - Upside and downside risk.
            - Market and competition.

            Financial Statement data:
            ---
            {data_inject}
            ---
            """

        log.info(f"LLM analysing query. Prompt {len(user_prompt)} chars.")
        ollama_completion = ollama_client.complete(user_prompt)
        report_text = ollama_completion.text
        return {"financial_report": report_text.strip()}
