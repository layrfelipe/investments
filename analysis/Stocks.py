from .configs import BIGGEST_BRAZILIAN_COMPANIES_TICKERS_LIST
from .utils import add_suffix_to_ticker

class Stocks:
    def __init__(self):
        self.tickers = [add_suffix_to_ticker(ticker) for ticker in BIGGEST_BRAZILIAN_COMPANIES_TICKERS_LIST]
        print(self.tickers)