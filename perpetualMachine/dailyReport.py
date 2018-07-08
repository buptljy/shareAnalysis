import sys
import TushareTool as tst
import DtHelper as dthp

def getAccountProfit(a_stock_now, f_stock_origin):
    a_stock_month_origin = 0.0
    f_stock_month_origin = 0.0

    a_stock_week_origin = 0.0
    f_stock_week_origin = 0.0

    print(a_stock_now/a_stock_month_origin, a_stock_now/a_stock_week_origin)
    print(a_stock_now/f_stock_month_origin, a_stock_now/f_stock_week_origin)

def getIndexTrend():




def runJob():
    getAccountProfit(float(sys.argv[1]), float(sys.argv[2]))

    print()




if __name__ == "__main__":
    runJob()