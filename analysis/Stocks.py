import pandas as pd
import yfinance as yf

from configs import BIGGEST_BRAZILIAN_COMPANIES_TICKERS_LIST
from utils import add_suffix_to_ticker

class Stocks:
    def __init__(self):
        self.tickers = [add_suffix_to_ticker(ticker) for ticker in BIGGEST_BRAZILIAN_COMPANIES_TICKERS_LIST]
        self.yf_tickers_objects = {}
        self.price_data = {}
        self.info_data = {}
        self.sectors = []
        self.growth_rates_by_sector = {}
        self.market_cap_by_sector_10y_ago = {}
        self.current_market_cap_by_sector = {}

        self.fill_tickers_objects()
        self.save_stock_info_data()
        self.save_sectors()
        self.fetch_historical_price_data()
        self.set_growth_rates_by_sector()
    
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
                'ebitda_margins': round(info['ebitdaMargins'], 2) if 'ebitdaMargins' in info.keys() else None,
                'profit_margins': round(info['profitMargins'], 2) if 'profitMargins' in info.keys() else None,
                'gross_margins': round(info['grossMargins'], 2) if 'grossMargins' in info.keys() else None,
                'earnings_quarterly_growth': round(info['earningsQuarterlyGrowth'], 2) if 'earningsQuarterlyGrowth' in info.keys() else None,
                'earnings_growth': round(info['earningsGrowth'], 2) if 'earningsGrowth' in info.keys() else None,
                'revenue_growth': round(info['revenueGrowth'], 2) if 'revenueGrowth' in info.keys() else None,
                'fifty_day_average': round(info['fiftyDayAverage'], 2) if 'fiftyDayAverage' in info.keys() else None,
                'two_hundred_day_average': round(info['twoHundredDayAverage'], 2) if 'twoHundredDayAverage' in info.keys() else None,
                'audit_risk': info['auditRisk'] if 'auditRisk' in info.keys() else None,
                'board_risk': info['boardRisk'] if 'boardRisk' in info.keys() else None,
                'compensation_risk': info['compensationRisk'] if 'compensationRisk' in info.keys() else None,
                'shareholder_rights_risk': info['shareHolderRightsRisk'] if 'shareHolderRightsRisk' in info.keys() else None,
                'overall_risk': info['overallRisk'] if 'overallRisk' in info.keys() else None
            }
            self.info_data[ticker] = useful_info_dict
    
    def get_companies_by_sector(self, sector):
        result_array = []
        for ticker in self.get_tickers():
            ticker_sector = self.info_data[ticker]['sector']
            if ticker_sector == sector:
                result_array += [ticker_sector]
        return result_array

    def save_sectors(self):
        result_array = []
        for ticker in self.get_tickers():
            ticker_sector = self.info_data[ticker]['sector']
            if not ticker_sector in result_array:
                result_array.append(ticker_sector)
        self.sectors = result_array

    def get_sectors(self):
        return self.sectors
    
    def set_growth_rates_by_sector(self):
        growth_rates_by_sector_dict = {}
        for sector in self.get_sectors():
            growth_rates_by_sector_dict[sector] = 0
            for ticker in self.get_tickers():
                if self.info_data[ticker]['sector'] == sector:
                    oldest = self.price_data[ticker].iloc[0]
                    current = self.price_data[ticker].iloc[-1]
                    growth = (current - oldest) * 100 / oldest
                    accumulated = growth_rates_by_sector_dict[sector] + growth
                    growth_rates_by_sector_dict[sector] = round(accumulated, 2)
        result_df = pd.DataFrame([growth_rates_by_sector_dict], index=['growth'])
        result_df_transposed = result_df.T
        result_df_sorted = result_df_transposed.sort_values(by='growth', ascending=False)
        self.growth_rates_by_sector = result_df_sorted

    def get_growth_rates_by_sector(self):
        return self.growth_rates_by_sector