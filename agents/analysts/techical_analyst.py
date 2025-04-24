"""
    # Techical data analysist
    Will analyse a stock's historical performance.
    Provided a dataframe with techical data,
    this will analyse realities about trend, momentum, volatility, etc.

    ## Output
    Will generate a report (markdown format) containing:
    - Stock price.
    - Stock performance numbers.
    - Stock ytd growth.
    - Techical indicators (P/E, EPS, RSI etc.).
"""
import os
from typing import Dict
from components.data_acq_layer import StockDataTech
from infrence_provider.infrence_provider import InferenceProvider
from portfolio_item import PortfolioItem
import logging
import logging.config

# Load the logging configuration
logging.config.fileConfig(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../config/logging.config')))

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


class TechnicalAnalyst:

    def __init__(self, llm_provider: InferenceProvider, dry_run: bool = False) -> None:
        self.llm_provider = llm_provider
        self.llm_temperature = 0.2
        self.dry_run = dry_run

    def analyse_technicals(self, data: list[StockDataTech], stock: PortfolioItem) -> Dict[str, str]:

        if self.dry_run:
            return {"techical_report":
                    f"This is a report containing Technical Analysis of the stock {stock.name} ({stock.ticker_symbol})"}

        log.info(
            f"Techical analysis of {stock.name} ({stock.ticker_symbol}). LLM: {self.llm_provider.get_provider_name()} {self.llm_provider.get_provider_llm()}. Temperature: {self.llm_temperature}")

        data_inject = ""
        for value in data:
            if value.fetcher_name is not None and (value.info is not None or value.techical_indicators is not None):
                data_element = f"{value.fetcher_name}:\n"
                if value.info is not None:
                    data_element += f"{value.info}\n"
                if value.techical_indicators is not None:
                    for table in value.techical_indicators:
                        data_element += f"{table.to_markdown(index=True)}\n"

                data_inject += data_element

        buy_info = (
            (f"It was bought on {stock.buy_date}." if stock.buy_date else "")
            + ("Buy price: " +
               (f"{stock.buy_price} {stock.currency}" if stock.buy_price and stock.currency else ""))
        )
        user_prompt = f"""
                    You are an expert financial analyst. Analyse these technical data for for the stock: {stock.name} ({stock.ticker_symbol}).
                    {buy_info if buy_info else ""}
                    Be concrete, precise and use human readable numbers (no scientific notation). 
                    Generic answers and disclaimers are strictly forbidden.
                    Analyze trends, momentum, volatility, etc.
                    Make a beautiful and concise report in Markdown format containing:
                        - Stock price.
                        - Stock performance numbers.
                        - Stock ytd growth.
                        - Techical indicators (MACD, ADX, RSI, SMA etc.).
    
                    Techical Data:
                    ---
                    {data_inject} 
                    ---
                """
        log.info(f"LLM analysing query. Prompt {len(user_prompt)} chars.")

        report_text = self.llm_provider.infer(
            user_prompt, temperature=self.llm_temperature)

        return {"technical_report": report_text.strip()}
