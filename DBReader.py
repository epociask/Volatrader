import time
from datetime import datetime

from Enums import *
import HelpfulOperators
from DBoperations import DBoperations
import IndicatorConstants
import QueryHelpers

'''
DataBase reader class that performs read operations on coin-database
@inherited from DBoperations  
'''


class DBReader(DBoperations):

    def __init__(self):
        super().__init__()
        super().connect()

    '''
    Gets all table candle data for a given pair & candle size 
    @param candleSize = Candle enum
    @param pair = Pair enum 
    @returns candle data as dict from psql server
    '''

    def getTableCandleData(self, candleSize: Candle, pair: Pair, args: list):
        try:
            self.cur.execute(QueryHelpers.getTableDataQuery(candleSize, pair, args))
            self.conn.commit()
            return HelpfulOperators.convertCandlesToDict(self.cur.fetchall())

        except Exception as e:
            print("ERROR : ", e)
            return None

    '''
    Gets all table indicator data for a given pair, candle size, & indicator name
    @param candleSize = Candle enum
    @param pair = Pair enum 
    @param indicator = Indicator enum 
    @param limit specifices how many table entries to obtain 
    @returns indicator data as dict from psql server
    '''

    def fetchIndicatorData(self, pair, candleSize, indicator, limit):
        try:

            self.cur.execute(
                f'SELECT * FROM {indicator}_{pair.value.replace("/", "")}_{candleSize.value} ORDER BY timestamp DESC LIMIT {limit};')
            return self.cur.fetchall()

        except Exception as e:
            raise e

    '''
     Gets all table indicator data for a given pair, candle size, & list of indicators 
     & groups values by timestamp
     @param candleSize = Candle enum
     @param pair = Pair enum 
     @param indicators = list of indicators to pull out w/ candles 
     @param args specifices how many table entries to obtain 
     @returns candle & indicator data as dict from psql server
     '''
    # TODO this can probably be consolidated with the getCandlesFromDB method with some conditional logic to
    #  consolidate space & reduce repetition in code operations
    def fetchCandlesWithIndicators(self, pair, candleSize, indicators, *args) -> list:
        assert len(args) == 0 or len(args) == 1

        x = []
        timestamps = []

        x.append(pair.value + "_OHLCV_" + candleSize.value)
        for indicator in indicators:
            x.append(indicator + "_" + pair.value + "_" + candleSize.value)
            timestamps.append("timstamp" + indicator)
        # TODO consoldiate and unit test w/ query helpers
        s, col = QueryHelpers.getWhereEqualsQuery(x)
        f = "CREATE TEMP TABLE mytable AS SELECT * FROM " + ", ".join(e for e in x) + " " + s + col

        if len(args) is 0:
            query = f + " SELECT * FROM mytable ORDER BY timestamp ASC;"

        else:
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

            # TODO functionalize this logic
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



inds = [QueryHelpers.clean2(QueryHelpers.clean100(QueryHelpers.clean3(e.value))) for e in Indicator]

x = datetime.now()
print(x)
t = DBReader()
t.fetchCandlesWithIndicators(Pair.STXUSDT, Candle.FIFTEEEN_MINUTE, inds)

print(datetime.now() - x)