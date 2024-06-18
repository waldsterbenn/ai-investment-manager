import os
import time


class ReportGenerator:
    def ensure_report_dir(self):
        if not os.path.exists("./reports/"):
            os.mkdir("./reports/")

    def write_to_file(self, file_name: str, text: str):
        self.ensure_report_dir()
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(text)

    def write_stock_report(self, ticker_symbol: str, stock_advice: str) -> str:
        # Generate markdown report

        report_time = time.time()

        # Join different sections of the report to avoid unwanted spaces in final string
        report = "\n\n".join([
            "# Advice",
            stock_advice.strip().replace("  ", ""),
            "# Details",
            f"> Ticker code: {ticker_symbol}"
            f"> Report generated at: {time.ctime(report_time)}",
        ])

        self.ensure_report_dir()
        output_filename = f"./reports/{ticker_symbol}_report.md"
        self.write_to_file(output_filename, report)
        return os.path.abspath(output_filename)

    def write_advice_report(self, portfolio_advice: str):
        report_time = time.time()
        # Join different sections of the report to avoid unwanted spaces in final string
        report = "\n\n".join([
            "# Portfolio Advice",
            portfolio_advice.replace("  ", "").strip(),
            "# Notes",
            "> Report generated at {0}".format(time.ctime(report_time)),
        ])
        output_filename = f"./reports/portfolio_advice_report.md"
        self.write_to_file(output_filename, report)

    def write_assesment_report(self, portfolio_assesment: str):
        report_time = time.time()
        # Join different sections of the report to avoid unwanted spaces in final string
        report = "\n\n".join([
            "# Portfolio Assesment",
            portfolio_assesment.replace("  ", "").strip(),
            "# Notes",
            "> Report generated at {0}".format(time.ctime(report_time)),
        ])
        output_filename = f"./reports/portfolio_assesment_report.md"
        self.write_to_file(output_filename, report)
