import psycopg2
from Helpers.DataOperators import convertCandlesToDict
from DataBasePY import QueryHelpers
from Helpers.Constants.Enums import Candle, Pair
from DataBasePY.config import config
from Helpers.Logger import logToSlack, logDebugToFile
from threading import Lock


class DBoperations:
    """
    Base database operations class for handling Database connection, commits, & ensuring connection
    """

    def __init__(self):
        self.conn = None
        self.cur = None
        self.lock = Lock()

    def commit(self) -> None:
        """"
        Commits cursor data to Database
        @:returns None
        """

        print("Comitting to database\n")
        self.conn.commit()
        self.terminateConnection()
        print("success :0")

    def connect(self) -> (None, Exception):
        """
        connects to DataBase
        @:returns None if connection is successful
        @:returns Exception otherwise
        """

        try:
            params = config()
            print("Connecting to postgreSQL database")
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()

        except(Exception, psycopg2.DatabaseError) as error:
            print("Error : ", error)
            return error

        return None

    def connStatus(self):
        """
        @:returns connection status
        """

        return self.conn

    def terminateConnection(self):
        """
        closes connection w/ database
        """

        self.conn.close()

    def ensureConnection(self):
        """
         ensures connection is still bounded
        """

        if self.connStatus() is None:
            self.connect()

    def getCandleDataDescFromDB(self, candleSize: Candle, pair: Pair, limit=None) -> list:
        """
        returns candle data as dict from psql server
        """
        try:
            query = QueryHelpers.getCandlesFromDBQuery(pair, candleSize, limit)
            logDebugToFile(query)
            self.lock.acquire()
            self.cur.execute(query)
            temp = self.cur.fetchall()
            self.lock.release()
            return convertCandlesToDict(temp)

        except Exception as e:
            logToSlack(e)
            self.lock.release()
            raise e
