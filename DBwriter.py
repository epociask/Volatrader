import datetime
import time
from Enums import *
from CMC_api import getMarketData, getMacroEconomicData
from DBoperations import DBoperations
import psycopg2
import QueryHelpers
import IndicatorAPI
import HelpfulOperators
import ccxt
class DBwriter(DBoperations):

    def __init__(self):
        super().__init__()
        self.connect()


    # writes dynamicmarketdata from CMC to POSTGRESQL server
    def writeDynamicMarketMacroData(self):
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(st)
        f = getMacroEconomicData()
        print("Inserting macro econ data :-)")
        self.conn.writeMacroEconMarketData(f, st)
        dataDict = getMarketData()
        print("Inserting dynamic market data ;-)")
        for coin in dataDict:
            self.conn.writeDynamicMarketDataQuerys(coin, st)

    # writes staticmarketdata from CMC to POSTGRESQL server
    def writeStaticMarketData(self):
        dataDict = getMarketData()
        for coin in dataDict:
            self.writeStaticMarketDataQuerys(coin)

    # writes candle data from CCXT to POSTGRESQL server
    def writeCandleData(self, candleSize: Candle, pair: Pair, *args):
        if len(args) == 0:
            self.writeCandlesFromCCXT(candleSize, pair)

        elif len(args) == 1:
            self.writeCandlesFromCCXT(candleSize, pair, args[0])

        else:
            print("too many arguments supplied to")

    #
    # #writes IndicatorData using indicatorAPI to POSTGRESQL server
    # def writeIndicatorData(timeFrame: str, pair: str, indicator: str, lim : int):
    #
    #    self.conn.writeIndicatorData(timeFrame, pair, indicator, lim)

    def writeIndicatorForTable(self, candleSize: Candle, pair: Pair, indicator: str, *args):

        assert len(args) == 0 or len(args) == 1

        if len(args) == 1:
            assert type(args[0]) == int

        if len(args) == 0:
            candles = self.getCandleDataDescFromDB(candleSize, pair, None)

        else:
            candles = self.getCandleDataDescFromDB(candleSize, pair, args[0])

        print(candles)
        for candle in candles:
            print(f"{candle['timestamp']}-------------------->>")

            try:
                self.conn.writeIndicatorData(candleSize, pair, indicator, candles[:300])

            except Exception as e:
                raise (e)
                # print("Reached end of possible calculating range")
                return
            candles.pop(0)

    # writes indicator data using TAAPIO api to POSTGRESQL server

    def writeIndicatorData(self, candleSize: Candle, pair: Pair, indicator: Indicator, candles: list):
        ts = str(candles[0]['timestamp'])
        print("TIMESTAMP", ts)
        if candles is None:
            raise TypeError("wrong parameters supplied into getCandleData()")
        candles.reverse()
        try:
            indicatorValues = IndicatorAPI.getIndicator(indicator.value, candles).copy()
            candles.reverse()
            print("INDICATOR VALUE", indicatorValues)

            if indicatorValues is None:
                print("END")
                return

        except Exception as e:
            print(e)
            print(indicatorValues)

        try:
            print(QueryHelpers.getInsertIndicatorsQueryString(indicator, indicatorValues, ts, candleSize, pair))
            self.cur.execute(
                QueryHelpers.getInsertIndicatorsQueryString(indicator, indicatorValues, ts, candleSize, pair))
            self.conn.commit()

        except Exception as e:

            if type(e) == psycopg2.errors.UndefinedTable:
                self.conn.rollback()
                print(QueryHelpers.makeCreateIndicatorTableQuery(candleSize, pair, indicator, indicatorValues))
                self.cur.execute(
                    QueryHelpers.makeCreateIndicatorTableQuery(candleSize, pair, indicator, indicatorValues))
                self.conn.commit()
                self.writeIndicatorData(candleSize, pair, indicator, candles)

            elif type(e) == psycopg2.errors.UniqueViolation:
                print("Unique violation")
                self.conn.rollback()

            else:
                raise e

    '''
    @param candleSize --> timelength of candle
    @param pair --> Trading pair
    @param args --> *optional ---> either limit of how many recent candles OR timestamp of data to get candles starting from
    timestamp format EX--> "2020-01-01"
    '''

    # TODO ADD CATCH FOR WHEN DECIMAL VALUES OF CANDLE FLOAT DATA CHANGES

    def writeCandlesFromCCXT(self, candleSize: Candle, pair: Pair, *args: (int, None)) -> (None, Exception):
        api = ccxt.binance()

        assert len(args) == 0 or len(args) == 1

        try:
            if len(args) != 0:
                candles = HelpfulOperators.fetchCandleData(api, pair, candleSize, args)
