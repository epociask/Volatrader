import datetime

from CMC_api import getMarketData, getMacroEconomicData
from DBoperations import DBoperations
import HelpfulOperators
import threading

connection = DBoperations()
connection.connect()


#ensures connection is still bounded
def ensureConnection():
    if connection.connStatus() is None:
        connection.connect()

#writes dynamicmarketdata from CMC to POSTGRESQL server
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

#writes staticmarketdata from CMC to POSTGRESQL server
def writeStaticMarketData():
    dataDict = getMarketData()
    for coin in dataDict:
        connection.writeStaticMarketDataQuerys(coin)

#writes candle data from CCXT to POSTGRESQL server
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

#TODO make timeframe an enum
def writeIndicatorForTable(timeFrame: str, pair: str, indicator: str, *args):

    assert len(args) == 0 or len(args) == 1

    if len(args) == 1:
        assert type(args[0]) == int

    if len(args) == 0:
        candles = connection.getCandleDataDescFromDB(timeFrame, pair, None)

    else:
        candles = connection.getCandleDataDescFromDB(timeFrame, pair, args[0])
    for candle in candles:
        end = HelpfulOperators.rewind(candle['timestamp'], 300, 5)
        #print(f"{candle['timestamp']} ---> {end}")
        cs = connection.getCandleDataFromTimeRange(candle['timestamp'], end, pair, timeFrame)
        #print(cs)
        connection.writeIndicatorData(timeFrame, pair, indicator, cs)

# writeCandleData("1h", 'ETH/USDT', '2020-02-15')
# p1 = threading.Thread(target=writeIndicatorForTable, args=('15m', 'ETH/USDT', '3outside',))
# p2 = threading.Thread(target=writeIndicatorForTable, args=('1h', 'ETH/USDT', '3outside',))
# # #
# p1.start()
# p2.start()

writeIndicatorForTable('15m', 'ETH/USDT', '3outside')