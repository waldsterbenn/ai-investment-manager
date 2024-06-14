import os


class ReportGenerator:
    def generate_report(self, ticker_symbol: str, technical_analysis: dict, finanical_analysis: dict, advice: dict) -> str:
        # Generate markdown report

        # Join different sections of the report to avoid unwanted spaces in final string
        report = "\n\n".join([
            "# Advice",
            str(advice['advisory_report']).strip().replace("  ", ""),
            # "# Financial Analysis",
            # str(finanical_analysis['financial_report']
            #     ).strip().replace("  ", ""),
            # "# Technical Analysis",
            # str(technical_analysis['techical_report']
            #     ).strip().replace("  ", "")
        ])

        if not os.path.exists("./reports/"):
            os.mkdir("./reports/")
        output_filename = f"./reports/{ticker_symbol}_report.md"
        with open(output_filename, "w") as file:
            file.write(report)
        return os.path.abspath(output_filename)
