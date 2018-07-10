import sys
import datetime as dt
import pandas as pd
from perpetualMachine.tools.TushareTool import TushareTool
import perpetualMachine.tools.DtHelper as dthp


def getAccountProfit(a_stock_now, f_stock_origin):
    a_stock_month_origin = 0.0
    f_stock_month_origin = 0.0

    a_stock_week_origin = 0.0
    f_stock_week_origin = 0.0

    print(a_stock_now/a_stock_month_origin, a_stock_now/a_stock_week_origin)
    print(a_stock_now/f_stock_month_origin, a_stock_now/f_stock_week_origin)

def getIndex(code, date):
    tool = TushareTool()
    df = tool.getIndexTrend(date, code)
    return pd.DataFrame(df).head(1)["close"].values[0]



def runJob():
    if dt.datetime.now().hour < 6:
        today = dthp.getDayStr(-1, dthp.today())
    else:
        today = dthp.today()
    last_week_endday = dthp.getWeekEndDay(dthp.getDayStr(-7, today))
    last_month_endday = dthp.getMonthEndtDay(dthp.getDayStr(-30, today))
    code = "000001"
    today_index = getIndex(code, today)
    last_week_endday_index = getIndex(code, last_week_endday)
    last_month_endday_index = getIndex(code, last_month_endday)
    print(today_index, last_week_endday_index, last_month_endday_index)




if __name__ == "__main__":
    runJob()