#coding:utf-8
import matplotlib.pyplot as plt
from pandas import DataFrame as df
from pandas import Series
import TushareTool
import DtHelper as dthp
import RedisCache
import MultiThreadHelper
import time

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

class Perpetual(object):

    def __init__(self, date = None):
        self.cache = RedisCache.RedisCache()
        self.tst = TushareTool.TushareTool()
        self.mth = MultiThreadHelper.MultiThreadHelper()
        if date is not None:
            self.start_day = date
        else:
            self.start_day = dthp.getDayStr(0)

    def getAllStocks(self):
        t1 = time.time()
        conn = self.cache.getConn()
        pipe = conn.pipeline()
        stocks = self.tst.getStocks("all", self.start_day)[["name"]]
        cacheKey = ":".join(["stock", "list", self.start_day])
        for index, data in stocks.iterrows():
            pipe.hset(cacheKey, str(index), data["name"])
        pipe.execute()
        t2 = time.time()
        print("Finish getAllStocks tasks, time cost: %s seconds" % str(t2 - t1))

    def getAllStockData(self):
        t1 = time.time()
        cnt = 0
        conn = self.cache.getConn()
        pipe = conn.pipeline()
        # stocks = self.tst.getStocks("all", self.start_day)[["name"]]
        all_stocks_cache_key = ":".join(["stock", "list", self.start_day])
        stocks = conn.hgetall(all_stocks_cache_key)
        sorted_keys = list(stocks.keys())
        sorted_keys = list(map(lambda x: x.decode("utf-8"), sorted_keys))
        # sorted_keys = list(filter(lambda x: x > "601965", sorted_keys))
        print("Handle %s stocks in getAllStockData" % str(len(sorted_keys)))
        # sorted_keys = [b"300742", b"300743"]
        sorted_keys.sort()
        for index in sorted_keys:
            cnt += 1
            if cnt % 30 == 0:
                print("Successfully get %s records in getAllStockData: %s , %s" % (str(cnt), time.time(), index))
                pipe.execute()
            code = str(index)
            cacheKey = ":".join(["stock", "daily", code, self.start_day])
            resultDF = self.tst.getStockData(self.start_day, code)
            if resultDF is not None:
                result_dict = df(resultDF).to_dict(orient="split")
                if len(list(result_dict["data"])) > 0:
                    pipe.hmset(cacheKey, result_dict)
            else:
                print("Fail to get %s in getAllStockData" % code)
        pipe.execute()
        t2 = time.time()
        print("Finish getAllStockData tasks, time cost: %s minutes" % str((t2 - t1)/60))

    def getLimitupStocks(self):
        t1 = time.time()
        cacheKey = ":".join(["stock", "limitup", self.start_day])
        conn = self.cache.getConn()
        pipe = conn.pipeline()
        all_stocks_cache_key = ":".join(["stock", "list", self.start_day])
        stocks = conn.hgetall(all_stocks_cache_key)
        sorted_keys = list(stocks.keys())
        # sorted_keys = ["300742", "300743"]
        sorted_keys.sort()
        for code in sorted_keys:
            stock_data_cache_key = ":".join(["stock", "daily", code, self.start_day])
            stock_data_cache_key_yesterday = ":".join(["stock", "daily", code, dthp.getDayStr(-1, self.start_day)])
            code_data = conn.hgetall(stock_data_cache_key)
            code_data_yesterday = conn.hgetall(stock_data_cache_key_yesterday)
            if code_data is not None and code_data_yesterday is not None:
                schema = code_data["columns"]
                close_index = list(schema).index("close")
                close_price = code_data["data"][0][close_index]
                close_price_yesterday = code_data_yesterday["data"][0][close_index]
                if float(close_price - close_price_yesterday)/float(close_price_yesterday) > 9.0:
                    pipe.sadd(cacheKey, code)
        pipe.execute()
        t2 = time.time()
        print("Finish getLimitupStocks tasks, time cost: %s minutes" % str((t2 - t1)/60))

if __name__ == "__main__":
    perp = Perpetual("2018-04-10")
    # perp.getAllStocks()
    # perp.getAllStockData()
    perp.getLimitupStocks()

# 601965
