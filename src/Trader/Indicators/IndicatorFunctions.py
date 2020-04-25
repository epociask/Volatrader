import indicators
import pandas as pd
import numpy as np
from scipy.stats import linregress
import ta
import statistics as stats
import test_indicators


def getFunction(name: str):

    return globals()[name]


# """"
# Insert indicator graph logic here
# """"

def ADX(data, n=14):
    low = [e['low'] for e in data]
    closes = [e['close'] for e in data]
    data = [e['high'] for e in data]
    highs = pd.Series(data) 
    low = pd.Series(low)
    closes = pd.Series(closes)
    adx_values = ta.trend.ADXIndicator(highs, low, closes, n) 
    return{ "ADX VALUE" :adx_values.adx().iat[-1], "DI+": adx_values.adx_neg().iat[-1], "DI-": adx_values.adx_pos().iat[-1]}





def BB(data, period=14):

    middle, upper, low = indicators.BOLINGER_BANDES(np.array([e['close'] for e in data]), period)
   
    return {"MOVING AVERAGE BB" : middle, "UPPER BAND BB": upper, "LOWER BAND BB": low}


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


def MOM(candles: list, period: int)->float:
    return test_indicators.MOMENTUM(np.array([e['close'] for e in candles]), period) 

def RSIDIVERGENCE(candles: list):
    fourteen = RSI(candles, 14)
    five = RSI(candles, 5)
    return fourteen - five 

def HAMMER(candles: list, n=3):

    if candles[-1]['close'] < candles[-1]['open']:
        return False 
    if DOWNTREND(candles, n=6 ):
        candles = candles[len(candles)-n : len(candles)-1]
        if candles[-1]['close'] < candles[-1]['open']:
            for i in range(len(candles)-1):
                
                if candles[i]['close'] > candles[i]['open']:
                    return False 

            print("looping for hammer")

            prevDifference = candles[len(candles)-1]['open'] - candles[len(candles)-1]['close']
            highDifference = candles[len(candles)-1]['open'] - candles[-1]['open']
            if highDifference < prevDifference:

                if (candles[len(candles)-1]['high'] - candles[len(candles)-1]['close'] ) > (candles[len(candles)-1]['open'] - candles[len(candles)-1]['close']):
                    print("HAMMER DETECTED")
                    return True 



    return False 


def FIB(candles , period=10):
    l1, l2, l3 = indicators.FIB(candles, period)

    return {    'LEVEL1': l1, 'LEVEL2': l2, 'LEVEL3': l3}


def MACD(closes, n_fast=12, n_slow=26 , n_sign= 9):
    # closes = np.array([e['close'] for e in closes])

    result_MACD = ta.trend.MACD(pd.Series(closes), n_fast, n_slow, n_sign)
    return {"MACD Line": result_MACD.macd().iat[-1], "MACD Histogram" : result_MACD.macd_diff().iat[-1], "Signal Line" : result_MACD.macd_signal().iat[-1]}

def SMA(data, period=3):
    ret = np.cumsum(data, dtype=float)
    ret[period:] = ret[period:] - ret[:-period]
    return ret[period - 1:] / period




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
    if candles[len(candles)-n]['close'] <  candles[-1]['close']:   
        temp = candles[len(candles)-n :len(candles)]
        for candle in temp:
            if candle['close'] < candle['open']:
                return True
        return False

    if candles[len(candles)-n]['close'] <  candles[-1]['close']:
        return False

    return True

BEAR_CANDLE = lambda candle :  True if candle['close'] < candle['open'] else False

BULL_CANDLE = lambda candle: True if candle['close'] > candle['open'] else False 
     
DIFFERENCE = lambda candle : (candle['open'] - candle['close']) if BEAR_CANDLE(candle) else (candle['close'] - candle['open'])

def PATTERNONNECKLINE(candles, n=3): #TODO FIX 

    sdv = stats.stdev([DIFFERENCE(e) for e in candles]) 
    mean = sum([DIFFERENCE(e) for e in candles])/len(candles)
    thirdCandle = candles[-3]
    secondCandle = candles[-2]
    firstCandle = candles[-1]
    if(mean + sdv *2) > DIFFERENCE(thirdCandle):
        if(int(firstCandle['close']) == int(thirdCandle['close']) and int(secondCandle['close']) == int(firstCandle['close'])):
            if BULL_CANDLE(thirdCandle) and BEAR_CANDLE(secondCandle) and BEAR_CANDLE(firstCandle):
                if firstCandle['close'] >= thirdCandle['close'] and firstCandle['open'] <= thirdCandle['open']:
                    return True 


    return False 

calculated = False 
mean = None 
def calcSDV(candles):
    global calculated 
    calculated =  stats.stdev([DIFFERENCE(e) for e in candles])
    mean = sum([DIFFERENCE(e) for e in candles])/len(candles)


def PATTERNMORNINGSTAR(candles, n=3): #TODO FIX 
    global calculated
    global mean
    c1, c2, c3 = candles[-3], candles[-2], candles[-1]

    if calculated is False:
        calcSDV(candles)

    if BEAR_CANDLE(c1) and BULL_CANDLE(c2) and BULL_CANDLE(c3):
        if ((c2['high'] - c2['open']) > DIFFERENCE(c2)) and((c2['close'] - c2['low']) > DIFFERENCE(c2)):
            if c3['open'] > c1['close'] and c3['close'] < c1['open']:
                if DIFFERENCE(c1) > DIFFERENCE(c2) and DIFFERENCE(c1) > DIFFERENCE(c3) and DIFFERENCE(c1) > DIFFERENCE(c3): 
                    if c2['open'] < c1['close'] and c3['open'] > c2['open']:
                        if DIFFERENCE(c1) > (3 * DIFFERENCE(c2)):
                            if DOWNTREND(candles[0: len(candles)-2], n=5):
                                return True 

    return False 
