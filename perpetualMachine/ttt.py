import tushare as ts
from pandas import DataFrame as df
import redis


rd = redis.Redis(host="101.200.171.13", port=6379, password="buptwind")
print(rd.keys())
# df = ts.get_tick_data('200019',date='2018-04-04')
# print(df.head(10))
# data = {"name":['google','google','google'],"marks":[100,200,300],"price":[1,2,3]}
# df1 = df(data)[["name"]]
# print(df1.equals(df({"name": ["google" for i in range(0, 3)]})))
# for index, data in df.iterrows():
#     print(data["name"])
a, b= 1, 2
print(a,b)