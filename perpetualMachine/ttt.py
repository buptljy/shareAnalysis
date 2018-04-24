#coding:utf-8
import matplotlib.pyplot as plt
import RedisCache
import DtHelper as dthp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import tushare as  ts

data = ts.get_concept_classified()
print(pd.DataFrame(data).head(10000))
