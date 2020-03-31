from Helpers.Enums import Indicator
import enum




SIMPLE_BUY_STRAT_INDICATORS = [Indicator.THREEOUTSIDE, Indicator.INVERTEDHAMMER]
TEST_BUY_STRAT_INDICATORS = [Indicator.THREEOUTSIDE]
CANDLESTICK_STRAT_INDICATORS = [Indicator.LONGLEGGEDDOJI, Indicator.LONGLINE, Indicator.KICKING, Indicator.INNECK,
                                Indicator.HIGHWAVE, Indicator.GAPSIDEWHITE, Indicator.FIBONACCIRETRACEMENT,
                                Indicator.HARAMICROSS, Indicator.HIKKAKE, Indicator.HOMINGPIGEON, Indicator.EVENINGSTAR,
                                Indicator.EVENINGDOJISTAR, Indicator.DARKCLOUDCOVER, Indicator.BREAKAWAY,
                                Indicator.CONCEALBABYSWALL, Indicator.THREESTARSINSOUTH, Indicator.THREELINESTRIKE,
                                Indicator.THREEINSIDE, Indicator.ADXR, Indicator.THREEOUTSIDE, Indicator.INVERTEDHAMMER,
                                Indicator.MORNINGSTAR, Indicator.HANGINGMAN, Indicator.SHOOTINGSTAR,
                                Indicator.THREEWHITESOLDIERS]

NATHAN_STRAT_INDICATORS = [Indicator.MACDFIX]


# class STRAT(enum):
#     CANDLESTRAT = "CANDLESTICK_STRAT"
#     SIMPLE_BUY_STRAT = "SIMPLE_BUY_STRAT"
#     TEST_BUY_STRAT = "TEST_BUY_STRAT"


class TEST_BUY_STRAT():

    def __init__(self):
        self.indicatorList = [Indicator.THREEOUTSIDE]

    def update(self, data):
        return True, data['candle']['timestamp'], float(data['candle']['close'])



def getStrat(name: str):
    """
    returns strategy function with a list of indicators to use with it
    :param name: Name of strategy
    :returns: strategy function and list of indicators used w/ strategy
    """
    c = globals()[name]
    return c()


def SIMPLE_BUY_STRAT(data):
    if data['3outside']['value'] != '0' or float(data['invertedhammer']['value']) != "0":
        buyPrice = float(data['candle']['close'])
        buyTime = data['candle']['timestamp']

        return True, buyTime, buyPrice

    return False, None, None




def NATHAN_STRAT(data):
    """
    Nathan Haile's genius strategy
    """
    if data['macdfix']['valueMACDSignal'] > data['macdfix']['valueMACD']:
        return True, data['candle']['timestamp'], float(data['candle']['close'])

    return False, None, None

def CANDLESTICK_STRAT(data):
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

