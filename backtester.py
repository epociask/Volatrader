from DBoperations import *
from Session import Session
x = DBoperations()
x.connect()

#TODO write to be compatible w/ a strategy param
#TODO ADD A SHITTON SON
def backTest(pair: str, candleStep, *args):
    test = Session(pair)
    DataSet = x.getCandlesWithIndicator(pair, candleStep, args)

    print(DataSet)
    for data in DataSet:
        test.update(data)

    print("total profit loss: " + f"+%{str(test.getTotalPL())}" if test.getTotalPL() > 0 else str(test.getTotalPL()))



backTest('ETH/USDT', "15m", "threeoutside")