#def fetchCandleData(api: ccxt.Exchange, pair: Pair, candleSize: Candle, args: (int, None)):

            else:
                candles = HelpfulOperators.fetchCandleData(api, pair, candleSize, [500])

            candles = HelpfulOperators.convertCandlesToDict(candles)



        except Exception as e:
            raise e

        last = candles[len(candles) - 1]
        for candle in candles:
            ts = candle['timestamp']
            print(ts)
            try:
                insertQuery = QueryHelpers.getCandleInsertQuery(candle, pair, candleSize)
                print("[info] CANDLE INSERT QUERY: ", insertQuery)
                self.cur.execute(insertQuery)


            except Exception as e:
                print(e)

                if type(e) == psycopg2.errors.UniqueViolation:  # primary key timestamp already exists
                    print("Unique violation")
                    self.conn.rollback()  # ignore and continue

                elif type(e) == psycopg2.errors.UndefinedTable:  # table not created yet, so lets make it
                    self.conn.rollback()
                    print("table not found... CREATING NEW ONE TO FORMAT DATA")
                    bounds = self.getBounds(pair, candles)
                    print("Bounds ,", bounds)

                    bounds = HelpfulOperators.cleanBounds(str(bounds))
                    low = int(bounds[1: 2])
                    high = int(bounds[2: 3])

                    low += high
                    ++high

                    createTableQuery = QueryHelpers.getCreateCandleTableQuery(low, high, pair, candleSize)

                    print("CREATE TABLE: ", createTableQuery)
                    self.cur.execute(createTableQuery)
                    self.commit()
                    self.writeCandlesFromCCXT(candleSize, pair, args)


                elif type(e) == psycopg2.errors.NumericValueOutOfRange:

                    print(f"SELECT HIGH, LOW FROM BOUNDTABLE WHERE SYMBOL = '{pair}'")

                    self.conn.rollback()

                    self.cur.execute(f"SELECT HIGH, LOW FROM BOUNDTABLE WHERE SYMBOL = '{pair}'")

                    bounds = self.cur.fetchall()

                else:
                    print(type(e))
                    print(e)
                    return e

            self.commit()
        print(args[0])
        if len(args) != 0 and str(args[0]) != HelpfulOperators.dateFormat(
                HelpfulOperators.convertNumericTimeToString((last['timestamp']))) and type(args[0]) != int:
            print(f"{args[0]} ---> {HelpfulOperators.dateFormat(HelpfulOperators.convertNumericTimeToString(last['timestamp']))}")

            print("Writing for : ", HelpfulOperators.dateFormat(HelpfulOperators.convertNumericTimeToString(last['timestamp'])))
            self.writeCandlesFromCCXT(candleSize, pair,
                                      HelpfulOperators.dateFormat(HelpfulOperators.convertNumericTimeToString(last['timestamp'])))
            return

        print("Finshed :::: ;)")


    # writes static market metric data from CoinCapAPI to postgresql server
    def writeStaticMarketDataQuerys(self, coin, timeStamp):

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
            print("ERROR: ", e)
            return

        self.commit()


    # writes dynamic metric market data from CoinCapAPI to postgresql server
    def writeDynamicMarketDataQuerys(self, coin, timeStamp):

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
            print("ERROR: ", e)

        self.commit()

    '''
    #writes macroeconomic metric data from CoinCapAPI to postgresql server
    '''

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
            print("ERROR: ", e)
