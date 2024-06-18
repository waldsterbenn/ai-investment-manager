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

        # Summarize the reports or else our prompt will be huge
        reports = ""
        for report in report_files:
            summary = self.summarize_report(report, ollama_client)
            reports += summary + '\n\n'

        user_prompt = f"""
                    You are an expert financial advisor.
                    Remember: Be concrete and precise. Avoid generic answers and disclaimers.
                    
                    First task: 
                    You provide advice on the quality of the portfolio.
                    Asses for both long term and short term positions.
                    
                    Second task: 
                    Based on the provided reports, give all the stocks in the portfolio a buy/hold/sell rating.
                                        
                    Make a list in Markdown containing a table with each stock's recommendation.
                    
                    Stock Reports:
                    ---
                    {reports}
                    ---
                """
        log.info(f"LLM analysing query. Prompt {len(user_prompt)} chars.")
        ollama_completion = ollama_client.complete(user_prompt)
        report_text = ollama_completion.text
        return report_text.strip()

    def summarize_report(self, report_file: str, ollama_client: Ollama) -> str:
        text = ""
        with open(report_file) as f:
            text = ''.join(f.readlines())
        if text == "":
            return ""

        user_prompt = f"""
                    Summarize this but make sure to keep essential information. Especially buy/hold/sell rating.
                    Clearly state which stock it is.
                    ---
                    {text}
                    ---
                """
        log.info(f"Summarizing report. Prompt {len(user_prompt)} chars.")
        ollama_completion = ollama_client.complete(user_prompt)
        return ollama_completion.text

    def asses_portfolio(self, portfolio_advice):
        # Assess the quality of the portfolio.

        log.info(
            f"Portfolilo assesment analysis LLM: {self.llm_model_to_use.name}. Context Window: {self.llm_model_to_use.context_window}. Temperature: {self.llm_temperature}")

        ollama_client = Ollama(
            model=self.llm_model_to_use.name,
            request_timeout=15000.0,
            temperature=self.llm_temperature,
            stream=False,
            context_window=self.llm_model_to_use.context_window
        )

        user_prompt = f"""
                    You are an expert financial advisor.
                    Be concrete and precise. Avoid generic answers and disclaimers.
                    
                    Based on the provided Portfolio Report, make an assesment in Markdown, where you assess the quality of the portfolio.
                    
                    Portfolio Report:
                    ---
                    {portfolio_advice}
                    ---
                """
        log.info(f"LLM analysing query. Prompt {len(user_prompt)} chars.")
        ollama_completion = ollama_client.complete(user_prompt)
        report_text = ollama_completion.text
        return report_text.strip()
