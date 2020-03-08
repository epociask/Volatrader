import datetime
import time
from Enums import *
from multiprocessing.pool import Pool

from CMC_api import getMarketData, getMacroEconomicData
from DBoperations import DBoperations
import HelpfulOperators
import threading

connection = DBoperations()
connection.connect()


# ensures connection is still bounded
def ensureConnection():
    if connection.connStatus() is None:
        connection.connect()


# writes dynamicmarketdata from CMC to POSTGRESQL server
def writeDynamicMarketMacroData():
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print(st)
    f = getMacroEconomicData()
    print("Inserting macro econ data :-)")
    connection.writeMacroEconMarketData(f, st)
    dataDict = getMarketData()
    print("Inserting dynamic market data ;-)")
    for coin in dataDict:
        connection.writeDynamicMarketDataQuerys(coin, st)


# writes staticmarketdata from CMC to POSTGRESQL server
def writeStaticMarketData():
    dataDict = getMarketData()
    for coin in dataDict:
        connection.writeStaticMarketDataQuerys(coin)


# writes candle data from CCXT to POSTGRESQL server
def writeCandleData(timeFrame: str, pair: str, *args):
    if len(args) == 0:
        connection.writeCandlesFromCCXT(timeFrame, pair)

    elif len(args) == 1:
        connection.writeCandlesFromCCXT(timeFrame, pair, args[0])

    else:
        print("too many arguments supplied to")


#
# #writes IndicatorData using indicatorAPI to POSTGRESQL server
# def writeIndicatorData(timeFrame: str, pair: str, indicator: str, lim : int):
#
#    connection.writeIndicatorData(timeFrame, pair, indicator, lim)

# TODO make timeframe an enum
# TODO additional args to to be date
def writeIndicatorForTable(candleSize: str, pair: str, indicator: str, *args):

    assert len(args) == 0 or len(args) == 1

    if len(args) == 1:
        assert type(args[0]) == int

    if len(args) == 0:
        candles = connection.getCandleDataDescFromDB(candleSize, pair, None)

    else:
        candles = connection.getCandleDataDescFromDB(candleSize, pair, args[0])

    print(candles)
    print(candles[0])
    for candle in candles:
        print(f"{candle['timestamp']}-------------------->>")

        try:
            connection.writeIndicatorData(candleSize, pair, indicator, candles[:300])

        except Exception as e:
            print("Reached end of possible calculating range")
            return
        candles.pop(0)





# p1 = threading.Thread(target= writeIndicatorForTable, args = (Candle.FIFTEEEN, Pair.ETHUSDT, 'abandonedbaby',))
# p2 = threading.Thread(target= writeIndicatorForTable, args = (Candle.FIFTEEEN, Pair.ETHUSDT, 'advanceblock',))
# # p3 = threading.Thread(target= writeIndicatorForTable, args = (Candle.FIFTEEEN, Pair.ETHUSDT, 'belthold',))
# # p4 = threading.Thread(target= writeIndicatorForTable, args = (Candle.FIFTEEEN, Pair.ETHUSDT, 'breakaway',))
#
# if __name__ == '__main__':
#     p1.start()
#     time.sleep(2)
#     p2.start()
#     time.sleep(2)
#     p3.start()
#     time.sleep(2)
#     p4.start()
#     p1.join()
#     p2.join()
#     p3.join()
#     p4.join()