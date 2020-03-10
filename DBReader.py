from Enums import *
import HelpfulOperators
from DBoperations import DBoperations
import IndicatorConstants
import QueryHelpers
from Logger import logWarningToFile, logToSlack, logDebugToFile, logErrorToFile, MessageType
from IndicatorConstants import getIndicator


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

        l = [{e.value : getIndicator(e.value)} for e in indicators]
        print(l)
        assert len(args) == 0 or len(args) == 1

        try:

            query = QueryHelpers.getIndicatorDataWithCandlesQuery(pair, candleSize, l)
            print(query)
            self.cur.execute(query)
            return HelpfulOperators.cleanCandlesWithIndicators(self.cur.fetchall(), l)

        except Exception as e:
            logToSlack(e, tagChannel=True, messageType=MessageType.ERROR)
            raise e


reader = DBReader()
for val in reader.fetchCandlesWithIndicators(Pair.ETHUSDT, Candle.THIRTY_MINUTE, [Indicator.STOCHRSI]):
    print(val)