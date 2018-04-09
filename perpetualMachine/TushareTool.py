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

    def getHistoryDetails(self, date, code):
        count = 5
        while count > 0:
            df = ts.get_tick_data(code, date, src="tt", retry_count=1, pause=0.3)
            if df is not None:
                result = df.head(10)["type"]
                return result
            else:
                time.sleep(3)
                count -= 1
        return None
