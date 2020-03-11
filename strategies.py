from Enums import Indicator

SIMPLE_BUY_STRAT_INDICATORS = [Indicator.THREEOUTSIDE, Indicator.INVERTEDHAMMER]


def getStrat(name):
    """
    returns strategy function with a list of indicators to use with it
    """

    return globals()[name], globals()[f"{name}_INDICATORS"]





def SIMPLE_BUY_STRAT(data):

    if data['3outside']['value'] != '0' or float(data['invertedhammer']['value']) != "0":
        buyPrice = float(data['candle']['close'])
        buyTime = data['candle']['timestamp']

        return True, buyTime, buyPrice

    return False, None, None