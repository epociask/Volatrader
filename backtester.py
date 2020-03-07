from DBoperations import *
from Session import Session
import strategies
x = DBoperations()
x.connect()

#main backtest function

'''
@param pair -> pair you wish to run backtest on 
@param candleSize -> size of candle you wish to use
@param strategy -> Buying strategy that you wish to implement 
@param Stop-Loss percent 
@Param Take profit percent -> percent gain from buy-price at which you wish to sell
'''
def backTest(pair: str, candleSize, strategy, stopLossPercent, takeProfitPercent):

    takeProfitPercent = f"0{takeProfitPercent}" if takeProfitPercent - 10 <= 0 else f"{takeProfitPercent}"
    strat, indicators = strategies.getStrat(strategy)
    test = Session(pair, strat, takeProfitPercent, stopLossPercent)
    DataSet = x.getCandlesWithIndicator(pair, candleSize, indicators)
    for data in DataSet:
        print(data)
        test.update(data)

    print("total profit loss: " + f"+%{str(test.getTotalPL())}" if test.getTotalPL() > 0 else str(test.getTotalPL()))



backTest('ETH/USDT', "15m", "SIMPLE_BUY_STRAT", 4, 8)
