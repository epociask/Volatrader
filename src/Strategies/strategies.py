from Helpers.Constants.Enums import Indicator, Candle, Pair
from SlackNotifier.PriceNotifications import getUpperNormalDistrubtion
from Trader.Indicators import IndicatorFunctions
from Helpers.TimeHelpers import convertNumericTimeToString

strats = ['THREELINESTRIKE_STRATEGY', 'FIFTY_MOVING_AVERAGE_STRATEGY']
BUY, SELL = True, True
HOLD = False 
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
        return HOLD 


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

# class BBANDS_STRATEGY(strategy):

#     def __init__(self, pair: Pair, candle: Candle, principle : int):
#         super().__init__(pair, candle, principle)
#         self.indicatorList = [Indicator.BBANDS]

#     def checkBuy(self, candle):
    

#     def checkSell(self, )

class SIMPLE_BUY_STRAT(strategy):

    def __init__(self):
        pass
    def checkBuy(self, candle):
        if candle['3outside']['value'] != '0' or float(candle['invertedhammer']['value']) != "0":
            buyPrice = float(candle['close'])
            buyTime = candle['timestamp']

            return BUY

        return HOLD

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
            return HOLD

class THREELINESTRIKE_STRATEGY(strategy):

    def __init__(self, pair: Pair, candle: Candle, principle:int):
        super().__init__(pair, candle, principle)
        self.candleLimit = 100
        self.candles = []
        self.indicators = ['PATTERNTHREELINESTRIKE_3', 'PATTERNBEARISHENGULFING_3']
        self.sdv = getUpperNormalDistrubtion(pair, candle, 300)

        

    def checkBuy(self, candle):
        self.candles.append(candle)
        if len(self.candles) < self.candleLimit:
            return HOLD

        self.candles.pop(0)
        if IndicatorFunctions.PATTERNTHREELINESTRIKE(self.candles):
            print("indication")
            return BUY 


        return HOLD

        

class FIFTY_MOVING_AVERAGE_STRATEGY(strategy):

    def __init__(self, pair: Pair, candle: Candle, principle:int):
        super().__init__(pair, candle, principle)
        self.candleLimit = 50
        self.arr = []
        self.candles = []
        self.indicators = ["SMA_50", "UPTREND_5", 'RSI_14', "SMA_15", 'PATTERNTHREELINESTRIKE_3']
        self.sdv = getUpperNormalDistrubtion(pair, candle, 500)


    def checkBuy(self, candle):
        self.candles.append(candle)
        if len(self.arr) < self.candleLimit:
            self.arr.append(float(candle['close']))
            return HOLD

        self.arr.pop(1)
        self.candles.pop(1)
        self.arr.append(float(candle['close']))
        self.val_50 = IndicatorFunctions.SMA(self.arr, 50)[-1]
        self.val_15 = IndicatorFunctions.SMA(self.arr, 15)[-1]
        self.rsi = IndicatorFunctions.RSI(self.arr, 14)[-1]


        if self.val_50 < candle['close'] and self.val_15 < candle['close'] and IndicatorFunctions.UPTREND(self.candles, n=3) and self.sdv['3SD'] > candle['volume'] and self.rsi < 70:
            self.passed = True 
            return BUY


        self.passed = False 

        return HOLD 


    def checkSell(self, candle):
        if (self.val_50 > candle['close'] and IndicatorFunctions.DOWNTREND(self.candles, n=4) and not self.passed) or self.rsi > 70:
            return SELL
        return HOLD
        

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
            return HOLD
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
            return HOLD 


    def checkSell(self, candle):
        if self.update(candle) is None:
            if self.val_5 < self.val_13 and self.val_5 < self.val_8:
                return SELL

            return HOLD 
            
