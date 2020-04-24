import numpy as np 

cpdef SMA(double[:] closes, int period):
        cdef int length = len(closes)
        cdef float total = closes[length-period]
        cdef int i
        for i in xrange((length-period)+1, length):
                total += closes[i]
        return float(total/period)

cpdef UPTREND(candles, n=3):
        cdef int positives = 0
        if candles[len(candles)-n]['close'] <  candles[-1]['close']:   
                # temp = candles[len(candles)-n :len(candles)]
                # for candle in temp:
                #         if candle['close'] > candle['open']:
                #                 positives += 1 

                # if positives/2 > n:
                return True

        return False



cdef SDV(double[:] closes, period):
        cdef length = len(closes)
        cdef float mean = SMA(closes, period)
        cdef float x_i = 0.0
        cdef int i 
        for i in xrange((length - period), length):
                x_i += (closes[i] - mean) ** 2 
        return (x_i/(period-1))


cpdef FIB(list candles, int period):
        cdef float low = 100000
        cdef float high = 0
        cdef float diff
        cdef int i  
        cdef int length = len(candles)
        for i in xrange(length - period, length):
                if float(candles[i]['close']) < low and float(candles[i]['close'] > 1):
                        low = float(candles[i]['close'])
                if float(candles[i]['close']) > high:
                        high = float(candles[i]['close'])

        diff = high - low
        return (high - (0.236 * diff)), (high - (0.382 * diff)), (high - (0.618 * diff))



cpdef BOLINGER_BANDES(double[:] closes, int period):
#   * Middle Band = 20-day simple moving average (SMA)
#   * Upper Band = 20-day SMA + (20-day standard deviation of price x 2) 
#   * Lower Band = 20-day SMA - (20-day standard deviation of price x 2)
        cdef float sdv = SDV(closes, period)
        cdef float sma = SMA(closes, period)
        return (sma), (sma + sdv*2), (sma - sdv*2)


        
        
# cpdef EMA(np.array closes, int period):
# 	cdef int length = closes.shape[0]
#         cdef k = 2 / (period + 1)
#         cdef float[closes - period] emas
#         cdef int i 
#         cdef prevValue = SMA(closes.split(0, period), period)        
#         #EMA = (closes[i] * k) + (emas(i-period)(1-k))
#         for i in xrange((length-period) + 1, length):


                
