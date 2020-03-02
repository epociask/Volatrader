from DBoperations import *
from Session import Session

x = DBoperations()
x.connect()

#TODO write to be compatible w/ a strategy param
#TODO ADD A SHITTON SON
def backTest(pair: str, strat: str, candleStep, sample):
    test = Session(pair)
    candles = x.getCandleDataFromDB(candleStep, pair, sample)
    print(len(candles))

    for candle in candles:
        test.update(candle)
        print(candle)

    print("total profit loss: %" + str(test.getTotalPL()))


backTest('BTC/USDT', "strat", "15m", 500)
