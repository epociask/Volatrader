from BackTest.backtester import backTest
from DB.DBwriter import DBwriter
from Helpers.Enums import Pair, Candle, Time

writer = DBwriter()

pairs = []


def automateAndVariate(pair: Pair, candleSizes: list, stopLossRange: int, takeProfitRange: int, strategy, timeFrame=None, principle=1000):
    for sl in range(stopLossRange):
        sl+=1

        for tp in range(takeProfitRange):
            tp+=1
            for candleSize in candleSizes:

                if timeFrame is None:
                    backTest(pair, candleSize, strategy, sl, tp, principle, shouldOutputToConsole=False)

                else:
                    backTest(pair, candleSize, strategy, sl, tp, principle, timeEnum=timeFrame, shouldOutputToConsole=False)


automateAndVariate(Pair.ETHUSDT, [Candle.FIFTEEEN_MINUTE, Candle.FIVE_MINUTE, Candle.THIRTY_MINUTE], 4, 4,
                   "TEST_BUY_STRAT", Time.DAY)
