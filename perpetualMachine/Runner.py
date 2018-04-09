#coding:utf-8
import matplotlib.pyplot as plt
from pandas import DataFrame as df
import TushareTool
import DtHelper as dthp
import RedisCache
import MultiThreadHelper

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

    def getLimitupStocks(self):
        args = []
        stocks = self.tst.getStocks("all", self.start_day)[["name"]]
        # stocks = df({"name": ["123", "456", "123", "456"]}, index=["200019", "002888", "002864", "300722"])
        # stocks = df({"name": ["123"]}, index=["200019"])
        for index, data in stocks.iterrows():
            args.append([self.start_day, index])
        results = self.mth.runAsync("getLimitupStocks", args)
        filter_results = filter(lambda x: x is not None, list(results))
        print("get Limitup stocks, size: %s" % str(len(list(filter_results))))
        conn = self.cache.getConn()
        for result in filter_results:
            cacheKey = ":".join(["stock", "limitup", self.start_day])
            conn.lpush(cacheKey, result)

    # def runIndustryDaily(self):
    #     stocks = self.tst.getStocks("industry")
    #     print("Get industry stocks ....")
    #     for index, data in stocks.iterrows():
    #         cacheKey = ":".join(["stock", index, self.start_day])
    #         cacheData = self.cache.getCache(cacheKey)
    #         if self.cache.getCache(cacheKey):
    #             p_change =


if __name__ == "__main__":
    perp = Perpetual("2018-04-04")
    perp.getLimitupStocks()


