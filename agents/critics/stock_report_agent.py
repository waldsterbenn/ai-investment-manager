import os
import time
from llama_index.llms.ollama import Ollama
import logging
import logging.config

from agents.critics.prompts import Prompts
from tools.llm_config_factory import LlmModelConfig

# Load the logging configuration
logging.config.fileConfig(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../config/logging.config')))

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


class StockReportAgent:
    def __init__(self, llm_model_to_use: LlmModelConfig, dry_run: bool = False) -> None:
        self.llm_model_to_use = llm_model_to_use
        self.llm_temperature = 0.5
        self.dry_run = dry_run
        self.max_iterations = 2
        self.llm_client = Ollama(
            model=llm_model_to_use.name,
            request_timeout=15000.0,
            temperature=self.llm_temperature,
            stream=False,
            context_window=self.llm_model_to_use.context_window
        )

    def hone_report(self, report_text: str) -> str:

        base_folder = "reports"
        if not os.path.exists(base_folder):
            os.mkdir(base_folder)

        fmt = "%Y-%m-%d"
        date_str = f"{time.strftime(fmt, time.gmtime())}"
        report_folder = os.path.join(base_folder, f"report_{date_str}")

        if not os.path.exists(report_folder):
            os.mkdir(report_folder)

        with open(os.path.join(report_folder, f"test_{0}_report.txt"), "w", encoding="utf-8") as file:
            file.write(report_text)

        count = 0
        report = report_text
        instruction = ""
        while count < self.max_iterations:
            count += 1
            report = self.analyse_report(report, "¤Instruction¤: "+instruction)
            with open(os.path.join(report_folder, f"test_{count}_report.txt"), "w", encoding="utf-8") as file:
                file.write(report)
            if report.count("</think>"):
                report = report.split("</think>")[1]
            assesment = self.critique_report(report)

            with open(os.path.join(report_folder, f"test_{count}_asses.txt"), "w", encoding="utf-8") as file:
                file.write("*************************************")
                file.write(assesment)

            if assesment.count("DONE") > 0:
                break
            if assesment.count("</think>"):
                instruction = assesment.split("</think>")[1]
            else:
                instruction = assesment
        return report

    def analyse_report(self, report_text: str, instruction: str) -> str:
        if self.dry_run:
            return "This is a report."

        # Combine analyses and provide investment advice
        log.info(
            f"LLM: {self.llm_model_to_use.name}. Context Window: {self.llm_model_to_use.context_window}. Temperature: {self.llm_temperature}")

        user_prompt = f"""
                    {Prompts.reportAnalystPrompt}
                    
                    {instruction}
                    
                    ¤Stock Report¤:
                    ---
                    {report_text}
                    ---
                """

        log.info(f"LLM analysing query. Prompt {len(user_prompt)} chars.")
        report_text = self.invoke_llm(self.llm_client, user_prompt)
        return report_text

    def critique_report(self, report_text: str) -> str:

        log.info(
            f"LLM: {self.llm_model_to_use.name}. Context Window: {self.llm_model_to_use.context_window}. Temperature: {self.llm_temperature}")

        user_prompt = f"""
                    {Prompts.critique}
                    
                    ¤Stock Report¤:
                    ---
                    {report_text}
                    ---
                """

        log.info(f"LLM analysing query. Prompt {len(user_prompt)} chars.")
        report_text = self.invoke_llm(self.llm_client, user_prompt)
        return report_text

    def invoke_llm(self, ollama_client, user_prompt):
        ollama_completion = ollama_client.complete(user_prompt)
        report_text = ollama_completion.text
        return report_text.strip()
