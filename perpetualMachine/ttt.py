import tushare as ts
from pandas import DataFrame as df
import redis


rd = redis.StrictRedis(host="101.200.171.13", port=6379, password="buptwind", decode_responses=True)
result = rd.hgetall(":".join(["stock", "industry", "2018-04-16"]))
print(len(result))
rd.delete(":".join(["stock", "industry", "2018-04-16"]))
for k in result:
    print(k, result[k])


# l = [1,2,4,5,3]
# l.sort()
# print(l)
# rd = redis.Redis(host="101.200.171.13", port=6379, password="buptwind")
# keys = rd.keys("stock:daily*04-10")
# for k in keys:
#     k = k.decode("utf-8")
#     print(k)
#     datas = rd.hgetall(k)
#     if len(list(datas["data".encode("utf-8")])) == 0:
#         print("=========================================%s " % k)
#         rd.delete(k)
# rd.hset("test1", "11", 2)
# print(rd.hget("test1", "22"))
# print(rd.keys())
# df = ts.get_tick_data('200019',date='2018-04-04')
# print(df.head(10))
# data = {"name":['google'],"marks":[100],"price":[1]}
# df1 = df(data).to_dict()
# print(df1)
# for k in df1:
#     print(k, )
# print(df1.equals(df({"name": ["google" for i in range(0, 3)]})))
# for index, data in df.iterrows():
#     print(data["name"])
# a, b= 1, 2
# print(a,b)