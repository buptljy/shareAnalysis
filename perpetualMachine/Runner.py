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
        cnt = 0
        for index, data in stocks.iterrows():
            cnt += 1
            pipe.hset(cacheKey, str(index), data["name"])
        pipe.execute()
        t2 = time.time()
        print("Finish getAllStocks tasks, stock size: %s time cost: %s seconds" % (str(cnt), str(t2 - t1)))

    def getAllStockData(self, rerun=False):
        t1 = time.time()
        cnt = 0
        cnt_in = 0
        conn = self.cache.getConn()
        pipe = conn.pipeline()
        # stocks = self.tst.getStocks("all", self.start_day)[["name"]]
        all_stocks_cache_key = ":".join(["stock", "list", self.start_day])
        if not rerun:
            stocks = conn.hgetall(all_stocks_cache_key)
            sorted_keys = list(stocks.keys())
            sorted_keys.sort()
            reRunCacheKey = ":".join(["stock", "rerun", self.start_day])
            originalKey = ""
        else:
            data_key = ":".join(["stock", "rerun", self.start_day])
            sorted_keys = conn.smembers(data_key)
            reRunCacheKey = ":".join(["stock", "rerun", "1", self.start_day])
            originalKey = data_key
        print("Handle %s stocks in getAllStockData" % str(len(sorted_keys)))
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
                    cnt_in += 1
                    pipe.hmset(cacheKey, result_dict)
                else:
                    pipe.sadd(reRunCacheKey, code)
            else:
                print("Fail to get %s in getAllStockData" % code)
        pipe.execute()
        # rerun rename key
        if rerun and originalKey != "":
            conn.delete(originalKey)
            conn.rename(reRunCacheKey, originalKey)
        t2 = time.time()
        print("Finish getAllStockData tasks, %s stocks, %s in, time cost: %s minutes" % (str(cnt), str(cnt_in), str((t2 - t1)/60)))

    def getLimitupStocks(self):
        t1 = time.time()
        cacheKey = ":".join(["stock", "limitup", self.start_day])
        conn = self.cache.getConn()
        pipe = conn.pipeline()
        all_stocks_cache_key = ":".join(["stock", "list", self.start_day])
        stocks = conn.hgetall(all_stocks_cache_key)
        print("Calculate %s stocks in getLimitupStocks" % len(stocks))
        sorted_keys = list(stocks.keys())
        sorted_keys.sort()
        cnt = 0
        cnt_limitup = 0
        cnt_no_data = 0
        cnt_no_data_yesterday = 0
        for code in sorted_keys:
            cnt += 1
            if cnt % 1000 == 0:
                print("Successfully get %s records in getLimitupStocks: %s " % (str(cnt), time.time()))
            stock_data_cache_key = ":".join(["stock", "daily", code, self.start_day])
            stock_data_cache_key_yesterday = ":".join(["stock", "daily", code, dthp.getDayStr(-1, self.start_day)])
            code_data = conn.hgetall(stock_data_cache_key)
            code_data_yesterday = conn.hgetall(stock_data_cache_key_yesterday)
            if code_data is not None and code_data_yesterday is not None \
                    and len(code_data) > 0 and len(code_data_yesterday) > 0\
                    and len(self.str2List(code_data["data"])) > 1 and len(self.str2List(code_data_yesterday["data"])) > 1:
                try:
                    schema = self.str2List(str(code_data["columns"]))
                    close_index = list(schema).index("close")
                    close_price = self.str2List(code_data["data"])[close_index]
                    close_price_yesterday = self.str2List(code_data_yesterday["data"])[close_index]
                    p_change = float(float(close_price) - float(close_price_yesterday))/float(close_price_yesterday)
                    if p_change > 0.09:
                        cnt_limitup += 1
                        pipe.sadd(cacheKey, code)
                except Exception as err:
                    print(code)
                    raise err
            else:
                if code_data is None or len(code_data) <= 0 or len(code_data["data"]) <= 0:
                    cnt_no_data += 1
                elif code_data_yesterday is None or len(code_data_yesterday) <= 0 or len(code_data_yesterday["data"]) <= 0:
                    cnt_no_data_yesterday += 1
        pipe.execute()
        t2 = time.time()
        print("Finish getLimitupStocks tasks, %s limitup, %s no data today, %s no data yesterday, time cost: %s minutes" % (str(cnt_limitup), str(cnt_no_data), str(cnt_no_data_yesterday), str((t2 - t1)/60)))

    def getIndustryStock(self):
        t1 = time.time()
        industry_stocks = df(self.tst.getIndustryStocks())
        conn = self.cache.getConn()
        pipe = conn.pipeline()
        cacheKey = ":".join(["stock", "industry", self.start_day])
        cnt = 0
        for index, data in industry_stocks.iterrows():
            cnt += 1
            code = data["code"]
            industry = data["c_name"]
            pipe.hset(cacheKey, code, industry)
        pipe.execute()
        t2 = time.time()
        print("Finish getIndustryStock tasks, get %s stocks, time cost: %s" %  (str(cnt), str((t2 - t1)/60)))

    def str2List(self, s):
        return str(s).replace("[", "").replace("]", "").replace(" ", "").replace("'", "").split(",")

if __name__ == "__main__":
    start_date = "2018-01-01"
    end_date = "2018-04-20"
    for date in dthp.getAllDates(start_date, end_date):
        print("Running %s" % start_date)
        perp = Perpetual(start_date)
        perp.getAllStocks()
        perp.getAllStockData()
        time.sleep(60)
        perp.getAllStockData(True)
        perp.getLimitupStocks()
        perp.getIndustryStock()
        time.sleep(15)


# 601965
