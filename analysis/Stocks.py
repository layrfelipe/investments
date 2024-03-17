import pandas as pd
import yfinance as yf

from configs import BIGGEST_BRAZILIAN_COMPANIES_TICKERS_LIST
from utils import add_suffix_to_ticker

class Stocks:
    def __init__(self):
        self.tickers = [add_suffix_to_ticker(ticker) for ticker in BIGGEST_BRAZILIAN_COMPANIES_TICKERS_LIST[0]]
        self.yf_tickers_objects = {}
        self.price_data = {}
        self.info_data = {}

        self.fill_tickers_objects()
        self.save_stock_info_data()
        self.fetch_historical_price_data()
    
    def get_tickers(self):
        return self.tickers
    
    def fill_tickers_objects(self):
        for ticker in self.get_tickers():
            self.yf_tickers_objects[ticker] = yf.Ticker(ticker)
    
    def fetch_historical_price_data(self):
        for ticker in self.get_tickers():
            history = self.yf_tickers_objects[ticker].history(period='10y', interval='1wk')
            df_history = pd.DataFrame(history)
            df_history.rename(columns={'Close' : 'Price'}, inplace=True) 
            df_history = round(df_history['Price'], 2)
            self.price_data[ticker] = df_history
    
    def save_stock_info_data(self):
        for ticker in self.get_tickers():
            info = self.yf_tickers_objects[ticker].info
            useful_info_dict = {
                'summary': info['longBusinessSummary'] if 'longBusinessSummary' in info.keys() else None,
                'sector': info['sectorKey'] if 'sectorKey' in info.keys() else None,
                'board': info['companyOfficers'] if 'companyOfficers' in info.keys() else None,
                'pb': round(info['priceToBook'], 2) if 'priceToBook' in info.keys() else None,
                'pl': round(info['trailingPE'], 2) if 'trailingPE' in info.keys() else None,
                'dy': round(info['dividendYield'], 2) if 'dividendYield' in info.keys() else None,
                'dy_media_5y': round(info['fiveYearAvgDividendYield'], 2) if 'fiveYearAvgDividendYield' in info.keys() else None,
                'payout': round(info['payoutRatio'], 2) if 'payoutRatio' in info.keys() else None,
                'roe': round(info['returnOnEquity'], 2) if 'returnOnEquity' in info.keys() else None,
                'ebitda': info['ebitda'] if 'ebitda' in info.keys() else None,
                'market_cap': round(info['enterpriseValue'], 2) if 'enterpriseValue' in info.keys() else None,
                'free_cash_flow': info['freeCashflow'] if 'freeCashflow' in info.keys() else None,
                'operating_cash_flow': info['operatingCashflow'] if 'operatingCashflow' in info.keys() else None,
                'total_cash': info['totalCash'] if 'totalCash' in info.keys() else None,
                'total_revenue': info['totalRevenue'] if 'totalRevenue' in info.keys() else None,
                'total_debt': info['totalDebt'] if 'totalDebt' in info.keys() else None,
                'debt_to_equity': info['debtToEquity'] if 'debtToEquity' in info.keys() else None,
                'ebitda_margins': info['ebitdaMargins'] if 'ebitdaMargins' in info.keys() else None,
                'profit_margins': info['profitMargins'] if 'profitMargins' in info.keys() else None,
                'gross_margins': info['grossMargins'] if 'grossMargins' in info.keys() else None,
                # 'earnings_quarterly_growth': round(info['earningsQuarterlyGrowth'], 2) if 'earningsQuarterlyGrowth' in info.keys() else None,
                # 'earnings_growth': round(info['earningsGrowth'], 2) if 'earningsGrowth' in info.keys() else None,
                # 'revenue_growth': round(info['revenueGrowth'], 2) if 'revenueGrowth' in info.keys() else None,
            }
            self.info_data[ticker] = useful_info_dict

# print('fiftyDayAverage: ', petrobras['fiftyDayAverage'])
# print('twoHundredDayAverage: ', petrobras['twoHundredDayAverage'])
# print('auditRisk: ', petrobras['auditRisk'])
# print('boardRisk: ', petrobras['boardRisk'])
# print('compensationRisk: ', petrobras['compensationRisk'])
# print('shareHolderRightsRisk: ', petrobras['shareHolderRightsRisk'])
# print('overallRisk: ', petrobras['overallRisk'])