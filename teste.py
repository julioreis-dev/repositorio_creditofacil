from time import time, sleep
from datetime import datetime, timedelta

x = datetime.today()
sleep(5)
y= datetime.today()
dif = y - x
print(dif)
if dif < timedelta(minutes=1):
    print('Aplicação não usa a API')

a = [18]
print(a[-1])