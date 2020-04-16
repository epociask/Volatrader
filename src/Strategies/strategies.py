from Helpers.Constants.Enums import Indicator, Candle, Pair
from SlackNotifier.PriceNotifications import getUpperNormalDistrubtion
from Trader.Indicators import IndicatorFunctions
from Helpers.TimeHelpers import convertNumericTimeToString
BUY, SELL = True, True
WAIT = False 
def getStrat(name: str):
    """
    returns strategy function with a list of indicators to use with it
    :param name: Name of strategy
    :returns: strategy function and list of indicators used w/ strategy
    """
    c = globals()[name]
    return c


class strategy():

    def __init__(self, pair: Pair, candleSize: Candle, principle: int):
        self.pair = pair
        self.candleSize = candleSize
        self.indicatorList = None
        self.principle = principle

    def checkSell(self, candle):
        return WAIT 


# class riskManager():                              ######PORTFOLIO ALLOCATION TODO
#
#     def __init__(self, principle: int):
#         self.principle = principle
#
#     def sellPercent(self, percent: float):
#         self.principle = self.principle - (percent )

class TEST_STRAT(strategy):
    
    def __init__(self, pair: Pair, candle: Candle, principle: int):
        super().__init__(pair, candle, principle)

    def checkBuy(self, candle):
        return BUY

class BBANDS_STRAT(strategy):

    def __init__(self, pair: Pair, candle: Candle, principle : int):
        super().__init__(pair, candle, principle)
        self.indicatorList = [Indicator.BBANDS]

    def checkBuy(self, candle):
        if candle['bbands']['valueUpperBand'] < candle['close']:
            return BUY

        return WAIT

class SIMPLE_BUY_STRAT(strategy):

    def __init__(self):
        pass
    def checkBuy(self, candle):
        if candle['3outside']['value'] != '0' or float(candle['invertedhammer']['value']) != "0":
            buyPrice = float(candle['close'])
            buyTime = candle['timestamp']

            return BUY

        return WAIT

class TEST_BUY_STRAT(strategy):
    def __init__(self, pair: Pair, candle: Candle, principle:int ):
        super().__init__(pair, candle, principle)
        self.dumbass = NATHAN_STRAT(pair, candle, 100)
        self.sdv = getUpperNormalDistrubtion(pair, candle, 300)

    def checkBuy(self, candle):
        bear = None
        for i in candle:
            if i != 'candle' and i != 'macdfix':
                print(i, candle[i])
                if candle[i]['value'] == '-100':
                    bear = True

        ind, _, _, = self.dumbass.checkBuy(candle)
        if float(candle['volume']) > self.sdv['2SD'] and float(candle['close']) < float(
                candle['open']) and bear is None and float(candle['fibonacciretracement']['value']) > float(
            candle['close']) and ind:
            return BUY

        else:
            return WAIT


class NATHAN_STRAT(strategy):

    def __init__(self, pair: Pair, candle: Candle, principle:int):
        super().__init__(pair, candle, principle)

    def checkBuy(self, candle):
        """
        Nathan Haile's genius strategy
        """
        if candle['macdfix']['valueMACDSignal'] > candle['macdfix']['valueMACD']:
            return BUY

        return WAIT


class CANDLESTICK_STRAT(strategy):

    def __init__(self, pair: Pair, candle: Candle, principle:int):
        super().__init__(pair, candle, principle)

    def checkBuy(self, candle):
        bullSigns = 0
        bearSigns = 0
        print(f"fib val; {candle['fibonacciretracement']['value']}")
        for value in candle:
            if value != 'candle':

                try:
                    if candle[value]['value'] == '100':
                        bullSigns += 1

                    elif candle[value]['value'] == '-100':
                        bearSigns += 1

                except Exception:
                    pass
        total = bullSigns - bearSigns
        if total >= 2 and (float(candle['fibonacciretracement']['value']) < float(candle['close'])) and \
                candle['longleggeddoji']['value'] == '100':
            print(total)
            return BUY

        return WAIT


class EMA_STRATEGY(strategy):
    def __init__(self, candles, period):
        self.emas = IndicatorFunctions.EMA(candles, period)
        self.period = 9
        self.count = 0

    def checkBuy(self, candle):
        if self.count < self.period:
            self.count+=1
            return WAIT

        if self.emas[self.count] > candle[4]:
            self.count+=1
            return BUY 

        self.count += 1 
        return WAIT


class FIFTY_MOVING_AVERAGE_STRATEGY(strategy):

    def __init__(self, pair: Pair, candle: Candle, principle:int):
        super().__init__(pair, candle, principle)
        self.candleLimit = 50
        self.arr = []
        self.candles = []
        self.indicators = {"SMA_50": [True], "RSI_14": [False], "UPTREND_4": [True], 'BB_20': [True, 'MOVING AVERAGE BB', 'UPPER BAND BB', 'LOWER BAND BB']}

    def checkBuy(self, candle):
        self.candles.append(candle)
        if len(self.arr) < self.candleLimit:
            self.arr.append(float(candle['close']))
            return WAIT


        self.arr.append(float(candle['close']))
        self.val_50 = IndicatorFunctions.SMA(self.arr, 50)[-1]
        self.bb = IndicatorFunctions.BB(candles, 20)
        if self.val_50 < candle['close'] and not IndicatorFunctions.DOWNTREND(self.candles, n=4):
            return BUY

        return WAIT 


    def checkSell(self, candle):
        if self.val_50 > candle['close'] and IndicatorFunctions.DOWNTREND(self.candles, n=4):
            return SELL
        return WAIT
        

class MA_STRATEGY(strategy):
    
    def __init__(self, pair: Pair, candle: Candle, principle:int):
        super().__init__(pair, candle, principle)
        self.arr = []
        self.candleLimit = 13
        self.indicators = {'SMA_13': [True], 'SMA_8': [True], 'SMA_5': [True], 'BB_20': [True, 'MOVING AVERAGE BB', 'UPPER BAND BB', 'LOWER BAND BB']}
        self.sdv = getUpperNormalDistrubtion(pair, candle, 500)
        self.prevCandle = None 


    def update(self, candle):
        if len(self.arr) < self.candleLimit:

            self.arr.append(float(candle['close']))
            # print("APPEDEND CANDLE CLOSE", self.arr)
            self.prevCandle = candle
            return WAIT
        else:
            self.arr.append(float(candle['close']))
            del self.arr[0]
            self.val_13 = IndicatorFunctions.SMA(self.arr, 13)[-1]
            self.val_8 = IndicatorFunctions.SMA(self.arr, 8)[-1] 
            self.val_5 = IndicatorFunctions.SMA(self.arr, 5)[-1] 
            self.rsi = IndicatorFunctions.RSI(self.arr)[-1]
            return None 

    def checkBuy(self, candle):

        if self.update(candle) is None:
    
            if (self.val_5 > self.val_13 and self.val_5 > self.val_8):
                self.arr = []
                return BUY

            self.prevCandle = candle
            return WAIT 


    def checkSell(self, candle):
        if self.update(candle) is None:
            if self.val_5 < self.val_13 and self.val_5 < self.val_8:
                return SELL

            return WAIT 
            
