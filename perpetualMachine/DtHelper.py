import datetime as dt



def getDayStr(n, date=None):
    delta = dt.timedelta(days=n)
    if not date:
        date = dt.datetime.today().date()
    else:
        date = dt.datetime.strptime(date, "%Y-%m-%d").date()
    return str(date + delta)

if __name__ == "__main__":
    assert(getDayStr)