import datetime as dt



def getDayStr(n):
    delta = dt.timedelta(days=n)
    return str(dt.datetime.today().date() + delta)


if __name__ == "__main__":
    assert(getDayStr)