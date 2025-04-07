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

import os
from typing import Dict

import logging
import logging.config

from infrence_provider.infrence_provider import InferenceProvider

try:
    # Load the logging configuration
    logging.config.fileConfig(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../../config/logging.config')))

    # Get the logger specified in the configuration file
    log = logging.getLogger('sampleLogger')
except FileNotFoundError:
    error = "#ignore"


class StockAdvisor:
    def __init__(self,  llm_provider: InferenceProvider, dry_run: bool = False) -> None:
        self.llm_provider = llm_provider
        self.llm_temperature = 0.3
        self.dry_run = dry_run

    def makeTechicalReport(self, technical_analysis: Dict[str, str]) -> str:
        if self.dry_run:
            return "This is a report containing advice on the stock, based on Techical Analysis."

        # Combine analyses and provide investment advice
        log.info(
            f"Advisor analysis. LLM: {self.llm_provider.get_provider_name()} {self.llm_provider.get_provider_llm()}. Temperature: {self.llm_temperature}")

        user_prompt = f"""
                    You are an expert financial advisor with expertice in trading on the stock market.
                    Be critical, concrete and precise. Avoid generic answers and disclaimers.
                    
                    Analyse the Techical reports and provide investment advice.
                    Based on input from 'Techical data analysist' ('Techical Report'), 
                    try to assess if the company is a good buy now or its a good time to sell.
                    
                    Make a report in Markdown containing:
                        - What does the technical indicators tell us?
                        - What are the sort and long term risks, if any?
                        - Make a Buy, Hold or Sell rating.
                    
                    Techical Report:
                    ---
                    {technical_analysis} 
                    ---
                """
        log.info(f"LLM analysing query. Prompt {len(user_prompt)} chars.")
        report_text = self.llm_provider.infer(
            user_prompt, temperature=self.llm_temperature)
        return report_text.strip()

    def provide_advice(self, technical_analysis: Dict[str, str], financial_analysis: Dict[str, str]) -> str:
        if self.dry_run:
            return "This is a report containing advice on the stock."

        # Combine analyses and provide investment advice
        log.info(
            f"Advisor analysis. LLM: {self.llm_provider.get_provider_name()} {self.llm_provider.get_provider_llm()}. Temperature: {self.llm_temperature}")

        user_prompt = f"""
                    You are an expert financial advisor with expertice in trading on the stock market.
                    Be critical, concrete and precise. Avoid generic answers and disclaimers.
                    
                    Analyse the Techical and Financial reports and provide investment advice.
                    Based on input from 'Financial statement analyst' ('Financial Report') and 'Techical data analysist' ('Techical Report'), 
                    try to assess if the company will be profitable in the future.
                    
                    Make a report in Markdown containing:
                        - Is the company profitable?
                        - Is there harmoy between technical indicators and financials?
                        - What are the sort and long term risks?
                        - What are the riskfactors, i.e. geopolitical, macro, cyclical, technology, compitition, finanical trends.
                        - Make a Buy, Hold or Sell rating.
                    
                    Techical Report:
                    ---
                    {technical_analysis} 
                    ---
                    Financial Report:
                    ---
                    {financial_analysis} 
                    ---
                """
        log.info(f"LLM analysing query. Prompt {len(user_prompt)} chars.")
        report_text = self.llm_provider.infer(
            user_prompt, temperature=self.llm_temperature)
        return report_text.strip()