def PATTERNTHREELINESTRIKE(candles, n=4):
    
    candle1, candle2, candle3, candle4 = candles[-4], candles[-3], candles[-2], candles[-1]

    if BEAR_CANDLE(candle1) and BEAR_CANDLE(candle2) and BEAR_CANDLE(candle3) and BULL_CANDLE(candle4):
        for candle in [candle1, candle2, candle3]:
            if candle['open'] > candle4['close'] or candle['close'] < candle4['open']:
                return False 
        
        if candle3['open'] <= candle2['close'] and candle2['open'] <= candle1['close']:
            return True 

    return False 

def PATTERNTHREELINESTRIKEBEARISHREVERSAL(candles, n=4):
    
    candle1, candle2, candle3, candle4 = candles[-4], candles[-3], candles[-2], candles[-1]

    if BULL_CANDLE(candle1) and BULL_CANDLE(candle2) and BULL_CANDLE(candle3) and BEAR_CANDLE(candle4):
        for candle in [candle1, candle2, candle3]:
            if candle['open'] > candle4['open'] or candle['close'] < candle4['close']:
                return False 
        
        if candle3['open'] >= candle2['close'] and candle2['open'] >= candle1['close']:
            return True 

    return False 
def PATTERNTHREEINSIDE(candles, n=3):
    #  a large down candle, SOON 
    #  a smaller up candle contained within the prior candle, xx 
    #  another up candle that closes above the close of the second candle.

    sdv = stats.stdev([DIFFERENCE(e) for e in candles]) 
    mean = sum([DIFFERENCE(e) for e in candles])/len(candles)
    thirdCandle = candles[-3]
    secondCandle = candles[-2]
    firstCandle = candles[-1]

    #TODO normal distribution of open/close differences to figure out what constitutes as a LARGE candle 

    if BEAR_CANDLE(thirdCandle):
        if DIFFERENCE(thirdCandle) > (mean + 2 * sdv):
            if BULL_CANDLE(secondCandle):
                if secondCandle['close'] >= thirdCandle['close'] and secondCandle['open'] <= thirdCandle['open']:
                    if BULL_CANDLE(firstCandle) and firstCandle['close'] > secondCandle['close']:
                        if DIFFERENCE(thirdCandle) > DIFFERENCE(secondCandle) and DIFFERENCE(thirdCandle) > DIFFERENCE(firstCandle):
                            return True 

    return False  

def PATTERNTHREEBULLISHSOLDIERS(candles, n=3):
    thirdCandle = candles[-3]
    secondCandle = candles[-2]
    firstCandle = candles[-1]

    if BULL_CANDLE(thirdCandle):
        if BULL_CANDLE(secondCandle):     
            if BULL_CANDLE(firstCandle):      
                if secondCandle['open'] == thirdCandle['close'] and firstCandle['open'] >= secondCandle['close']:
                    return True 

    return False

def PATTERNBEARISHENGULFING(candles, n=3):
    c1, c2, c3 = candles[-3], candles[-2], candles[-1]
    if UPTREND(candles[0 : len(candles)-2], n=3):
        if BEAR_CANDLE(c2) and BULL_CANDLE(c1) and BEAR_CANDLE(c3):
            print("here")
            if c1['high'] > c2['close'] and c1['low'] < c2['open']:
                if (DIFFERENCE(c2) * 2) <= DIFFERENCE(c3):
                    return True 


    return False 


def PATTERNBULLISHHARAME(candles, n=2):

    c1, c2 = candles[-2], candles[-1]

    if DOWNTREND(candles[len(candles) -5: len(candles)]):
        if BEAR_CANDLE(c1) and BULL_CANDLE(c2):
            if DIFFERENCE(c1) >=( DIFFERENCE(c2)* 4):
                if c2['open'] > c1['close']:
                    return True 


    return False 

def PATTERNTWEEZER(candles, n=3):
    c1, c2, c3 = candles[-3], candles[-2], candles[-1]

    if BEAR_CANDLE(c1) and BEAR_CANDLE(c2):
        if c2['open'] == c3['close']:
            return True 

    return False 


def PATTERNTHREEBEARISHSOLDIERS(candles, n=3):
    thirdCandle = candles[-3]
    secondCandle = candles[-2]
    firstCandle = candles[-1]

    if BEAR_CANDLE(thirdCandle):
        if BEAR_CANDLE(secondCandle):     
            if BEAR_CANDLE(firstCandle):      
                if secondCandle['open'] == thirdCandle['close'] and firstCandle['open'] == secondCandle['close']:
                    return True 

    return False  


def UPTREND(candles, n=3):

    positives = 0
    if candles[len(candles)-n]['close'] <  candles[-1]['close']:   
        temp = candles[len(candles)-n :len(candles)]
        for candle in temp:
            if candle['close'] > candle['open']:
                positives += 1 
        

    if positives/2 > n:
        return True

    return False


candle3 = {'open': 40, 'close': 30}
candle2 = {'open': 30, 'close': 20}
candle1 = {'open':20, 'close': 11}
candle0 = {'open':10, 'close': 50}
l = [candle3, candle2, candle1, candle0]

print(PATTERNTHREELINESTRIKE(l))

