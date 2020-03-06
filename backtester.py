from DBoperations import *
from Session import Session
import strategies
x = DBoperations()
x.connect()

#TODO write to be compatible w/ a strategy param
#TODO ADD A SHITTON SON
def backTest(pair: str, candleStep, strategy, stopLossPercent, takeProfitPercent, *args):

    strat = strategies.getStrat(strategy)
    test = Session(pair, strat, takeProfitPercent, stopLossPercent)
    DataSet = x.getCandlesWithIndicator(pair, candleStep, args)
    for data in DataSet:
        #print(data)
        test.update(data)

    print("total profit loss: " + f"+%{str(test.getTotalPL())}" if test.getTotalPL() > 0 else str(test.getTotalPL()))



backTest('ETH/USDT', "15m", "SIMPLE_BUY_STRAT", 4, "08", "threeoutside")
