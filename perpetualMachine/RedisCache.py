import redis
import pandas as pd




class RedisCache(object):

    def __init__(self):
        self.conn = redis.StrictRedis(host="101.200.171.13", port=6379, password="buptwind", decode_responses=True)

    def getConn(self):
        return self.conn

    def getIndustryData(self, start_day):
        cacheKey = ":".join(["stock", "industry", start_day])
        return self.conn.hgetall(cacheKey)

    def getLimitupData(self, start_day):
        cacheKey = ":".join(["stock", "limitup", start_day])
        return self.conn.smembers(cacheKey)

    def getAllStocks(self, start_day):
        cacheKey = ":".join(["stock", "list", start_day])
        return self.conn.hgetall(cacheKey)

    def getStockDetails(self, code, start_day):
        result = {}
        cacheKey = ":".join(["stock", "daily", code, start_day])
        stock_data = self.conn.hgetall(cacheKey)
        if stock_data is not None and len(stock_data) > 0 and len(self.str2List(stock_data["data"])) > 1:
            schema = self.str2List(str(stock_data["columns"]))
            datas = self.str2List(stock_data["data"])
            for i in range(0, len(schema)):
                result[schema[i]] = datas[i]
            return result
        else:
            return None

    def getStockListDetails(self, codes, start_day):
        pipe = self.conn.pipeline()
        for code in codes:
            cacheKey = ":".join(["stock", "daily", code, start_day])
            pipe.hgetall(cacheKey)
        pipe_result = pipe.execute()
        filtered_pipe_result = filter(lambda stock_data: stock_data is not None
                                        and len(stock_data) > 0
                                        and len(self.str2List(stock_data["data"])) > 1, pipe_result)
        result = []
        schema = []
        for stock_data in filtered_pipe_result:
            schema = self.str2List(str(stock_data["columns"]))
            datas = self.str2List(stock_data["data"])
            result.append(datas)
        return_df = pd.DataFrame.from_records(result, columns=schema)
        return return_df

    def setCache(self, key, value, ttl=0):
        self.conn.set(key, value, ttl)

    def getCache(self, key):
        return self.conn.get(key)

    def str2List(self, s):
        return str(s).replace("[", "").replace("]", "").replace(" ", "").replace("'", "").split(",")