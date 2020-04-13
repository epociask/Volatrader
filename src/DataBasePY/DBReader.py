import collections
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
from Helpers.Constants.Enums import *
from Helpers import DataOperators
from DataBasePY import QueryHelpers
from DataBasePY.DBoperations import DBoperations
from Helpers.Logger import logToSlack, logDebugToFile, MessageType
import json
import re


class DBReader(DBoperations):
    """
    DataBase reader class that performs read operations on coin-database
    @:inherited from DBoperations
    """

    def __init__(self):
        super().__init__()
        super().connect()


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

    def fetchCandlesWithIndicators(self, pair: Pair, candleSize: Candle, limit = None) -> list:

        """
        Gets all table indicator data for a given pair, candle size, & list of indicators
        & groups values by timestamp
        @:param candleSize = Candle enum
        @:param pair = Pair enum
        @:param limit
        """

        try:
            self.lock.acquire()
            query = QueryHelpers.getCandlesWithIndicatorsFromDBQuery(pair, candleSize, limit)
            logDebugToFile(query)
            self.cur.execute(query)
            temp = self.cur.fetchall()
            self.lock.release()
            return HelpfulOperators.cleanCandlesWithIndicators(temp)
        except Exception as e:
            logToSlack(e, tagChannel=True, messageType=MessageType.ERROR)
            raise e

