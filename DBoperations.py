import psycopg2
from config import confige
import ccxt
from IndicatorAPI import getIndicator
import HelpfulOperators
import IndicatorConstants
from Enums import *

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

    # TODO this can probably be consolidated with the getCandlesFromDB method with some conditional logic to consoldiate space & reduce repition in code operations

    def fetchCandlesWithIndicators(self, pair, candleSize, indicators, *args):
        pair = pair.value.replace("/", "")

        assert len(args) == 0 or len(args) == 1
        x = []
        timestamps = []

        x.append(pair + "_OHLCV_" + candleSize.value)
        print(indicators)
        for indicator in indicators:
            x.append(indicator + "_" + pair + "_" + candleSize.value)
            timestamps.append("timstamp"+indicator)

        s, col = HelpfulOperators.makeEqualities(x)
        f = "CREATE TEMP TABLE mytable AS SELECT * FROM " + ", ".join(e for e in x) + " " + s + col

        if len(args) is 0:
            query = f + " SELECT * FROM mytable ORDER BY timestamp ASC;"

        else:
            query = f + f"SELECT * FROM mytable WHERE timestamp >= \'{args[0]}\' ORDER BY timestamp ASC;"
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
            it2 = iter(indicators)
            for indicator in indicators:
                indlist.append(IndicatorConstants.getIndicator(indicator).copy())
            # ind = IndicatorConstants.getIndicator('threeoutside').copy()
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

    def getCandleDataFromTimeRange(self, startDate: str, finishDate: str, pair: str, candleSize: str):

        try:
            # print('SELECT * FROM {}_OHLCV_{} WHERE timestamp <= \'{}\' and timestamp > \'{}\';'.format(
            #     pair.replace("/", ""), candleSize.value, startDate, finishDate))
            self.cur.execute('SELECT * FROM {}_OHLCV_{} WHERE timestamp <= \'{}\' and timestamp > \'{}\';'.format(
                pair.value.replace("/", ""), candleSize.value, startDate, finishDate))
            return HelpfulOperators.convertCandlesToDict(self.cur.fetchall())

        except Exception as e:
            raise e

    def fetchIndicatorData(self, pair, candleSize, indicator, limit):

        try:
            self.cur.execute(
                f'SELECT * FROM {indicator}_{pair.value.replace("/", "")}_{candleSize.value} ORDER BY timestamp DESC LIMIT {limit};')
            return self.cur.fetchall()

        except Exception as e:
            raise e

    # writes indicator data using TAAPIO api to POSTGRESQL server

    def writeIndicatorData(self, candleSize: Candle, pair: Pair, indicator: str, candles: list):
        ts = candles[0]['timestamp']
        print("TIMESTAMP", ts)
        if candles is None:
            raise TypeError("wrong parameters supplied into getCandleData()")
        candles.reverse()
        try:
            indicatorVal = getIndicator(indicator, candles).copy()
            candles.reverse()
            print("INDICATOR VALUE", indicatorVal)

            if indicatorVal is None:
                print("END")
                return

        except Exception as e:
            print(indicatorVal)
        delimeter = ", "
        clean = lambda indicator: indicator if indicator.find("3") == -1 else indicator.replace("3", "three")

        delimter = "\', \'"

        l = []
        for ind in indicatorVal.values():
            l.append(str(ind))
        values = "(" + '\'' + ts + '\'' + ", " + delimeter.join(l) + ")"



        keys = (f"(timestamp{clean(indicator)}, " + (delimeter.join(indicatorVal.keys())) if list(indicatorVal.keys())[0] != "value" else f"(timestamp{clean(indicator)}," + f" {clean(indicator)}value") + ")"

        print("Keys", keys)

        try:
            print('INSERT INTO ' + clean(indicator) + "_" + pair.value.replace("/",
                                                                         "") + "_" + candleSize.value + keys + "VALUES" + values + ";")
            self.cur.execute('INSERT INTO ' + clean(indicator) + "_" + pair.value.replace("/",
                                                                                    "") + "_" + candleSize.value + keys + "VALUES" + values + ";")
            self.conn.commit()
        except Exception as e:

            if type(e) == psycopg2.errors.UndefinedTable:
                self.conn.rollback()
                delimeter = " VARCHAR, "
                keys = f"(timestamp{clean(indicator)} VARCHAR PRIMARY KEY NOT NULL, " + (delimeter.join(
                    indicatorVal.keys()) if list(indicatorVal.keys())[0] != "value" else f" {clean(indicator)}value") + f" VARCHAR, FOREIGN KEY(timestamp{clean(indicator)}) REFERENCES {pair.value.replace('/', '')}_OHLCV_{candleSize.value}(timestamp))"
                print('CREATE TABLE ' + clean(indicator) + "_" + pair.value.replace("/",
                                                                              "") + "_" + candleSize.value + "" + keys + ";")
                self.cur.execute(
                    'CREATE TABLE ' + clean(indicator) + "_" + pair.value.replace("/",
                                                                            "") + "_" + candleSize.value + "" + keys + ";")
                self.conn.commit()
                self.writeIndicatorData(candleSize.value, pair.value, indicator, candles)

            elif type(e) == psycopg2.errors.UniqueViolation:
                print("Unique violation")
                self.conn.rollback()

            else:
                raise e

    # returns candle data as dict from psql server
    def getTableData(self, candleSize: str, pair: str, args: list):

        try:
            self.cur.execute(
                    "SELECT * FROM {}_OHLCV_{} ORDER BY timestamp ASC LIMIT {};".format(pair.value.replace("/", ""), candleSize.value,
                                                                                    args[0]))

            self.conn.commit()
            return HelpfulOperators.convertCandlesToDict(self.cur.fetchall())

        except Exception as e:
            print("ERROR : ", e)
            return None

        # returns candle data as dict from psql server

    def getCandleDataDescFromDB(self, candleSize: Candle, pair: Pair, limit: int):
        assert pair.value.find("/") != -1

        try:

            if limit is not None:
                self.cur.execute(

                "SELECT * FROM {}_OHLCV_{} ORDER BY timestamp DESC LIMIT {};".format(pair.value.replace("/", ""),
                                                                                     candleSize.value,
                                                                                     limit))
            else:
                self.cur.execute(
                    "SELECT * FROM {}_OHLCV_{} ORDER BY timestamp DESC;".format(pair.value.replace("/", ""),
                                                                                         candleSize.value,
                                                                                         ))
            self.conn.commit()
            return HelpfulOperators.convertCandlesToDict(self.cur.fetchall())

        except Exception as e:
            print("ERROR : ", e)
            return None

    # returns proper bounds to ensure decimals are parsed to table properly
    def getBounds(self, pair: Pair, candles):

        try:
            self.cur.execute('SELECT (LOW, HIGH) FROM BOUNDTABLE WHERE SYMBOL=\'{}\';'.format(pair.value[0: pair.value.find('/')]))
            data = self.cur.fetchall()
            print("Bounds string**" + str(data) + "**")
            if str(data) == '[]':
                self.conn.rollback()
                low, high = HelpfulOperators.getLowHighBounds(candles)
                print(
                    'INSERT INTO BOUNDTABLE VALUES(\'{}\', \'{}\', \'{}\');'.format(pair.value[0: pair.value.find('/')], low, high))
                self.cur.execute(
                    'INSERT INTO BOUNDTABLE VALUES(\'{}\', \'{}\', \'{}\');'.format(pair.value[0: pair.value.find('/')], low, high))
                self.commit()
                return self.getBounds(pair, candles)

            return data

        except Exception as e:

            raise e

    # Returns candles fetched from an exchange
    def fetchCandleData(self, api: ccxt.Exchange, pair: Pair, candleSize: Candle, args: (int, None)):

            arg = args[0]
            if type(arg) == int:
                candles = api.fetchOHLCV(pair.value.replace("USDT", "/USDT"), candleSize.value, limit=args[0])

            else:
                candle = api.parse8601(dateFormat(arg))
                candles = api.fetchOHLCV(pair.value.replace("USDT", "/USDT"), candleSize.value, candle)
            return candles


    def getCandleInsertQuery(self, candle: dict, marketPair: str, candleSize: str) -> str:
        return f"INSERT INTO {marketPair}_OHLCV_{candleSize}" \
               f"(timestamp, open, high, low, close, volume) VALUES " \
               f"(\'{candle['timestamp']}\', \'{candle['open']}\', \'{candle['high']}\', \'{candle['low']}\', \'{candle['close']}\', \'{candle['volume']}\');"

    # Generates create table query
    def getCreateCandleTableQuery(self, low, high, marketPair: str, candleSize: str) -> str:
        lowHigh = f'{low}, {high}'

        return f"CREATE TABLE {marketPair}_OHLCV_{candleSize}(timestamp TIMESTAMP PRIMARY KEY NOT NULL, " \
               f"open DECIMAL({lowHigh}), high  DECIMAL({lowHigh}), low DECIMAL({lowHigh}), " \
               f"close DECIMAL({lowHigh}), volume numeric(10));"

    # gets OHLCV candle data from CCXT_BINANCE and writes data to POSTGRESQL server table

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

            candles = self.fetchCandleData(api, pair, candleSize, args)

            candles = HelpfulOperators.convertCandlesToDict(candles)



        except Exception as e:
            raise e


        last = candles[len(candles) - 1]
        for candle in candles:
            ts = candle['timestamp']
            print(ts)
            try:
                insertQuery = self.getCandleInsertQuery(candle, pair.value, candleSize.value)
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

                    createTableQuery = self.getCreateCandleTableQuery(low, high, pair.value, candleSize.value)

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

        if len(args) != 0 and str(args[0]) != dateFormat(last['timestamp']) and type(args[0]) != int:
            print(f"{args[0]} ---> {dateFormat(HelpfulOperators.convertNumericTimeToString(last['timestamp']))}")

            print("Writing for : ", dateFormat(HelpfulOperators.convertNumericTimeToString(last['timestamp'])))
            self.writeCandlesFromCCXT(candleSize, pair,
                                      dateFormat(HelpfulOperators.convertNumericTimeToString(last['timestamp'])))

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


x = DBoperations()
x.connect()

x.writeCandlesFromCCXT(Candle.HOUR, Pair.ETHUSDT, "2020-01-01 00:00:00")