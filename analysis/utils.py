from configs import YFINANCE_TICKER_SUFFIX

def add_suffix_to_ticker(ticker):
    return f'{ticker}{YFINANCE_TICKER_SUFFIX}'

def remove_suffix_from_ticker(ticker):
    suffix_length = len(YFINANCE_TICKER_SUFFIX)
    return ticker[:-suffix_length]