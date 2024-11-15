
class PortfolioItem:
    def __init__(self, stock_info):
        self.name = stock_info['name']
        self.ticker_symbol = stock_info['ticker_symbol']
        self.buy_price = stock_info['buy_price']
        self.currency = stock_info['currency']
        self.buy_date = stock_info['buy_date']
