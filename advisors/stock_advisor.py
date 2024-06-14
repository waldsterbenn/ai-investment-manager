"""
# Advisor
# Based on input from 'Financial statement analyst' (finanicals) and 'Techical data analysist' (techical data), this will try to figure out if the company will be profitable.
#
# Output
# Report containing:
# - Is the company profitable?
# - Is there harmoy between technical indicators and financials?
# - What are the sort term risk and long term?
# - What are the riskfactors, i.e. geopolitical, macro, cyclical, technology, compitition, finanical trends.
# - Buy or sell?
"""

from typing import Dict
from llama_index.llms.ollama import Ollama
import logging
import logging.config

from tools.llm_config_factory import LlmConfigFactory, SupportedModels

# Load the logging configuration
logging.config.fileConfig('./config/logging.config')

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


class Advisor:
    def __init__(self, llm_model_to_use: SupportedModels) -> None:
        self.llm_model_to_use = llm_model_to_use
        self.llm_temperature = 0.3

    def provide_advice(self, technical_analysis: Dict[str, str], financial_analysis: Dict[str, str]) -> dict:
        # Combine analyses and provide investment advice
        num_prompt_tokens = 500
        llm_config = LlmConfigFactory(self.llm_model_to_use, num_prompt_tokens)
        log.info(
            f"Advisor analysis LLM: {llm_config.llm_model_name}. Context Window: {llm_config.llm_model_context_window_size}. Temperature: {self.llm_temperature}")

        ollama_client = Ollama(
            model=llm_config.llm_model_name,
            request_timeout=15000.0,
            temperature=self.llm_temperature,
            stream=False,
            context_window=llm_config.llm_model_context_window_size
        )

        user_prompt = f"""
                    You are an expert financial advisor with expertice in trading on the stock market.
                    Analyse the techical and financial reports and provide investment advice.
                    Be concrete and precise. Avoid generic answers and disclaimers.
                    
                    Techical report:
                    ---
                    {technical_analysis} 
                    ---
                    Financial report:
                    ---
                    {financial_analysis} 
                    ---
                """
        log.info(f"LLM analysing query. Prompt {len(user_prompt)} chars.")
        ollama_completion = ollama_client.complete(user_prompt)
        report_text = ollama_completion.text
        return {"advisory_report": report_text}
