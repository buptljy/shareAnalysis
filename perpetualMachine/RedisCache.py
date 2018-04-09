import redis





class RedisCache(object):

    def __init__(self):
        self.conn = redis.Redis(host="101.200.171.13", port=6379, password="buptwind")

    def getConn(self):
        return self.conn

    def setCache(self, key, value, ttl=0):
        self.conn.set(key, value, ttl)

    def getCache(self, key):
        return self.conn.get(key)