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


# class STRAT(enum):
#     CANDLESTRAT = "CANDLESTICK_STRAT"
#     SIMPLE_BUY_STRAT = "SIMPLE_BUY_STRAT"
#     TEST_BUY_STRAT = "TEST_BUY_STRAT"

class SIMPLE_BUY_STRAT():

    def __init__(self):
        self.indicatorList = [Indicator.THREEOUTSIDE, Indicator.INVERTEDHAMMER]

    def update(self, data):
        if data['3outside']['value'] != '0' or float(data['invertedhammer']['value']) != "0":
            buyPrice = float(data['candle']['close'])
            buyTime = data['candle']['timestamp']

            return True, buyTime, buyPrice

        return False, None, None


class strategy():

    def __init__(self, pair: Pair, candleSize: Candle):
        self.pair = pair
        self.candleSize = candleSize


class TEST_BUY_STRAT(strategy):
    def __init__(self, pair: Pair, candle: Candle):
        super().__init__(pair, candle)
        self.indicatorList = [Indicator.THREEOUTSIDE, Indicator.LONGLEGGEDDOJI, Indicator.LONGLINE, Indicator.KICKING,
                              Indicator.INNECK, Indicator.MACDFIX,
                              Indicator.HIGHWAVE, Indicator.GAPSIDEWHITE, Indicator.FIBONACCIRETRACEMENT,
                              Indicator.HARAMICROSS, Indicator.HIKKAKE, Indicator.HOMINGPIGEON, Indicator.EVENINGSTAR,
                              Indicator.EVENINGDOJISTAR, Indicator.DARKCLOUDCOVER, Indicator.BREAKAWAY,
                              Indicator.CONCEALBABYSWALL, Indicator.THREESTARSINSOUTH, Indicator.THREELINESTRIKE,
                              Indicator.THREEINSIDE, Indicator.ADXR, Indicator.THREEOUTSIDE, Indicator.INVERTEDHAMMER,
                              Indicator.MORNINGSTAR, Indicator.HANGINGMAN, Indicator.SHOOTINGSTAR,
                              Indicator.THREEWHITESOLDIERS]
        self.dumbass = NATHAN_STRAT(pair, candle)
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
                data['candle']['open']) and bear is None and float(data['fibonacciretracement']['value']) > float(data['candle']['close']) and ind:
            return True, data['candle']['timestamp'], float(data['candle']['close'])

        else:
            return False, None, None


class NATHAN_STRAT(strategy):

    def __init__(self, pair: Pair, candle: Candle):
        super().__init__(pair, candle)
        self.indicatorList = [Indicator.MACDFIX]

    def update(self, data):
        """
        Nathan Haile's genius strategy
        """
        if data['macdfix']['valueMACDSignal'] > data['macdfix']['valueMACD']:
            return True, data['candle']['timestamp'], float(data['candle']['close'])

        return False, None, None


class CANDLESTICK_STRAT():

    def __init__(self):
        self.indicatorList = [Indicator.LONGLEGGEDDOJI, Indicator.LONGLINE, Indicator.KICKING, Indicator.INNECK,
                              Indicator.HIGHWAVE, Indicator.GAPSIDEWHITE, Indicator.FIBONACCIRETRACEMENT,
                              Indicator.HARAMICROSS, Indicator.HIKKAKE, Indicator.HOMINGPIGEON, Indicator.EVENINGSTAR,
                              Indicator.EVENINGDOJISTAR, Indicator.DARKCLOUDCOVER, Indicator.BREAKAWAY,
                              Indicator.CONCEALBABYSWALL, Indicator.THREESTARSINSOUTH, Indicator.THREELINESTRIKE,
                              Indicator.THREEINSIDE, Indicator.ADXR, Indicator.THREEOUTSIDE, Indicator.INVERTEDHAMMER,
                              Indicator.MORNINGSTAR, Indicator.HANGINGMAN, Indicator.SHOOTINGSTAR,
                              Indicator.THREEWHITESOLDIERS]

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
