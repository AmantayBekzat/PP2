from datetime import date,timedelta,datetime

y=datetime.now()-timedelta(1)
t=datetime.now()+timedelta(1)

y=datetime.timestamp(y)

t=datetime.timestamp(t)
print(t-y)