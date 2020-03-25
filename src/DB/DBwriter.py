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
from multiprocessing import Lock


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

    def writeCandleData(self, candleSize: Candle, pair: Pair, *args):
        """
        wrapper function of getCCXTcandledata to write candle data from CCXT to POSTGRESQL server
        @:param candleSize = Candle enum
        @:param pair = Pair enum
        @:param *args --> either:
                            --->None in which the default limit of 500 are written
                            --->Timestamp or integer limit in which writecandlesfromCCXT will parse args accordingly
        """
        if len(args) == 0:
            self.writeCandlesFromCCXT(candleSize, pair)

        elif len(args) == 1:
            self.writeCandlesFromCCXT(candleSize, pair, args[0])

        else:
            print("too many arguments supplied to writeCandleData")

    def writeIndicatorForTable(self, candleSize: Candle, pair: Pair, returnOnUNIQUEVIOLATION, indicator: Indicator,
                               *args) -> None:

        """
        writes IndicatorData using indicatorAPI to POSTGRESQL server
        @:param candleSize = Candle enum
        @:param pair = Pair enum
        @:param indicator = Indicator enum
        @*args --> either nothing or limit number of candles to calculate for
        @:returns None

        """
        print("writing indicators")
        assert len(args) == 0 or len(args) == 1
        if len(args) == 1:
            assert type(args[0]) == int

        if len(args) == 0:
            candles = self.getCandleDataDescFromDB(candleSize, pair, None).copy()

        else:
            print("Getting candles")
            if args[0] == 0:
                self.updateSharedTable(pair, candleSize, False)
            candles = self.getCandleDataDescFromDB(candleSize, pair, args[0] + 300).copy()
        x = True
        err = True
        while x:
            print("writing ind, CANDLE LENGTH: ", len(candles))
            try:
                err = self.calculateAndInsertIndicatorEntry(candleSize, pair, indicator, candles[:300],
                                                            returnOnUNIQUEVIOLATION)
                if err is None or len(candles) - 300 == 0:
                    x = False
            except Exception as e:
                logToSlack(e, messageType=MessageType.WARNING, tagChannel=True)
                raise e
            candles.pop(0)
        print("Reached end of possible calculating range of data set for indicators")
        if args[0] == 0:
            self.updateSharedTable(pair, candleSize, True)
        return

    def calculateAndInsertIndicatorEntry(self, candleSize: Candle, pair: Pair, indicator: Indicator, candles: list,
                                         returnOnUNIQUEVIOLATION: bool) -> (bool, None):
        """
        @:param candleSize = Candle enum
        @:param pair = Pair enum
        @:param indicator = Indicator enum
        @:param candles are the candle data that's going to be used to calculate the indicator value
        @:param returnOnUNIQUEVIOLATION -> bool --> true if function should return on UniqueViolation error
        calculates indicator value w/ Indicator API
        & writes SINGLE instance of indicator data w/ timestamp to POSTGRESQL server table
        & creates table if it doesn't already exist
        :rtype: bool
        """
        if candles is None:
            raise TypeError("wrong parameters supplied into getCandleData()")
        try:
            candles = sorted(candles, key=lambda i: i['timestamp'], reverse=False)
            ts = str(candles[-1]['timestamp'])

            print(candles)

            indicatorValues = IndicatorAPI.getIndicator(indicator, candles)

            if indicatorValues is None:
                return None

        except Exception as e:
            logToSlack(e, tagChannel=True, messageType=MessageType.ERROR)
            raise e

        try:

            query = QueryHelpers.getInsertIndicatorsQueryString(indicator, indicatorValues, ts, candleSize, pair)
            logDebugToFile(query)
            self.lock.acquire()
            self.cur.execute(query)
            self.conn.commit()
            self.lock.release()

        except Exception as e:

            if type(e) == psycopg2.errors.UndefinedColumn:
                self.conn.rollback()
                createTable = QueryHelpers.getModifyTableForIndicatorQuery(candleSize, pair, indicator, indicatorValues)
                self.cur.execute(createTable)
                logDebugToFile(createTable)
                self.conn.commit()
                self.lock.release()

                insert = QueryHelpers.getInsertIndicatorsQueryString(indicator, indicatorValues, ts, candleSize, pair)
                logDebugToFile(insert)
                self.lock.acquire()
                self.cur.execute(insert)
                self.conn.commit()
                self.lock.release()

            elif type(e) == psycopg2.errors.UniqueViolation:
                logDebugToFile("UNIQUE VIOLATION")
                self.conn.rollback()
                self.lock.release()

                if returnOnUNIQUEVIOLATION is True:
                    return None

            else:
                logToSlack(e, tagChannel=True, messageType=MessageType.ERROR)
                raise e
        return True

    def writeCandlesFromCCXT(self, candleSize: Candle, pair: Pair, returnOnUNIQUEVIOLATION, *args: (int, None)) -> (
            None, Exception):
        logDebugToFile("Starting write candles fucntion")
        """
        writes candle data from CCXT Binance to PSQL table
        & creates table if it doesn't already exist
        @:param candleSize --> timelength of candle
        @:param pair --> Trading pair
        @:param returnOnUNIQUEVIOLATION
        @:param args --> *optional ---> either limit of how many recent candles OR timestamp of data to get candles starting from
        timestamp format EX--> "2020-01-01"
        """

        api = ccxt.binance()
        assert len(args) == 0 or len(args) == 1

        try:
            self.lock.acquire()

            if len(args) != 0:
                candles = HelpfulOperators.fetchCandleData(api, pair, candleSize, args)

            else:
                candles = HelpfulOperators.fetchCandleData(api, pair, candleSize, [500])

            self.lock.release()

            candles = HelpfulOperators.convertCandlesToDict(candles)

        except Exception as e:
            logToSlack(e, tagChannel=True, messageType=MessageType.ERROR)

            raise e

        last = candles[len(candles) - 1]
        count = 0
        for candle in candles:
            try:
                insertQuery = QueryHelpers.getCandleInsertQuery(candle, pair, candleSize)
                logDebugToFile(insertQuery)
                self.lock.acquire()
                self.cur.execute(insertQuery)
                self.lock.release()
            except Exception as e:

                if type(e) == psycopg2.errors.UniqueViolation:  # primary key timestamp already exists
                    logDebugToFile("UNIQUE VIOLATION")
                    self.conn.rollback()  # ignore and continue
                    self.lock.release()

                    if returnOnUNIQUEVIOLATION:
                        return count

                elif type(e) == psycopg2.errors.UndefinedTable:  # table not created yet, so lets make it
                    self.conn.rollback()
                    logDebugToFile("TABLE NOT FOUND, CREATING NEW ONE")

                    low, high = HelpfulOperators.getLowHighBounds(candles)
                    low += high
                    ++high

                    createTableQuery = QueryHelpers.getCreateCandleTableQuery(low, high, pair, candleSize)
                    self.cur.execute(createTableQuery)
                    logDebugToFile(createTableQuery)

                    self.commit()
                    self.lock.release()
                    return self.writeCandlesFromCCXT(candleSize, pair, args)

                else:
                    logToSlack(e, tagChannel=True, messageType=MessageType.ERROR)
                    self.lock.release()
                    raise e
            count+=1
            self.commit()


        if len(args) != 0 and type(args[0]) == str:

            ts = HelpfulOperators.dateFormat(HelpfulOperators.convertNumericTimeToString(int(last['timestamp'])))
            if str(args[0]) != ts:
                # logDebugToFile(f"{args[0]} ---> {ts}")
                self.writeCandlesFromCCXT(candleSize, pair, ts)
                return

        logDebugToFile("[SUCCESS] FINISHED WRITING CANDLE DATA")

    def updateSharedTable(self, pair: Pair, candleSize: Candle, value: bool):

        try:
            q = QueryHelpers.getUpdateRowInSharedTableQuery(pair, candleSize, value)
            logDebugToFile(q)
            self.lock.acquire()
            self.cur.execute(q)
            self.lock.release()
            print("NOW HERE")
            self.conn.commit()
        except Exception as e:
            logToSlack(e)
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

