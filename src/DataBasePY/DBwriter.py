import datetime
import time

from Helpers.Enums import *
from Helpers.Session import Session
from API.CMC_api import getMarketData, getMacroEconomicData
from DB.DBoperations import DBoperations
import psycopg2
from Helpers import HelpfulOperators
from DB import QueryHelpers
from API import IndicatorAPI
import ccxt
from Helpers.Logger import logToSlack, MessageType, logDebugToFile, logErrorToFile
indicatorENUMS = [e for e in Indicator]

class DBwriter(DBoperations):
    """
    DataBase writer class to handle DBwrite operations
    @inherited from DBopertions
    """

    def __init__(self):
        super().__init__()
        self.connect()

    def writeBackTestData(self, session: Session, startTimeStamp: str, finishTimeStamp: str):
        """

        :param session:
        :param startTimeStamp:
        :param finishTimeStamp:
        :return:
        """
        query = QueryHelpers.getInsertBackTestDataQuery(session, startTimeStamp, finishTimeStamp)
        try:
            logDebugToFile(query)
            self.cur.execute(query)

        except Exception as e:
            logErrorToFile(e)

            if type(e) == psycopg2.errors.UndefinedTable:
                createTableQuery = ""
            raise e




    def writeStaticMarketDataQuerys(self, coin, timeStamp):
        """
        writes static market metric data from CoinCapAPI to postgresql server
        """

        if coin['platform'] is not None:
            js = coin['platform']['name']

        else:
            js = None

        try:
            self.cur.execute(
                'INSERT INTO STATIC_MARKET_DATA (NAME, SYMBOL, DATE_ADDED, MAX_SUPPLY, TOTAL_SUPPLY, PLATFORM) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'.format(
                    str(coin["name"]).replace("'", ""), str(coin["symbol"]), str(coin["date_added"][1: 10]),
                    (coin["max_supply"] if coin["max_supply"] is not None else "0"),
                    str(coin["total_supply"] if coin["total_supply"] is not None else "0"), str(js)))



        except Exception as e:
            logToSlack(e, tagChannel=True, messageType=MessageType.ERROR)
            return

        self.commit()

    def writeDynamicMarketDataQuerys(self, coin, timeStamp):
        """
        Writes dynamic metric market data from CoinCapAPI to PostgreSQL server
        """

        clean = lambda exp: exp if exp is not None else "0"

        print(
            "INSERT INTO DYNAMIC_MARKET_DATA(TIME_STAMP_DMD, NAME, PRICE, CMC_RANK, MARKET_CAP, NUM_MARKET_PAIRS, CIRCULATING_SUPPLY, PERCENT_CHANGE_1H, PERCENT_CHANGE_24H, PERCENT_CHANGE_7D, VOLUME_24H, SYMBOL) VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
                str(timeStamp), str(coin["name"]).replace("'", ""), str(coin['quote']['USD']['price']),
                str(coin['cmc_rank']), str(coin['num_market_pairs']), str(coin['quote']['USD']['market_cap']),
                str(coin['circulating_supply']), str(coin['quote']['USD']['percent_change_1h']),
                str(coin['quote']['USD']['percent_change_24h']), str(coin['quote']['USD']['percent_change_7d']),
                str(coin['quote']['USD']['volume_24h']), str(coin['symbol'])))

        try:
            self.cur.execute(
                "INSERT INTO DYNAMIC_MARKET_DATA(TIME_STAMP_DMD, NAME, PRICE, CMC_RANK, MARKET_CAP, NUM_MARKET_PAIRS, CIRCULATING_SUPPLY, PERCENT_CHANGE_1H, PERCENT_CHANGE_24H, PERCENT_CHANGE_7D, VOLUME_24H, SYMBOL) VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
                    str(timeStamp), str(coin["name"]).replace("'", ""), str(coin['quote']['USD']['price']),
                    str(clean(coin['cmc_rank'])),
                    str(clean(coin['num_market_pairs'])),
                    str(clean(coin['quote']['USD']['market_cap'])),
                    str(clean(coin['circulating_supply'])),
                    str(coin['quote']['USD']['percent_change_1h']) if coin['quote']['USD'][
                                                                          'percent_change_1h'] is not None else "0",
                    str(coin['quote']['USD']['percent_change_24h']) if coin['quote']['USD'][
                                                                           'percent_change_24h'] is not None else "0",
                    str(coin['quote']['USD']['percent_change_7d']) if coin['quote']['USD'][
                                                                          'percent_change_7d'] is not None else "0",
                    str(coin['quote']['USD']['volume_24h']),
                    str(coin['symbol']) if coin['quote']['USD']['volume_24h'] is not None else "0"))

        except Exception as e:
            logToSlack(e, tagChannel=True, messageType=MessageType.ERROR)

        self.commit()

    """
    writes macroeconomic metric data from CoinCapAPI to postgresql server
    """

    def writeMacroEconMarketData(self, json, timeStamp):

        try:
            self.cur.execute(
                "INSERT INTO macroecon_market_data (TIME_STAMP_MMD, ACTIVE_CRYPTOCURRENCIES, TOTAL_CRYPTOCURRENCIES, ACTIVE_MARKET_PAIRS, ACTIVE_EXCHANGES, TOTAL_EXCHANGES, BTC_DOMINANCE, ETH_DOMINANCE, TOTAL_MARKET_CAP, TOTAL_VOLUME_24H, ALTCOIN_VOLUME_24H, ALTCOIN_MARKET_CAP) VALUES('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}','{}')".format(
                    timeStamp, json['active_cryptocurrencies'], json['total_cryptocurrencies'],
                    json['active_market_pairs'], json['active_exchanges'], json['total_exchanges'],
                    json['eth_dominance'], json['btc_dominance'], json['quote']['USD']['total_market_cap'],
                    json['quote']['USD']['total_volume_24h'], json['quote']['USD']['altcoin_volume_24h'],
                    json['quote']['USD']['altcoin_market_cap']))
            self.commit()

        except Exception as e:
            logToSlack(e, tagChannel=True, messageType=MessageType.ERROR)

    """
    writes dynamicmarketdata from CMC to POSTGRESQL server
    """

    def writeDynamicMarketMacroData(self):
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        f = getMacroEconomicData()
        self.conn.writeMacroEconMarketData(f, st)
        dataDict = getMarketData()
        for coin in dataDict:
            self.conn.writeDynamicMarketDataQuerys(coin, st)

    """
    writes staticmarketdata from CMC to POSTGRESQL server
    """

    def writeStaticMarketData(self):
        dataDict = getMarketData()
        for coin in dataDict:
            self.writeStaticMarketDataQuerys(coin)

