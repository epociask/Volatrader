from Helpers.Constants.Enums import Indicator, Candle, Pair
from SlackNotifier.PriceNotifications import getUpperNormalDistrubtion
from Trader.Indicators import IndicatorFunctions

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

    def checkSell(self, data):
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

    def checkBuy(self, data):
        return BUY

class BBANDS_STRAT(strategy):

    def __init__(self, pair: Pair, candle: Candle, principle : int):
        super().__init__(pair, candle, principle)
        self.indicatorList = [Indicator.BBANDS]

    def checkBuy(self, data):
        if data['bbands']['valueUpperBand'] < data['candle']['close']:
            return BUY

        return WAIT

class SIMPLE_BUY_STRAT(strategy):

    def __init__(self):
        pass
    def checkBuy(self, data):
        if data['3outside']['value'] != '0' or float(data['invertedhammer']['value']) != "0":
            buyPrice = float(data['candle']['close'])
            buyTime = data['candle']['timestamp']

            return BUY

        return WAIT

class TEST_BUY_STRAT(strategy):
    def __init__(self, pair: Pair, candle: Candle, principle:int ):
        super().__init__(pair, candle, principle)
        self.dumbass = NATHAN_STRAT(pair, candle, 100)
        self.sdv = getUpperNormalDistrubtion(pair, candle, 300)

    def checkBuy(self, data):
        bear = None
        for i in data:
            if i != 'candle' and i != 'macdfix':
                print(i, data[i])
                if data[i]['value'] == '-100':
                    bear = True

        ind, _, _, = self.dumbass.checkBuy(data)
        if float(data['candle']['volume']) > self.sdv['2SD'] and float(data['candle']['close']) < float(
                data['candle']['open']) and bear is None and float(data['fibonacciretracement']['value']) > float(
            data['candle']['close']) and ind:
            return BUY

        else:
            return WAIT


class NATHAN_STRAT(strategy):

    def __init__(self, pair: Pair, candle: Candle, principle:int):
        super().__init__(pair, candle, principle)

    def checkBuy(self, data):
        """
        Nathan Haile's genius strategy
        """
        if data['macdfix']['valueMACDSignal'] > data['macdfix']['valueMACD']:
            return BUY

        return WAIT


class CANDLESTICK_STRAT(strategy):

    def __init__(self, pair: Pair, candle: Candle, principle:int):
        super().__init__(pair, candle, principle)

    def checkBuy(self, data):
        bullSigns = 0
        bearSigns = 0
        print(f"fib val; {data['fibonacciretracement']['value']}")
        for value in data:
            if value != 'candle':

                try:
                    if data[value]['value'] == '100':
                        bullSigns += 1

                    elif data[value]['value'] == '-100':
                        bearSigns += 1

                except Exception:
                    pass
        total = bullSigns - bearSigns
        if total >= 2 and (float(data['fibonacciretracement']['value']) < float(data['candle']['close'])) and \
                data['longleggeddoji']['value'] == '100':
            print(total)
            return BUY

        return WAIT


class EMA_STRATEGY(strategy):
    def __init__(self, candles, period):
        self.emas = IndicatorFunctions.EMA(candles, period)
        self.period = 9
        self.count = 0

    def checkBuy(self, data):
        if self.count < self.period:
            self.count+=1
            return WAIT

        if self.emas[self.count] > data[4]:
            self.count+=1
            return BUY 

        self.count += 1 
        return WAIT


class MA_STRATEGY(strategy):

    
    def __init__(self, pair: Pair, candle: Candle, principle:int):
        super().__init__(pair, candle, principle)
        self.ma_13_list = []
        self.ma_8_list = []
        self.ma_5_list = []
        self.momentums = []
        self.arr = []
        self.candleLimit = 26
        self.sdv = getUpperNormalDistrubtion(pair, candle, 500)
        self.prevCandle = None 



    def update(self, data):
        if len(self.arr) < self.candleLimit:

                    self.arr.append(float(data['candle']['close']))
                    # print("APPEDEND CANDLE CLOSE", self.arr)
                    self.prevCandle = data
                    return WAIT
        else:
            self.arr.append(float(data['candle']['close']))
            del self.arr[0]
            self.val_13 = IndicatorFunctions.SMA(self.arr, 13)[-1]
            self.val_8 = IndicatorFunctions.SMA(self.arr, 8)[-1] 
            self.val_5 = IndicatorFunctions.SMA(self.arr, 5)[-1] 
            self.rsi = IndicatorFunctions.RSI(self.arr)[-1]
            return None 

    def checkBuy(self, data):

        if self.update(data) is None:
    
            if (self.val_5 > self.val_13 and self.val_5 > self.val_8):
                # print("data =====================> ", data)
                self.arr = []
                return BUY

            self.prevCandle = data
            return WAIT 


    def checkSell(self, data):
        if self.update(data) is None:
            if self.val_5 < self.val_13 and self.val_5 < self.val_8:
                return SELL

            return WAIT 
            
