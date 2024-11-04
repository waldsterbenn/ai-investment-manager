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
from typing import Dict
from llama_index.llms.ollama import Ollama
from components.data_acq_layer import StockDataTech
from tools.llm_config_factory import LlmModelConfig
import logging
import logging.config

# Load the logging configuration
logging.config.fileConfig('./config/logging.config')

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


class TechnicalAnalyst:

    def __init__(self, llm_model_to_use: LlmModelConfig, dry_run: bool = False) -> None:
        self.llm_model_to_use = llm_model_to_use
        self.llm_temperature = 0.2
        self.dry_run = dry_run

    def analyse_technicals(self, data: list[StockDataTech], ticker_symbol: str) -> Dict[str, str]:

        if self.dry_run:
            {"techical_report": "This is a report containing Technical Analysis of the stock."}

        log.info(
            f"Techical analysis of ticker: {ticker_symbol}. LLM: {self.llm_model_to_use.name}. Context Window: {self.llm_model_to_use.context_window}. Temperature: {self.llm_temperature}")
        ollama_client = Ollama(
            model=self.llm_model_to_use.name,
            request_timeout=15000.0,
            temperature=self.llm_temperature,
            stream=False,
            context_window=self.llm_model_to_use.context_window
        )

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

        user_prompt = f"""
                    You are an expert financial analyst. Analyse these technical data for for the stock: {ticker_symbol}.
                    Be concrete and precise. Avoid generic answers and disclaimers.
                    Analyze trends, momentum, volatility, etc.
                    Make a concise report in Markdown format, containing:
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

        ollama_completion = ollama_client.complete(user_prompt)
        report_text = ollama_completion.text
        return {"techical_report": report_text.strip()}
