import pandas as pd
import numpy as np
from scipy.stats import linregress
import ta


def getFunction(name: str):

    return globals()[name]


"""
Insert indicator graph logic here
"""



def BB(data, period=10, ndev=2):
    data = [e['close'] for e in data]
    data = pd.Series(data)
    indicator_bb = ta.volatility.BollingerBands(close=data, n=20, ndev=2)
    print (indicator_bb.bollinger_mavg().iat[-1])
    return {"MOVING AVERAGE BB" : indicator_bb.bollinger_mavg().iat[-1], "UPPER BAND BB": indicator_bb.bollinger_hband().iat[-1], "LOWER BAND BB": indicator_bb.bollinger_lband().iat[-1]}




def SMA(data, period=3) :
    ret = np.cumsum(data, dtype=float)
    ret[period:] = ret[period:] - ret[:-period]
    return ret[period - 1:] / period




def EMA(values, alpha = .3, epsilon = 0):

   if not 0 < alpha < 1:
      raise ValueError("out of range, alpha='%s'" % alpha)

   if not 0 <= epsilon < alpha:
      raise ValueError("out of range, epsilon='%s'" % epsilon)

   result = [None] * len(values)

   for i in range(len(result)):
       currentWeight = 1.0

       numerator     = 0
       denominator   = 0
       for value in values[i::-1]:
           numerator     += value * currentWeight
           denominator   += currentWeight

           currentWeight *= alpha
           if currentWeight < epsilon:
              break

       result[i] = numerator / denominator

   return result

def RSI(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi

def DOWNTREND(candles, n=3):
    #TODO REFORMAT DATA TO ONLY BE IN TYPE candle['open'] instead of data['candle']['open'] in TradeSession, Strategies, & Indicator functions

    if candles[len(candles)-n]['close'] <  candles[-1]['close']:
        return False

    return True


def UPTREND(candles, n=3):


    if candles[len(candles)-n]['close'] <  candles[-1]['close']:
        return True

    return False
