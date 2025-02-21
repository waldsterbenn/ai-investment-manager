import datetime


class PortfolioItem:
    def __init__(self, stock_info):
        self.name = stock_info['name']
        self.ticker_symbol = stock_info['ticker_symbol']
        self.buy_price = stock_info.get('buy_price', -1)
        self.currency = stock_info.get('currency', "")
        self.buy_date = stock_info.get(
            'buy_date', datetime.datetime.now().date())
