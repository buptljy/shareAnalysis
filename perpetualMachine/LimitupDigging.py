#coding:utf-8
import matplotlib.pyplot as plt
import RedisCache
import DtHelper as dthp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook



plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


cache = RedisCache.RedisCache()
industry_data = cache.getIndustryData("2018-04-18")
industry_data_df = pd.DataFrame(list(dict(industry_data).items()), columns=['code', 'industry'])
all_industries = industry_data_df["industry"].unique()
start_day = "2018-04-01"
end_day = "2018-04-16"
limitup_data = {}

for date in dthp.getAllDates(start_day, end_day):
    limitup_data_daily = cache.getLimitupData(date)
    if limitup_data_daily is None:
        limitup_data[date] = pd.DataFrame([], columns=["code"])
    else:
        limitup_data[date] = pd.DataFrame(list(limitup_data_daily), columns=["code"])

# 1. 涨停股票趋势图
# result = []
# for date in dthp.getAllDates(start_day, end_day):
#     limitup_num = pd.DataFrame(limitup_data[date]).shape[0]
#     result.append((date, limitup_num))
# x_ticks_labels = list(map(lambda x: dthp.dateTransform(str(x[0]), "%d-%m-%Y"), result))
# x_datas = np.arange(0, len(result), 1)
# y_datas = list(map(lambda x: x[1], result))
# fig, ax = plt.subplots(figsize=(15, 15))
# ax.plot(x_datas, y_datas)
# ax.set_xticks(x_datas)
# ax.set_xticklabels(x_ticks_labels, rotation="vertical", fontsize=6)
# fig.autofmt_xdate()
# ax.grid(True)
# plt.show()

# 2. 行业趋势图
# result = {}
# for industry in all_industries:
#     result[industry] = []
#     for date in dthp.getAllDates(start_day, end_day):
#         result[industry].append([date, 0])
# for date in dthp.getAllDates(start_day, end_day):
#     joined_df = pd.DataFrame(limitup_data[date]).set_index("code")\
#         .join(industry_data_df.set_index("code"))
#     agg_joined_df = joined_df.reset_index().groupby(["industry"]).agg("count")
#     for index, data in pd.DataFrame(agg_joined_df).iterrows():
#         industry = index
#         limitup_num = data["code"]
#         replace_index = list(result[industry]).index([date, 0])
#         result[industry][replace_index] = [date, limitup_num]
#
# fig, ax = plt.subplots(figsize=(15, 15))
# x_datas = np.arange(0, len(dthp.getAllDates(start_day, end_day)), 1)
# x_ticks_labels = list(map(lambda x: dthp.dateTransform(str(x), "%d-%m-%Y"),
#                           dthp.getAllDates(start_day, end_day)))
# ax.set_xticks(x_datas)
# ax.set_xticklabels(x_ticks_labels, rotation="vertical", fontsize=6)
# legend = []
# for industry in result:
#     datas = result[industry]
#     if len(list(filter(lambda x: x[1] > 1, datas))) > 0:
#         legend.append(industry)
#         y_datas = list(map(lambda x: x[1], datas))
#         ax.plot(x_datas, y_datas)
# fig.autofmt_xdate()
# ax.grid(True)
# plt.legend(legend, loc='upper center', bbox_to_anchor=(0.5, 1.05),
#           ncol=3, fancybox=True, shadow=True)
# plt.show()

# 3. 首阴反包策略
result = []
all_count = 0
success_count = 0
all_stocks = dict(cache.getAllStocks(dthp.getDayStr(-1, start_day))).keys()
for date in dthp.getAllDates(start_day, end_day):
    date = "2018-04-13"
    limitup_stocks = cache.getLimitupData(date)
    limitup_records = list(map(lambda x: [x, x], list(limitup_stocks)))
    limitup_df = pd.DataFrame.from_records(limitup_records, columns=["a", "b"]).set_index("a")
    date_df = pd.DataFrame(cache.getStockListDetails(all_stocks, date)).set_index("code")
    date_df_y = pd.DataFrame(cache.getStockListDetails(all_stocks, dthp.getDayStr(-1, date))).set_index("code")
    date_df_t = pd.DataFrame(cache.getStockListDetails(all_stocks, dthp.getDayStr(1, date))).set_index("code")
    date_df_t.columns = list(map(lambda x: str(x) + "_t", date_df_t.columns))
    # we get all the negtive stocks for $date
    filter_date_df = date_df[(date_df.close < date_df.open)]
    # we get all the positive stocks for $date_y
    filter_date_df_y = date_df_y[(date_df_y.close > date_df_y.open)]
    filter_date_df_y = limitup_df.join(filter_date_df_y)
    filter_date_df_y.columns = list(map(lambda x: str(x) + "_y", filter_date_df_y.columns))
    # join date and date-1  with shouyinfanbao strategy
    first_df = filter_date_df.join(filter_date_df_y)
    filter_first_df = first_df[(first_df.close_y > first_df.open_y) & (first_df.close_y < first_df.close)]
    print("we get {} stocks for {}".format(str(filter_first_df.shape[0]), date))
    second_df = filter_first_df.join(date_df_t)
    success_df = second_df[(second_df.close_t > second_df.open_t)]
    fail_df = second_df[(second_df.close_t < second_df.open_t)]
    print("success {} stocks, fail {} stocks".format(success_df.shape[0], fail_df.shape[0]))




























