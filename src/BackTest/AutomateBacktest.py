from BackTest.backtester import backTest
from DB.DBwriter import DBwriter
writer = DBwriter()


def automateAndVariate(pair, stopLossRange: int, takeProfitRange: int, strategy, candleList, timeFrame=None):

    for sl in range(stopLossRange):

        for tp in range(takeProfitRange):

                for candle in  candleList:
                    tempSess, start, fin = backTest(pair, candle, strategy, sl, tp, 1000)
                    writer.writeBackTestData(tempSess, start, fin)