from Enums import *
import HelpfulOperators
from DBoperations import DBoperations
import IndicatorConstants
import QueryHelpers
from Logger import logWarningToFile, logToSlack, logDebugToFile, logErrorToFile, MessageType



class DBReader(DBoperations):
    """
    DataBase reader class that performs read operations on coin-database
    @:inherited from DBoperations
    """

    def __init__(self):
        super().__init__()
        super().connect()

    def getTableCandleData(self, candleSize: Candle, pair: Pair, args: list):

        """
        Gets all table candle data for a given pair & candle size
        @:param candleSize = Candle enum
        @:param pair = Pair enum
        @:returns candle data as dict from psql server
        """

        try:
            query = QueryHelpers.getTableDataQuery(candleSize, pair, args)
            logDebugToFile(query)
            self.cur.execute()
            self.conn.commit()
            return HelpfulOperators.convertCandlesToDict(self.cur.fetchall())

        except Exception as e:
            logToSlack(e, messageType=MessageType.ERROR, tagChannel=True)
            return None

    def fetchIndicatorData(self, pair, candleSize, indicator, limit):

        """
            Gets all table indicator data for a given pair, candle size, & indicator name
            @:param candleSize = Candle enum
            @:param pair = Pair enum
            @:param indicator = Indicator enum
            @:param limit specifices how many table entries to obtain
            @:returns indicator data as dict from psql server
        """

        try:

            self.cur.execute(
                f'SELECT * FROM {indicator}_{pair.value.replace("/", "")}_{candleSize.value} ORDER BY timestamp DESC LIMIT {limit};')
            return self.cur.fetchall()

        except Exception as e:
            logToSlack(e, tagChannel=True, messageType=MessageType.ERROR)
            raise e

    # TODO: can probably be consolidated with the getCandlesFromDB method with some conditional logic to
    #  consolidate space & reduce repetition in code operations
    def fetchCandlesWithIndicators(self, pair, candleSize, indicators, *args) -> list:

        """
        Gets all table indicator data for a given pair, candle size, & list of indicators
        & groups values by timestamp
        @:param candleSize = Candle enum
        @:param pair = Pair enum
        @:param indicators = list of indicators to pull out w/ candles
        @:param args specifices how many table entries to obtain
        @:returns candle & indicator data as dict from psql server
        """

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

        try:
            logDebugToFile(query)
            self.cur.execute(query)
            data = self.cur.fetchall()
            self.cur.execute("DROP TABLE mytable;")

        except Exception as e:
            logToSlack(e, tagChannel=True, messageType=MessageType.ERROR)
            raise e

        l = []

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
