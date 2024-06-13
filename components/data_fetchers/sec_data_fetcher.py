import requests
import pandas as pd

from components.data_acq_layer import DataFetcher


class SECDataFetcher(DataFetcher):
    BASE_URL = "https://api.sec-api.io"  # Base URL for the SEC API

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, ticker_symbol: str) -> dict:
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        query = {
            "query": {
                "query_string": {
                    "query": f"ticker:{ticker_symbol} AND formType:(10-K OR 10-Q)"
                }
            },
            "from": 0,
            "size": 10,
            "sort": [
                {"filedAt": {"order": "desc"}}
            ]
        }
        response = requests.post(
            f"{self.BASE_URL}/query", json=query, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extract and process the data as needed
        filings = data.get('filings', [])
        processed_data = self._process_filings(filings)

        return processed_data

    def _process_filings(self, filings: list) -> dict:
        # Example of processing filings to extract relevant information
        processed_data = []
        for filing in filings:
            processed_data.append({
                'filedAt': filing.get('filedAt'),
                'formType': filing.get('formType'),
                'reportUrl': filing.get('linkToFilingDetails')
            })
        return processed_data
