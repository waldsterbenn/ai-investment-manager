import os
from infrence_provider.infrence_provider import InferenceProvider
import logging
import logging.config
from agents.advisors.report_summarizer import ReportSummarizer

# Load the logging configuration
logging.config.fileConfig(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../config/logging.config')))

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


class PortfolioAdvisor:
    def __init__(self, llm_provider: InferenceProvider, report_summarizer: ReportSummarizer, dry_run: bool = False) -> None:
        self.llm_provider = llm_provider
        self.llm_temperature = 0.5
        self.dry_run = dry_run
        self.report_summarizer = report_summarizer

    def provide_advice(self, report_files: list[str]) -> str:
        if self.dry_run:
            return "This is a report containing advice on the portfolio."

        # Combine analyses and provide investment advice
        log.info(
            f"Advisor analysis of {len(report_files)} stock reports. LLM: {self.llm_provider.get_provider_llm}. Temperature: {self.llm_temperature}")

        # Summarize the reports or else our prompt will be huge
        summaries = self.report_summarizer.summarize_reports(report_files)
        reports = '\n\n'.join(summaries)

        user_prompt = f"""
                    You are a world class financial advisor.
                    Remember: 
                     - Be concrete and precise. Avoid generic answers and disclaimers.
                     - Make output in Markdown. 
                     - Prefer to present data in tables.
                    
                    First task: 
                    You provide advice on the quality of the portfolio.
                    Asses the individual stocks for both long term and short term positions.
                    
                    Second task: 
                    Based on the provided 'Stock Reports', give all the stocks in the portfolio a buy/hold/sell rating.
                    Put these ratings in a table.
                    
                    Stock Reports:
                    ---
                    {reports}
                    ---
                """
        log.info(f"LLM analysing query. Prompt {len(user_prompt)} chars.")
        ollama_completion = self.llm_provider.infer(user_prompt)
        report_text = ollama_completion
        return report_text.strip()

    def asses_portfolio(self, portfolio_advice) -> str:
        # Assess the quality of the portfolio.

        log.info(
            f"Portfolilo assesment analysis LLM: {self.llm_provider.get_provider_llm}. Temperature: {self.llm_temperature}")

        user_prompt = f"""
                    You are an expert financial advisor.
                    Be concise, concrete and precise. Avoid generic answers and disclaimers.
                    
                    Based on the provided 'Portfolio Report', make an overall assesment on quality of the portfolio.
                                        
                    Portfolio Report:
                    ---
                    {portfolio_advice}
                    ---
                """
        log.info(f"LLM analysing query. Prompt {len(user_prompt)} chars.")
        ollama_completion = self.llm_provider.infer(user_prompt)
        report_text = ollama_completion
        return report_text.strip()
