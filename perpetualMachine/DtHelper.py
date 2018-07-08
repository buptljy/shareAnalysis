import datetime as dt
import calendar


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

def today():
    return dt.datetime.today().strftime("%Y-%m-%d")

def getWeekStartDay(date):
    format_d = dt.datetime.strptime(date, "%Y-%m-%d")
    week_day = format_d.weekday()
    if week_day == 0:
        return date
    while week_day > 0:
        delta = dt.timedelta(days=-week_day)
        d = (format_d + delta).strftime("%Y-%m-%d")
        if d not in HOLIDAYS:
            return d
        week_day = week_day - 1
    return None

def getWeekEndDay(date):
    format_d = dt.datetime.strptime(date, "%Y-%m-%d")
    week_day = format_d.weekday()
    if week_day == 4:
        return date
    while (4 - week_day) > 0:
        delta = dt.timedelta(days=week_day)
        d = (format_d + delta).strftime("%Y-%m-%d")
        if d not in HOLIDAYS:
            return d
        week_day = week_day + 1
    return None

def getMonthStartDay(date):
    format_d = dt.datetime.strptime(date, "%Y-%m-%d")
    day = format_d.day - 1
    if day == 0:
        return date
    while day > 0:
        delta = dt.timedelta(days=-day)
        d = (format_d + delta).strftime("%Y-%m-%d")
        if d not in HOLIDAYS:
            return d
        day = day - 1
    return date

def getMonthEndtDay(date):
    format_d = dt.datetime.strptime(date, "%Y-%m-%d")
    (month_start, month_end) = calendar.monthrange(format_d.year, format_d.month)
    for day in range(month_end, month_start, -1):
        format_d.replace(day=day)
        d = format_d.strftime("%Y-%m-%d")
        if d not in HOLIDAYS:
            return d
    return None


if __name__ == "__main__":
    assert(getDayStr)