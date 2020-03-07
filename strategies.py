SIMPLE_BUY_STRAT_INDICATORS = ['threeoutside']



#returns strategy function with a list of indicators to use with it
def getStrat(name):

    return globals()[name], globals()[f"{name}_INDICATORS"]





def SIMPLE_BUY_STRAT(data):
    #print("Checking buy start")
    #print(data['threeoutside']['value'])
    if data['threeoutside']['value'] == '-100':
        buyPrice = float(data['candle']['close'])
        buyTime = data['candle']['timestamp']

        return True, buyTime, buyPrice

    return False, None, None