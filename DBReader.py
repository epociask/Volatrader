from Enums import *
import HelpfulOperators
from DBoperations import DBoperations
import QueryHelpers
from Logger import  logToSlack, logDebugToFile, MessageType
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

    def fetchCandlesWithIndicators(self, pair, candleSize, indicators, *args) -> dict:

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

        indicatorList = [{e.value: getIndicator(e.value)} for e in indicators]

        try:

            query = QueryHelpers.getIndicatorDataWithCandlesQuery(pair, candleSize, indicatorList)
            logDebugToFile(query)
            self.cur.execute(query)
            return HelpfulOperators.cleanCandlesWithIndicators(self.cur.fetchall(), indicatorList)

        except Exception as e:
            logToSlack(e, tagChannel=True, messageType=MessageType.ERROR)
            raise e
