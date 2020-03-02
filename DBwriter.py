import datetime
import time
from CMC_api import getMarketData, getMacroEconomicData
from DBoperations import DBoperations

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
def writeCandleData(timeFrame: str, pair: str):
    connection.writeCandlesFromCCXT(timeFrame, pair)



#writes IndicatorData using indicatorAPI to POSTGRESQL server
def writeIndicatorData(timeFrame: str, pair: str, indicator: str, lim : int):

   connection.writeIndicatorData(timeFrame, pair, indicator, lim)



writeCandleData("15m", "ETH/USDT")