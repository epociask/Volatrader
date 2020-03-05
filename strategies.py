def getStrat(name):

    return globals()[name]





def SIMPLE_BUY_STRAT(data):
    print("Checking buy start")
    print(data['threeoutside']['value'])
    if data['threeoutside']['value'] != '0':
        print("Buying")
        buyPrice = float(data['candle']['close'])
        buyTime = data['candle']['timestamp']

        return True, buyTime, buyPrice

    return False, None, None