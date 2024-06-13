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
import json
import pandas as pd
from llama_index.llms.ollama import Ollama
from tools.llm_config_factory import LlmConfigFactory, SupportedModels
import logging
import logging.config

# Load the logging configuration
logging.config.fileConfig('logging.config')

# Get the logger specified in the configuration file
log = logging.getLogger('simpleLogger')


class TechnicalAnalyst:
    llm_temperature = 0.3

    def analyse_technicals(self, data: pd.DataFrame) -> dict:

        num_prompt_tokens = 500
        llm_config = LlmConfigFactory(
            SupportedModels.Llama3_8b, num_prompt_tokens)
        log.info(
            f"Techical analysis LLM: {llm_config.llm_model_name}. Context Window: {llm_config.llm_model_context_window_size}. Temperature: {self.llm_temperature}")

        ollama_client = Ollama(
            model=llm_config.llm_model_name,
            request_timeout=15000.0,
            temperature=self.llm_temperature,
            stream=False,
            context_window=llm_config.llm_model_context_window_size
        )

        user_prompt = f"""
                    You are an expert financial analyst. Analyse these technical data for a stock.
                    Analyze trends, momentum, volatility, etc.
                    Make a report in Markdown format.
                    
                    Techical Data:
                    ---
                    {json.stringify(data)} 
                    ---
                """
        ollama_completion = ollama_client.complete(user_prompt)
        report_text = ollama_completion.text
        return {"techical_report": report_text}
