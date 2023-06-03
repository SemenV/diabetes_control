from datetime import date, timedelta, datetime
dtStart = datetime.now()
dtStart = dtStart.replace(hour=0, minute=0, second=0, microsecond=0)
dtStart.strftime('%Y-%m-%d')
print(dtStart)
dtEnd = datetime.now()
dtEnd = dtEnd.replace(hour=23, minute=59, second=59, microsecond=0)
print(dtEnd)

test = date(2023, 5, 2)
print(test)