import datetime as dt



HOLIDAYS = [
    "2018-01-01",
    "2018-02-15",
    "2018-02-16",
    "2018-02-19",
    "2018-02-20",
    "2018-02-21",
    "2018-04-05",
    "2018-04-06",
    "2018-04-30",
    "2018-05-01"
]

def getDayStr(n, date=None):
    assert(n != 0)
    delta = dt.timedelta(days=n)
    if not date:
        date = dt.datetime.today().date()
    else:
        date = dt.datetime.strptime(date, "%Y-%m-%d").date()
    result = str(date + delta)
    if isInHoliday(result):
        return getDayStr(delta / abs(delta), result)
    else:
        return result

def isInHoliday(date):
    format_d = dt.datetime.strptime(date, "%Y-%m-%d")
    week_day = format_d.weekday()
    if week_day >= 5 or date in HOLIDAYS:
        return True
    else:
        return False

def getAllDates(start_day, end_day):
    result = []
    while start_day <= end_day:
        if not isInHoliday(start_day):
            result.append(start_day)
        start_day = getDayStr(1, start_day)
    return result

def dateTransform(date, format):
    return dt.datetime.strptime(date, "%Y-%m-%d").strftime(format)

if __name__ == "__main__":
    assert(getDayStr)