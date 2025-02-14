from datetime import date,timedelta,datetime

time = datetime.now()-timedelta(1)
yesterday= time.strftime("%d-%m-%Y")
print("yesterday: ", yesterday)


time = datetime.now()
today = time.strftime("%d-%m-%Y")
print("Todat: ",today)



time = datetime.now()+timedelta(1)
tomarrow = time.strftime("%d-%m-%Y")
print("Tomarrow ",tomarrow)