from Enums import *
import HelpfulOperators
from DBoperations import DBoperations
import IndicatorConstants
import QueryHelpers
import ccxt

class DBReader(DBoperations):

    def __init__(self):
        super().__init__()
        self.connect()

    # returns candle data as dict from psql server
    def getTableData(self, candleSize: str, pair: str, args: list):
        try:
            self.cur.execute(QueryHelpers.getTableDataQuery(candleSize, pair, args))

            self.conn.commit()
            return HelpfulOperators.convertCandlesToDict(self.cur.fetchall())

        except Exception as e:
            print("ERROR : ", e)
            return None

    # returns candle data as dict from psql server
    def getCandleDataDescFromDB(self, candleSize: Candle, pair: Pair, limit=None):
        try:
            self.conn.commit()
            return HelpfulOperators.convertCandlesToDict(self.cur.fetchall())

        except Exception as e:
            print("ERROR : ", e)
            return None

    def fetchIndicatorData(self, pair, candleSize, indicator, limit):
        try:

            self.cur.execute(f'SELECT * FROM {indicator}_{pair.value.replace("/", "")}_{candleSize.value} ORDER BY timestamp DESC LIMIT {limit};')
            return self.cur.fetchall()

        except Exception as e:
            raise e

    # TODO this can probably be consolidated with the getCandlesFromDB method with some conditional logic to
    #  consolidate space & reduce repetition in code operations

    def fetchCandlesWithIndicators(self, pair, candleSize, indicators, *args):
        assert len(args) == 0 or len(args) == 1

        x = []
        timestamps = []

        x.append(pair.value + "_OHLCV_" + candleSize.value)
        for indicator in indicators:
            x.append(indicator + "_" + pair.value + "_" + candleSize.value)
            timestamps.append("timstamp" + indicator)

        s, col = HelpfulOperators.makeEqualities(x)
        f = "CREATE TEMP TABLE mytable AS SELECT * FROM " + ", ".join(e for e in x) + " " + s + col

        if len(args) is 0:
            query = f + " SELECT * FROM mytable ORDER BY timestamp ASC;"

        else:
            print((args[0]))
            query = f + f"SELECT * FROM mytable WHERE timestamp >= \'{args[0]}\' ORDER BY timestamp ASC;"
        print("Query ::::::: ", query)

        try:
            self.cur.execute(query)
            data = self.cur.fetchall()
            self.cur.execute("DROP TABLE mytable;")

        except Exception as e:
            raise e

        l = []
        print("Data:::", data)
        for a in data:
            indlist = []
            c = IndicatorConstants.getIndicator('candle').copy()
            if c is None:
                return
            d = {}
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



