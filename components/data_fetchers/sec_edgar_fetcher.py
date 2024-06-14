import json
import os
import pandas as pd
from bs4 import BeautifulSoup
from sec_cik_mapper import StockMapper
from components.data_acq_layer import DataFetcher, StockDataFin
from sec_edgar_downloader import Downloader

# https://www.sec.gov/include/ticker.txt


class SecEdgarDataFetcher(DataFetcher):

    def __init__(self):

        if not os.path.exists("./data/"):
            os.mkdir("./data/")
        if not os.path.exists("./data/sec_cik_tickers.json"):

            # Initialize a stock mapper instance
            mapper = StockMapper()

            # Get mapping from ticker to CIK
            tickers_dict = mapper.ticker_to_cik

            with open("./data/sec_cik_tickers.json", "w", encoding="utf8") as f:
                json.dump(tickers_dict, f, ensure_ascii=False, indent=4)
            self.edgar_tickers = tickers_dict
        else:
            with open("./data/sec_cik_tickers.json", "r", encoding="utf8") as f:
                self.edgar_tickers = json.load(f)

    def strip_html(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            contents = f.read()

        # Parse the HTML content
        soup = BeautifulSoup(contents, "html.parser")
        # Extract all text and return
        return soup.get_text()

    def fetch_data(self, ticker_symbol: str) -> StockDataFin:

        # Directory containing all folders within ticker directory
        base_dir = f'./data/sec-edgar-filings/{ticker_symbol}/'

        # Avoid overuse of edgar api, since its rate limit to 10 req/min
        filings = self.load_filings(base_dir)
        if len(filings) != 0:
            return StockDataFin(ticker_symbol, filings)

        dl = Downloader("MyCompanyName", "my.email@domain.com", "./data/")
        # 10-K anual reoport
        # 10-Q, 10-Q/A Quarterly report
        # 8-K, 8-K/A Current report filing
        # Note: after and before strings must be in the form "YYYY-MM-DD"
        nbr_filings = dl.get("8-K", ticker_symbol,
                             after="2024-05-01", before="2024-06-25")
        filings = self.load_filings(base_dir)

        # filepath = '.\\sec-edgar-filings\\NVO\\6-K\\0001171843-24-002400\\full-submission.txt'
        return StockDataFin(ticker_symbol, pd.DataFrame(filings))

    def load_filings(self, base_dir):
        filings = []

        # Iterate through all directories and files under base_dir
        for foldername, subfolders, filenames in os.walk(base_dir):
            for filename in filenames:
                if filename == 'full-submission.txt':
                    # Get the full path to the file
                    filepath = os.path.join(foldername, filename)
                    filings.append(self.strip_html(filepath))
        return filings
