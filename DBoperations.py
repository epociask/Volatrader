import psycopg2
from config import confige
import ccxt
from IndicatorAPI import getIndicator
import HelpfulOperators
import time
import IndicatorConstants


dateFormat = lambda time : str(time) + "T00:00:00Z"


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


#TODO this can probably be consolidated with the getCandlesFromDB method with some conditional logic to consoldiate space & reduce repition in code operations

    def getCandlesWithIndicator(self, pair, candleStep, args):
        pair = pair.replace("/", "")
        x = []
        timestamps = []
        x.append(pair + "_OHLCV_" + candleStep)
        print(args)
        for indicator in args:
            x.append(indicator + "_" + pair + "_" + candleStep)
            timestamps.append("timstamp"+indicator)

        s, col = HelpfulOperators.makeEqualities(x)
        f = "CREATE TEMP TABLE mytable AS SELECT * FROM " + ", ".join(e for e in x) + " " + s + col
        query = f + " SELECT * FROM mytable ORDER BY timestamp ASC;"
        print(query)

        try:
            self.cur.execute(query)
            data = self.cur.fetchall()
            self.cur.execute("DROP TABLE mytable;")

        except Exception as e:
            raise e

        l = []
        for a in data:
            indlist = []
            c = IndicatorConstants.getIndicator('candle').copy()
            if c is None:
                return
            d= {}
            it2 = iter(args)
            for indicator in args:
                indlist.append(IndicatorConstants.getIndicator(indicator).copy())
            #ind = IndicatorConstants.getIndicator('threeoutside').copy()
            it = iter(a)
            c['timestamp'] = HelpfulOperators.cleaner(next(it))
            c['open'] = HelpfulOperators.cleaner(next(it))
            c['high'] = HelpfulOperators.cleaner(next(it))
            c['low'] = HelpfulOperators.cleaner(next(it))
            c['close'] = HelpfulOperators.cleaner(next(it))
            c['volume'] = HelpfulOperators.cleaner(next(it))

            d['candle'] = c
            for ind in indlist:
                for key in ind.keys():
                    ind[key] = next(it)
                d[next(it2)] = ind
            l.append(d)

        return l

    def getCandleDataFromTimeRange(self, startDate: str, finishDate: str, pair: str, candleStep: str):

        try:
            # print('SELECT * FROM {}_OHLCV_{} WHERE timestamp <= \'{}\' and timestamp > \'{}\';'.format(
            #     pair.replace("/", ""), candleStep, startDate, finishDate))
            self.cur.execute('SELECT * FROM {}_OHLCV_{} WHERE timestamp <= \'{}\' and timestamp > \'{}\';'.format(
                pair.replace("/", ""), candleStep, startDate, finishDate))
            return HelpfulOperators.convertCandlesToDict(self.cur.fetchall())

        except Exception as e:
            raise e

    def getIndicatorData(self, pair, candleSize, indicator, limit):

        try:
            self.cur.execute(
                f'SELECT * FROM {indicator}_{pair.replace("/", "")}_{candleSize} ORDER BY timestamp DESC LIMIT {limit};')
            return self.cur.fetchall()

        except Exception as e:
            raise e

    # writes indicator data using TAAPIO api to POSTGRESQL server
    def writeIndicatorData(self, candleSize: str, pair: str, indicator: str, candles: list):
        ts = candles[len(candles)-1]['timestamp']

        if candles is None:
            raise TypeError("wrong parameters supplied into getCandleData()")

        try:
            indicatorVal = getIndicator(indicator, candles)

            if indicatorVal is None:
                print("END")
                return

        except Exception as e:
            raise e

        print(indicatorVal)
        delimeter = ", "
        clean = lambda indicator: indicator if indicator.find("3") == -1 else indicator.replace("3", "three")

        keys = f"(timestamp{clean(indicator)}, " + delimeter.join(indicatorVal.keys()) + ")"
        delimter = "\', \'"

        l = []
        for ind in indicatorVal.values():
            l.append(str(ind))
        values = "(" + '\'' + ts + '\'' + ", " + delimeter.join(l) + ")"

        print("indicator keys", keys)

        print("indicator values", values)
        try:
            print('INSERT INTO ' + clean(indicator) + "_" + pair.replace("/",
                                                                         "") + "_" + candleSize + keys + "VALUES" + values + ";")
            self.cur.execute('INSERT INTO ' + clean(indicator) + "_" + pair.replace("/",
                                                                                    "") + "_" + candleSize + keys + "VALUES" + values + ";")
            self.conn.commit()
        except Exception as e:

            if type(e) == psycopg2.errors.UndefinedTable:
                self.conn.rollback()
                delimeter = " VARCHAR, "
                keys = f"(timestamp{clean(indicator)} VARCHAR PRIMARY KEY NOT NULL, " + delimeter.join(
                    indicatorVal.keys()) + f" VARCHAR, FOREIGN KEY(timestamp{clean(indicator)}) REFERENCES {pair.replace('/', '')}_OHLCV_{candleSize}(timestamp))"
                print('CREATE TABLE ' + clean(indicator) + "_" + pair.replace("/",
                                                                              "") + "_" + candleSize + "" + keys + ";")
                self.cur.execute(
                    'CREATE TABLE ' + clean(indicator) + "_" + pair.replace("/",
                                                                            "") + "_" + candleSize + "" + keys + ";")
                self.conn.commit()
                self.writeIndicatorData(candleSize, pair, indicator, candles)

            elif type(e) == psycopg2.errors.UniqueViolation:
                print("Unique violation")
                self.conn.rollback()

            else:
                raise e

    # returns candle data as dict from psql server
    def getCandleDataFromDB(self, candleSize: str, pair: str, limit: int):
        assert candleSize == "1m" or candleSize == "5m" or candleSize == "15m" or candleSize == "30m" or candleSize == "1h" or candleSize == "3h"
        assert pair.find("/") != -1

        try:
            self.cur.execute(
                "SELECT * FROM {}_OHLCV_{} ORDER BY timestamp ASC LIMIT {};".format(pair.replace("/", ""), candleSize,
                                                                                    limit))
            self.conn.commit()
            return HelpfulOperators.convertCandlesToDict(self.cur.fetchall())

        except Exception as e:
            print("ERROR : ", e)
            return None

        # returns candle data as dict from psql server

    def getCandleDataDescFromDB(self, candleSize: str, pair: str, limit: int):
        assert candleSize == "1m" or candleSize == "5m" or candleSize == "15m" or candleSize == "30m" or candleSize == "1h" or candleSize == "3h"
        assert pair.find("/") != -1

        try:

            if limit is not None:
                self.cur.execute(
                "SELECT * FROM {}_OHLCV_{} ORDER BY timestamp DESC LIMIT {};".format(pair.replace("/", ""),
                                                                                     candleSize,
                                                                                     limit))
            else:
                self.cur.execute(
                    "SELECT * FROM {}_OHLCV_{} ORDER BY timestamp DESC;".format(pair.replace("/", ""),
                                                                                         candleSize,
                                                                                         ))

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

    '''
    @param candleSize --> timelength of candle
    @param pair --> Trading pair
    @param args --> *optional ---> either limit of how many recent candles OR timestamp of data to get candles starting from  
    timestamp format EX--> "2020-01-01"
    '''

    #TODO ADD CATCH FOR WHEN DECIMAL VALUES OF CANDLE FLOAT DATA CHANGES

    def writeCandlesFromCCXT(self, candleSize: str, pair: str, *args: (int, None)) -> (None, Exception):
        api = ccxt.binance()

        assert len(args) == 0 or len(args) == 1


        try:

            if len(args) == 0:
                candles = api.fetchOHLCV(pair, candleSize)

            else:
                if type(args[0]) == int:
                    candles = api.fetchOHLCV(pair, candleSize, limit=args[0])

                else:
                    candle = api.parse8601(dateFormat(args[0]))
                    candles = api.fetchOHLCV(pair, candleSize, candle)


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
        last = candles[len(candles)-1]
        for candle in candles:
            print("Cleaning candle with val: ", low)
            candle = HelpfulOperators.cleanCandle(candle, low)

            # if candle == candles[len(candles) - 1]:
            #    last = candle
            ts = HelpfulOperators.convertNumericTimeToString(candle['timestamp'])
            try:
                print(
                    "INSERT INTO {}_OHLCV_{}(timestamp, open, high, low, close, volume) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');".format(
                        marketPair, candleSize, ts,
                        candle['open'],
                        candle['high'], candle['low'], candle['close'], candle['volume']))
                self.cur.execute(
                    "INSERT INTO {}_OHLCV_{}(timestamp, open, high, low, close, volume) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');".format(
                        marketPair, candleSize, HelpfulOperators.convertNumericTimeToString(candle['timestamp']),
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
                            marketPair, candleSize, low, high, low, high, low, high, low, high))
                    self.cur.execute(
                        "CREATE TABLE {}_OHLCV_{}(timestamp VARCHAR PRIMARY KEY NOT NULL, open DECIMAL({}, {}), high  DECIMAL({}, {}), low  DECIMAL({}, {}), close  DECIMAL({}, {}), volume numeric(10));".format(
                            marketPair, candleSize, low, high, low, high, low, high, low, high))
                    print("CREATED TABLE  \n\n")
                    self.commit()
                    self.writeCandlesFromCCXT(candleSize, pair, args)


                elif type(e) == psycopg2.errors.NumericValueOutOfRange:

                    print(
                        f"SELECT HIGH, LOW FROM BOUNDTABLE WHERE SYMBOL = '{marketPair}'"
                    )

                    self.conn.rollback()

                    self.cur.execute(
                        f"SELECT HIGH, LOW FROM BOUNDTABLE WHERE SYMBOL = '{marketPair}'"
                    )

                    bounds = self.cur.fetchall()

                    print(bounds)
                    #     f"ALTER TABLE {}_OHLCV_{} "
                    # )


                else:
                    print(type(e))
                    print(e)
                    return e

            self.commit()

        if len(args) != 0 and str(args[0]) != dateFormat(HelpfulOperators.convertNumericTimeToString(last['timestamp'])) and type(args[0]) != int:
            print(f"{args[0]} ---> {last}")
            print("Writing for : ", dateFormat(HelpfulOperators.convertNumericTimeToString(last['timestamp'])))
            self.writeCandlesFromCCXT(candleSize, pair, dateFormat(HelpfulOperators.convertNumericTimeToString(last['timestamp'])))



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

# x = DBoperations()
# x.connect()
# x.writeIndicatorData("1d", "BTC/USDT", "3outside")
#
# x.writeCandlesFromCCXT("15m", "BTC/USDT", '2020-01-01')
#


