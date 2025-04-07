import os
from infrence_provider.infrence_provider import InferenceProvider
import logging
import logging.config

# Load the logging configuration
logging.config.fileConfig(os.path.abspath(os.path.join(
    os.path.dirname(__file__), './config/logging.config')))

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


class ReportSummarizer:
    def __init__(self, llm_provider: InferenceProvider, dry_run: bool = False) -> None:
        self.llm_provider = llm_provider
        self.llm_temperature = 1
        self.dry_run = dry_run

    def summarize_reports(self, report_files: list[str]) -> list[str]:

        summaries = []
        for report in report_files:
            summary = self.summarize_report(report)
            summaries.append(summary)
        return summaries

    def summarize_report(self, report_file: str) -> str:
        text = ""
        with open(report_file) as f:
            text = ''.join(f.readlines())
        if text == "":
            return ""

        user_prompt = f"""
                    Summarize this text. 
                    Remember: 
                     - Keep essential information. 
                     - Preserve buy/hold/sell rating.
                     - Clearly state which stock it is.
                    ---
                    {text}
                    ---
                """
        log.info(f"Summarizing report. Prompt {len(user_prompt)} chars.")
        ollama_completion = self.llm_provider.infer(user_prompt)
        return ollama_completion.strip()
