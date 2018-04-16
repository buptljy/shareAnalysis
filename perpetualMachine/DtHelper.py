import datetime as dt



HOLIDAYS = [
    "2018-04-05",
    "2018-04-06"
]

def getDayStr(n, date=None):
    delta = dt.timedelta(days=n)
    if not date:
        date = dt.datetime.today().date()
    else:
        date = dt.datetime.strptime(date, "%Y-%m-%d").date()
    return str(date + delta)

def isInHoliday(date):
    format_d = dt.datetime.strptime(date, "%Y-%m-%d")
    week_day = format_d.weekday()
    if week_day >= 5 and date not in HOLIDAYS:
        return True
    else:
        return False

if __name__ == "__main__":
    assert(getDayStr)