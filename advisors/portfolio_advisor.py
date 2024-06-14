from typing import Dict
from llama_index.llms.ollama import Ollama
import logging
import logging.config

from tools.llm_config_factory import LlmModelConfig

# Load the logging configuration
logging.config.fileConfig('./config/logging.config')

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


class PortfolioAdvisor:
    def __init__(self, llm_model_to_use: LlmModelConfig) -> None:
        self.llm_model_to_use = llm_model_to_use
        self.llm_temperature = 0.3

    def provide_advice(self, report_files: list[str]) -> str:
        # Combine analyses and provide investment advice
        log.info(
            f"Advisor analysis LLM: {self.llm_model_to_use.name}. Context Window: {self.llm_model_to_use.context_window}. Temperature: {self.llm_temperature}")

        ollama_client = Ollama(
            model=self.llm_model_to_use.name,
            request_timeout=15000.0,
            temperature=self.llm_temperature,
            stream=False,
            context_window=self.llm_model_to_use.context_window
        )
        reports = ""
        for report in report_files:
            with open(report) as f:
                reports += report+''.join(f.readlines()) + '\n\n'

        user_prompt = f"""
                    You are an expert financial advisor.
                    Based on the provided reports, and make a buy, sell or hold rating on ALL stocks in the portfolio.
                    Be concrete and precise. Avoid generic answers and disclaimers.
                    
                    Make a list in Markdown containing a table with each stock's recommendation.
                    
                    Reports:
                    ---
                    {reports}
                    ---
                """
        log.info(f"LLM analysing query. Prompt {len(user_prompt)} chars.")
        ollama_completion = ollama_client.complete(user_prompt)
        report_text = ollama_completion.text
        return report_text.strip()
