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


class FinancialAnalyst:
    llm_temperature = 0.3

    def analyse_financials(data: dict) -> dict:
        num_prompt_tokens = 500
        llm_config = LlmConfigFactory(
            SupportedModels.Llama3_8b, num_prompt_tokens)
        log.info(
            f"Financial statement analysis LLM: {llm_config.llm_model_name}. Context Window: {llm_config.llm_model_context_window_size}. Temperature: {self.llm_temperature}")

        ollama_client = Ollama(
            model=llm_config.llm_model_name,
            request_timeout=15000.0,
            temperature=self.llm_temperature,
            stream=False,
            context_window=llm_config.llm_model_context_window_size
        )

        user_prompt = f"""
                    You are an expert financial analyst.
                    Analyse this financial statement for a stock.
                    
                    Make a report in Markdown format containing:
                    - Profitability.
                    - Growth.
                    - Upside and downside risk.
                    - Market and competition.
        
                    Financial Statement:
                    ---
                    {json.stringify(data)} 
                    ---
                """
        ollama_completion = ollama_client.complete(user_prompt)
        report_text = ollama_completion.text
        return {"financial_report": report_text}
