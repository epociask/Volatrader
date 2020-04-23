import collections
import sys, os
from Helpers.Constants.Enums import *
from Helpers import DataOperators
from DataBasePY import QueryHelpers
from DataBasePY.DBoperations import DBoperations
from Helpers.Logger import logToSlack, logDebugToFile, MessageType, logErrorToFile
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

 
    def getPaperTradeSessions(self):
        query = 'select row_to_json(t) from (SELECT * FROM papertrader_results) t ;'

        try:
            self.execute(query)
            y =  str(self.cur.fetchall())
            logDebugToFile(y)
        except Exception as e:
            logErrorToFile(e)
        print(y)   
        y= y.replace("(", "").replace(",)", "").replace("\'", "\"").replace("None,", "\"None\",").replace("True", "\"True\"").replace("False","\"False\"")
        self.terminateConnection()
        print(y)
        y = json.loads(y)
        print(y)
        return y

    def getActiveStatus(self, sessionID: str):
        """
        @param: sessionID: unique ID to reference session
        @returns: active status of session 
        """
        query = f'SELECT (ACTIVE) FROM papertrader_results WHERE session_id =\'{sessionID}\';'

        try:
            self.execute(query)
            boolean = self.cur.fetchall()
            self.commit()

        except Exception as e:
            logErrorToFile(e)
        return True if str(boolean).find("T") != -1 else False 




    def getSupportResistance(self, pair: Pair, candleSize: Candle):
        """
        @param: pair, candle: Enums to specify which support/resistance strategies to obtain 
        @returns: current support/resistance of given pair, candle 
        """
        query = f"SELECT ROW_to_JSON(t) FROM (SELECT support, resistance FROM support_resistance WHERE pair=\'{pair.value}\' AND candle=\'{candleSize.value}\') t;"
        
        try:
            self.execute(query)
            regex = re.compile("{.+}")
            y = json.loads(regex.search(str(self.cur.fetchall())).group().replace("\'", "\""))
            self.terminateConnection()

        except Exception as e:
            logErrorToFile(e)

        return y 
