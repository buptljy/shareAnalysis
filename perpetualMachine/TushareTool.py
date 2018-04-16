import tushare as ts
from pandas import DataFrame as df
import asyncio
import time



class TushareTool(object):

    def __init__(self):
        pass

    def getStocks(self, catogary, date):
        print("getting stocks..... %s : %s" % (date, catogary))
        if catogary == "all":
            return df(ts.get_stock_basics(date))
        elif catogary == "industry":
            return df(ts.get_industry_classified())

    def getStockData(self, date, code):
        count = 5
        while count > 0:
            try:
                # df = ts.get_hist_data(code, start=date, end=date, retry_count=1)
                df = ts.get_k_data(code, start=date, end=date, retry_count=1)
                if df is not None:
                    result = df.head(1)
                    return result
                else:
                    time.sleep(3)
                    count -= 1
            except IOError:
                print("IOError in getStockData")
                time.sleep(3)
                count -= 1
        return None

    def getIndustryStocks(self):
        count = 3
        while count > 0:
            try:
                df = ts.get_industry_classified(standard="sina")
                if df is not None:
                    return df
                else:
                    time.sleep(3)
                    count -= 1
            except IOError:
                print("IOError in getIndustryStocks")
                time.sleep(3)
                count -= 1
        return None

    def getHistoryDetails(self, date, code):
        count = 5
        while count > 0:
            try:
                df = ts.get_tick_data(code, date, src="tt", retry_count=1)
                if df is not None:
                    result = df.head(10)["type"]
                    return result
                else:
                    time.sleep(3)
                    count -= 1
            except IOError:
                time.sleep(3)
                count -= 1
        return None
