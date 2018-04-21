#coding:utf-8
import matplotlib.pyplot as plt
import RedisCache
import DtHelper as dthp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

sales = [['Jones LLC', 150, 200, 50],
         ['Alpha Co', 200, 210, 90],
         ['Blue Inc', 140, 215, 95]]
labels = ['account', 'Jan', 'Feb']
df = pd.DataFrame.from_records(sales, columns=labels)
print(1)