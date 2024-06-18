from llama_index.llms.ollama import Ollama
from tools.llm_config_factory import LlmModelConfig
import logging
import logging.config

# Load the logging configuration
logging.config.fileConfig('./config/logging.config')

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


class ReportSummarizer:
    def __init__(self, llm_model_to_use: LlmModelConfig, dry_run: bool = False) -> None:
        self.llm_model_to_use = llm_model_to_use
        self.llm_temperature = 1
        self.dry_run = dry_run

    def summarize_reports(self, report_files: list[str]) -> list[str]:
        ollama_client = Ollama(
            model=self.llm_model_to_use.name,
            request_timeout=15000.0,
            temperature=self.llm_temperature,
            stream=False,
            context_window=self.llm_model_to_use.context_window
        )
        summaries = []
        for report in report_files:
            summary = self.summarize_report(report, ollama_client)
            summaries.append(summary)
        return summaries

    def summarize_report(self, report_file: str, ollama_client: Ollama) -> str:
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
        ollama_completion = ollama_client.complete(user_prompt)
        return ollama_completion.text
