#coding:utf-8
import matplotlib.pyplot as plt
import RedisCache
import DtHelper as dthp
import pandas as pd
import numpy as np



plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


cache = RedisCache.RedisCache()
industry_data = cache.getIndustryData("2018-04-18")
industry_data_df = pd.DataFrame(list(dict(industry_data).items()), columns=['code', 'industry'])
all_industries = industry_data_df["industry"].unique
start_day = "2018-04-01"
end_day = "2018-04-18"
limitup_data = {}

x_data = []
i = 0
while start_day <= end_day:
    if not dthp.isInHoliday(start_day):
        i += 1
        x_data.append(i)
        limitup_data_daily = cache.getLimitupData(start_day)
        limitup_data[start_day] = pd.DataFrame(list(limitup_data_daily), columns=["code"])
    start_day = dthp.getDayStr(1, start_day)

result = {}
for date in limitup_data:
    limitup_stocks_df = limitup_data[date]
    date_result_df = pd.DataFrame(limitup_stocks_df).set_index("code").join(industry_data_df.set_index("code"))
    r = date_result_df.groupby(["code"]).agg(["count"])
    result[date] = r


