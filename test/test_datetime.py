import datetime as DT

time_start = DT.datetime.now()

# code
num = 0
for i in range(10000):
    num = num + 1

time_end = DT.datetime.now()

interval = time_end - time_start
interval = interval.total_seconds() * 1000
print("{} ms".format(interval))