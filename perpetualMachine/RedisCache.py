import redis





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

    def setCache(self, key, value, ttl=0):
        self.conn.set(key, value, ttl)

    def getCache(self, key):
        return self.conn.get(key)