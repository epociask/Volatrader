import time
import indicators
import IndicatorFunctions
import numpy as np 

l = [{'open': 23.4, 'close': 24.5}] * 1000000
print("testing python")
start = time.time()
l1 = [e['close'] for e in l]
for index, val in enumerate(l1):
    if index >= 4:
        IndicatorFunctions.SMA(l1[0 : 4], 4)
end = time.time()
print(end - start)

start = time.time()

print("testing cython")
for index, val in enumerate(l1):
        if index >= 4:
            indicators.SMA(np.array(l1[0 : 4]), 4)
end = time.time()
print(end - start)


print("testing python")
start = time.time()
for index, val in enumerate(l):
    if index >= 4:
        IndicatorFunctions.UPTREND(l[0 : 4], 4)
end = time.time()
print(end - start)

start = time.time()

print("testing cython")
for index, val in enumerate(l):
        if index >= 4:
            indicators.UPTREND(np.array(l[0 : 4]), 4)
end = time.time()
print(end - start)



