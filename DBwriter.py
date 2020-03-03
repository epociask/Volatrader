import datetime
import time
from CMC_api import getMarketData, getMacroEconomicData
from DBoperations import DBoperations
import HelpfulOperators

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
def writeCandleData(timeFrame: str, pair: str, lim):
    connection.writeCandlesFromCCXT(timeFrame, pair, lim)


#
# #writes IndicatorData using indicatorAPI to POSTGRESQL server
# def writeIndicatorData(timeFrame: str, pair: str, indicator: str, lim : int):
#
#    connection.writeIndicatorData(timeFrame, pair, indicator, lim)

#TODO make timeframe an enum
def writeIndicatorForTable(timeFrame: str, pair: str, indicator: str):

    candles = connection.getCandleDataDescFromDB(timeFrame, pair, 500)
    print(candles)

    for candle in candles:
        cs = connection.getCandleDataFromTimeRange(candle['timestamp'], HelpfulOperators.rewind(candle['timestamp'], 300, 15), pair, timeFrame)
        connection.writeIndicatorData(timeFrame, pair, indicator, cs)


writeIndicatorForTable('15m', 'ETH/USDT', 'stochrsi')