import os


class ReportGenerator:
    def generate_report(self, ticker_symbol: str, technical_analysis: dict, finanical_analysis: dict, advice: dict) -> str:
        # Generate markdown report

        report = f"""
        # Advice 
        {str(advice['advisory_report']).strip()}
        
        # Financial Analysis
        {str(finanical_analysis['financial_report']).strip()}
        
        # Technical Analysis
        {str(technical_analysis['techical_report']).strip()}
        """

        if not os.path.exists("./reports/"):
            os.mkdir("./reports/")
        output_filename = f"./reports/{ticker_symbol}_report.md"
        with open(output_filename, "w") as file:
            file.write(report)
        return os.path.abspath(output_filename)
