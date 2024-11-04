import os
import time


class ReportGenerator:
    def ensure_report_dir(self, report_folder: str):
        if not os.path.exists(report_folder):
            os.mkdir(report_folder)

    def write_to_file(self, report_folder: str, file_name: str, text: str) -> str:
        self.ensure_report_dir(report_folder)
        file_path = os.path.join(report_folder, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)
        return os.path.abspath(file_path)

    def write_stock_report(self, report_folder: str, ticker_symbol: str, stock_advice: str) -> str:
        # Generate markdown report

        report_time = time.time()

        # Join different sections of the report to avoid unwanted spaces in final string
        report = "\n\n".join([
            "# Advice",
            stock_advice.strip().replace("  ", ""),
            "# Details",
            f"> Ticker code: {ticker_symbol}\n"
            f"> Report generated at: {time.ctime(report_time)}",
        ])

        output_filename = f"{ticker_symbol}_report.md"
        return self.write_to_file(report_folder, output_filename, report)

    def write_advice_report(self, report_folder: str, portfolio_advice: str) -> str:
        report_time = time.time()
        # Join different sections of the report to avoid unwanted spaces in final string
        report = "\n\n".join([
            "# Portfolio Advice",
            portfolio_advice.replace("  ", "").strip(),
            "# Notes",
            "> Report generated at {0}".format(time.ctime(report_time)),
        ])
        output_filename = f"portfolio_advice_report.md"
        return self.write_to_file(report_folder, output_filename, report)

    def write_assesment_report(self, report_folder: str, portfolio_assesment: str) -> str:
        report_time = time.time()
        # Join different sections of the report to avoid unwanted spaces in final string
        report = "\n\n".join([
            "# Portfolio Assesment",
            portfolio_assesment.replace("  ", "").strip(),
            "# Notes",
            "> Report generated at {0}".format(time.ctime(report_time)),
        ])
        output_filename = f"portfolio_assesment_report.md"
        return self.write_to_file(report_folder, output_filename, report)
