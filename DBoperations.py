import psycopg2
from config import confige
import ccxt
from IndicatorAPI import getIndicator
import HelpfulOperators


class DBoperations:

    def __init__(self) -> None:
        self.conn = None
        self.cur = None

    # Commits cursor data to Database
    def commit(self) -> None:
        print("Comitting to database\n")
        self.conn.commit()
        print("success :0")

    # connects to DataBase
    def connect(self) -> (None, Exception):

        try:
            params = confige()
            print("Connecting to postgreSQL database")
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()

        except(Exception, psycopg2.DatabaseError) as error:
            print("Error : ", error)
            raise error

    # returns connection status
    def connStatus(self):
        return self.conn

    # returns candles from given date-time range
    def getCandleDataFromTimeRange(self, startDate: str, finishDate: str, pair: str, candleStep: str):

        try:
            print('SELECT * FROM {}_OHLCV_{} WHERE timestamp <= \'{}\' and timestamp > \'{}\';'.format(
                pair.replace("/", ""), candleStep, startDate, finishDate))
            self.cur.execute('SELECT * FROM {}_OHLCV_{} WHERE timestamp <= \'{}\' and timestamp > \'{}\';'.format(
                pair.replace("/", ""), candleStep, startDate, finishDate))
            return HelpfulOperators.convertCandlesToDict(self.cur.fetchall())

        except Exception as e:
            raise e

    # writes indicator data using TAAPIO api to POSTGRESQL server
    def writeIndicatorData(self, timeFrame: str, pair: str, indicator: str, lim):

        if lim is None:
            lim = 500

        candles = self.getCandleDataFromDB(timeFrame, pair, lim)

        ts = candles[0]['timestamp']

        if candles is None:
            raise TypeError("wrong parameters supplied into getCandleData()")

        try:
            indicatorVal = getIndicator(indicator, candles)

        except Exception as e:
            raise e

        print(indicatorVal)
        delimeter = ", "
        keys = "(timestamp, " + delimeter.join(indicatorVal.keys()) + ")"
        delimter = "\', \'"

        l = []
        for ind in indicatorVal.values():
            l.append(str(ind))
        values = "(" + '\'' + ts + '\'' + ", " + delimeter.join(l) + ")"

        print("indicator keys", keys)

        print("indicator values", values)

        try:
            print('INSERT INTO ' + indicator + "_" + pair.replace("/",
                                                                  "") + "_" + timeFrame + keys + "VALUES" + values + ";")
            self.cur.execute('INSERT INTO ' + indicator + "_" + pair.replace("/",
                                                                             "") + "_" + timeFrame + keys + "VALUES" + values + ";")
            self.conn.commit()
        except Exception as e:

            if type(e) == psycopg2.errors.UndefinedTable:
                self.conn.rollback()
                delimeter = " VARCHAR, "
                keys = "(timestamp VARCHAR PRIMARY KEY NOT NULL, " + delimeter.join(indicatorVal.keys()) + " VARCHAR)"
                print('CREATE TABLE ' + indicator + "_" + pair.replace("/", "") + "_" + timeFrame + "" + keys + ";")
                self.cur.execute(
                    'CREATE TABLE ' + indicator + "_" + pair.replace("/", "") + "_" + timeFrame + "" + keys + ";")
                self.conn.commit()
                self.writeIndicatorData(timeFrame, pair, indicator, lim)

            elif type(e) == psycopg2.errors.UniqueViolation:
                print("Unique violation")
                self.conn.rollback()

            else:
                raise e

    # returns candle data as dict from psql server
    def getCandleDataFromDB(self, timeFrame: str, pair: str, limit: int):
        assert timeFrame == "1m" or timeFrame == "5m" or timeFrame == "15m" or timeFrame == "30m" or timeFrame == "1h" or timeFrame == "3h"
        assert pair.find("/") != -1

        try:
            self.cur.execute(
                "SELECT * FROM {}_OHLCV_{} ORDER BY timestamp ASC LIMIT {};".format(pair.replace("/", ""), timeFrame,
                                                                                    limit))
            self.conn.commit()
            return HelpfulOperators.convertCandlesToDict(self.cur.fetchall())

        except Exception as e:
            print("ERROR : ", e)
            return None

    # returns proper bounds to ensure decimals are parsed to table properly
    def getBounds(self, pair: str, candles):

        try:
            self.cur.execute('SELECT (LOW, HIGH) FROM BOUNDTABLE WHERE SYMBOL=\'{}\';'.format(pair[0: pair.find('/')]))
            data = self.cur.fetchall()
            print("Bounds string**" + str(data) + "**")
            if str(data) == '[]':
                self.conn.rollback()
                low, high = HelpfulOperators.getLowHighBounds(candles)
                print(
                    'INSERT INTO BOUNDTABLE VALUES(\'{}\', \'{}\', \'{}\');'.format(pair[0: pair.find('/')], low, high))
                self.cur.execute(
                    'INSERT INTO BOUNDTABLE VALUES(\'{}\', \'{}\', \'{}\');'.format(pair[0: pair.find('/')], low, high))
                self.commit()
                return self.getBounds(pair, candles)

            return data

        except Exception as e:

            raise e

    # gets OHLCV candle data from CCXT_BINANCE and writes data to POSTGRESQL server table
    def writeCandlesFromCCXT(self, timeFrame: str, pair: str, lim: (int, None)) -> (None, Exception):
        api = ccxt.binance()

        try:

            if lim is None:
                candles = api.fetchOHLCV(pair, timeFrame)

            else:
                candles = api.fetchOHLCV(pair, timeFrame, limit=lim)

            print(candles)

            candles = HelpfulOperators.convertCandlesToDict(candles)

            print(candles)

            print(candles[0]['timestamp'])

            bounds = self.getBounds(pair, candles)
            print("Bounds ,", bounds)

            # TODO optimize this, probably doesn't need to be callled everytime
            bounds = HelpfulOperators.cleanBounds(str(bounds))
            low = int(bounds[1: 2])
            high = int(bounds[2: 3])

            low += high

            print("low ", low)
            print("high ", high)
        except Exception as e:
            raise e

        marketPair = pair.replace('/', '')

        for candle in candles:
            print("Cleaning candle with val: ", low)
            candle = HelpfulOperators.cleanCandle(candle, low)
            try:
                print(
                    "INSERT INTO {}_OHLCV_{}(timestamp, open, high, low, close, volume) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');".format(
                        marketPair, timeFrame, HelpfulOperators.convertNumericTimeToString(candle['timestamp']),
                        candle['open'],
                        candle['high'], candle['low'], candle['close'], candle['volume']))
                self.cur.execute(
                    "INSERT INTO {}_OHLCV_{}(timestamp, open, high, low, close, volume) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');".format(
                        marketPair, timeFrame, HelpfulOperators.convertNumericTimeToString(candle['timestamp']),
                        candle['open'],
                        candle['high'], candle['low'], candle['close'], candle['volume']))

            except Exception as e:
                print(e)

                if type(e) == psycopg2.errors.UniqueViolation:  # primary key timestamp already exists
                    print("Unique violation")
                    self.conn.rollback()  # ignore and continue

                elif type(e) == psycopg2.errors.UndefinedTable:  # table not created yet, so lets make it
                    self.conn.rollback()
                    print("table not found... CREATING NEW ONE TO FORMAT DATA")

                    print(
                        "CREATE TABLE {}_OHLCV_{}(timestamp VARCHAR PRIMARY KEY NOT NULL, open DECIMAL({}, {}), high  DECIMAL({}, {}), low  DECIMAL({}, {}), close  DECIMAL({}, {}), volume numeric(10));".format(
                            marketPair, timeFrame, low, high, low, high, low, high, low, high))
                    self.cur.execute(
                        "CREATE TABLE {}_OHLCV_{}(timestamp VARCHAR PRIMARY KEY NOT NULL, open DECIMAL({}, {}), high  DECIMAL({}, {}), low  DECIMAL({}, {}), close  DECIMAL({}, {}), volume numeric(10));".format(
                            marketPair, timeFrame, low, high, low, high, low, high, low, high))
                    print("CREATED TABLE  \n\n")
                    self.commit()
                    self.writeCandlesFromCCXT(timeFrame, pair, lim)

                else:
                    print(type(e))
                    print(e)
                    return e

            self.commit()

    ''''
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


x = DBoperations()
x.connect()
print(x.getCandleDataFromTimeRange('2020-03-02 01:45:00', '2020-02-29 00:00:00', 'ETH/USDT', '15m'))
