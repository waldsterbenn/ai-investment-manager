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

    def __init__(self, llm_model_to_use: LlmModelConfig) -> None:
        self.llm_model_to_use = llm_model_to_use
        self.llm_temperature = 0.2

    def analyse_technicals(self, data: list[StockDataTech], ticker_symbol: str) -> Dict[str, str]:

        log.info(
            f"Techical analysis LLM: {self.llm_model_to_use.name}. Context Window: {self.llm_model_to_use.context_window}. Temperature: {self.llm_temperature}")

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
                    data_element += f"{value.techical_indicators.head(50).to_markdown(index=True)}\n"

                # ollama_completion = ollama_client.complete(
                #     "extract only the important information in this text\n\n" + data_element)
                # data_inject += ollama_completion.text
                data_inject += data_element.replace(
                    ' ', '').replace('\n', '').replace('nan', '') + '\n\n'

        user_prompt = f"""
                    You are an expert financial analyst. Analyse these technical data for for the stock: {ticker_symbol}.
                    Be concrete and precise. Avoid generic answers and disclaimers.
                    Analyze trends, momentum, volatility, etc.
                    Make a concise report in Markdown format, containing:
                        - Stock price.
                        - Stock performance numbers.
                        - Stock ytd growth.
                        - Techical indicators (P/E, EPS, RSI etc.).
    
                    Techical Data:
                    ---
                    {data_inject} 
                    ---
                """
        log.info(f"LLM analysing query. Prompt {len(user_prompt)} chars.")

        ollama_completion = ollama_client.complete(user_prompt)
        report_text = ollama_completion.text
        return {"techical_report": report_text.strip()}
