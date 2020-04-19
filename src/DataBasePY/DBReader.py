import collections
import sys, os
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

 
    def getPaperTradeSessions(self):
        query = 'SELECT * FROM papertrader_results;'
        self.execute(query)
        y =  str(self.cur.fetchall()).replace("Decimal(", "").replace("datetime.datetime", "").replace("(", "[").replace(")", "").replace("[2", "2").replace("[{", "{").replace("\'", "\"").replace("None,", "").replace("True", "\"True\"").replace("False", "\"False\"").replace(", []", ']')
        y = y.replace("[[","[") if y.count("2020") == 1 else y
        print(y)
        self.commit()
        return json.loads(y)

    # def getUnactivePaperTrades(self):
    #     query = 'SELECT * FROM papertrader_results WHERE ACTIVE = False;'
    #     self.execute(query)
    #     # print(y)
    #     self.commit()
    #     return json.loads(y)

    def getActiveStatus(self, sessionID):
        query = f'SELECT (ACTIVE) FROM papertrader_results WHERE session_id =\'{sessionID}\';'
        self.execute(query)
        boolean = self.cur.fetchall()
        self.commit()
        return True if str(boolean).find("T") != -1 else False 




