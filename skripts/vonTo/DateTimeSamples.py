from datetime import date
from datetime import datetime
from datetime import timedelta

today = date.today()
print(today)

print(today.day, today.month, today.year, today.weekday())

today = datetime.now()
print(today)

t = datetime.time(datetime.now())

print(t)

td = timedelta(hours=1)

t = datetime.now()

r = t + td

print(r)




