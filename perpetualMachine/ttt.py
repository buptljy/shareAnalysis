#coding:utf-8
import matplotlib.pyplot as plt
import RedisCache
import DtHelper as dthp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook


sales = [["Jones LLC"]]
sales = sales * 2
labels = ['account', "dd"]
df = pd.DataFrame.from_records(sales, columns=labels).set_index()
print(1)