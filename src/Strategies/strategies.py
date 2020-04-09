from Helpers.Enums import Indicator, Candle, Pair
from SlackNotifier.PriceNotifications import getUpperNormalDistrubtion
from Indicators import IndicatorFunctions

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

#TODO 4/2
#
# class riskManager():
#
#     def __init__(self, principle: int):
#         self.principle = principle
#
#     def sellPercent(self, percent: float):
#         self.principle = self.principle - (percent )

class BBANDS_STRAT(strategy):

    def __init__(self, pair: Pair, candle: Candle, principle : int):
        super().__init__(pair, candle, principle)
        self.indicatorList = [Indicator.BBANDS]

    def update(self, data):
        if data['bbands']['valueUpperBand'] < data['candle']['close']:
            return True, data['candle']['timestamp'], float(data['candle']['close'])

        return False, None, None

class SIMPLE_BUY_STRAT(strategy):

    def __init__(self):
        pass
    def update(self, data):
        if data['3outside']['value'] != '0' or float(data['invertedhammer']['value']) != "0":
            buyPrice = float(data['candle']['close'])
            buyTime = data['candle']['timestamp']

            return True, buyTime, buyPrice

        return False, None, None

class TEST_BUY_STRAT(strategy):
    def __init__(self, pair: Pair, candle: Candle, principle:int ):
        super().__init__(pair, candle, principle)
        self.dumbass = NATHAN_STRAT(pair, candle, 100)
        self.sdv = getUpperNormalDistrubtion(pair, candle, 300)

    def update(self, data):
        bear = None
        for i in data:
            if i != 'candle' and i != 'macdfix':
                print(i, data[i])
                if data[i]['value'] == '-100':
                    bear = True

        ind, _, _, = self.dumbass.update(data)
        if float(data['candle']['volume']) > self.sdv['2SD'] and float(data['candle']['close']) < float(
                data['candle']['open']) and bear is None and float(data['fibonacciretracement']['value']) > float(
            data['candle']['close']) and ind:
            return True, data['candle']['timestamp'], float(data['candle']['close'])

        else:
            return False, None, None


class NATHAN_STRAT(strategy):

    def __init__(self, pair: Pair, candle: Candle, principle:int):
        super().__init__(pair, candle, principle)

    def update(self, data):
        """
        Nathan Haile's genius strategy
        """
        if data['macdfix']['valueMACDSignal'] > data['macdfix']['valueMACD']:
            return True, data['candle']['timestamp'], float(data['candle']['close'])

        return False, None, None


class CANDLESTICK_STRAT(strategy):

    def __init__(self, pair: Pair, candle: Candle, principle:int):
        super().__init__(pair, candle, principle)

    def update(self, data):
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
            return True, data['candle']['timestamp'], float(data['candle']['close'])

        return False, None, None


class EMA_STRATEGY(strategy):
    def __init__(self, candles, period):
        self.emas = IndicatorFunctions.EMA(candles, period)
        self.period = 9
        self.count = 0

    def update(self, data):
        if self.count < self.period:
            self.count+=1
            return False, None, None

        if self.emas[self.count] > data[4]:
            self.count+=1
            return True, data[0], data[4] 

        self.count += 1 
        return False, None, None


class MA_STRATEGY(strategy):

    
    def __init__(self, pair: Pair, candle: Candle, principle:int):
        super().__init__(pair, candle, principle)
        self.ma_13_list = []
        self.ma_8_list = []
        self.ma_5_list = []
        self.arr = []
        self.candleLimit = 14
        self.sdv = getUpperNormalDistrubtion(pair, candle, 500)


    def update(self, data):

        if len(self.arr) < self.candleLimit:

            self.arr.append(float(data['candle']['close']))
            print("APPEDEND CANDLE CLOSE", self.arr)
            return False, None, None
        else:
            self.arr.append(float(data['candle']['close']))
            del self.arr[0]

        val_13 = IndicatorFunctions.SMA(self.arr, 13)[-1]
        val_8 = IndicatorFunctions.SMA(self.arr, 8)[-1] 
        val_5 = IndicatorFunctions.SMA(self.arr, 5)[-1] 
        rsi = IndicatorFunctions.RSI(self.arr)[-1]

        print("value 13", val_13)
        print('value 8', val_8)
        print("value 5", val_5)
        if (val_5 > val_13 and val_5 > val_8) and data['candle']['volume'] >=  self.sdv['2SD']:
            print("data =====================> ", data)
            self.arr = []
            return True, data['candle']['timestamp'], float(data['candle']['close'])
 

        return False, None, None

