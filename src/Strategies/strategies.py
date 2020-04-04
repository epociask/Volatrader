from Helpers.Enums import Indicator, Candle, Pair
from Helpers.PriceNotifications import getUpperNormalDistrubtion


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

    def __init__(self):
        pass

    def update(self, data):
        bullSigns = 0
        bearSigns = 0
        print(f"fib val; {data['fibonacciretracement']['value']}")
        for value in data:
            if value != 'candle':
                print(f"{value}: {data[value]['value']}")
                if data[value]['value'] == '100':
                    bullSigns += 1

                elif data[value]['value'] == '-100':
                    bearSigns += 1

        total = bullSigns - bearSigns
        if total >= 2 and (float(data['fibonacciretracement']['value']) < float(data['candle']['close'])) and \
                data['longleggeddoji']['value'] == '100':
            print(total)
            return True, data['candle']['timestamp'], float(data['candle']['close'])

        return False, None, None
