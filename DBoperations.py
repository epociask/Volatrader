import psycopg2
import HelpfulOperators
import QueryHelpers
from Enums import Candle, Pair
from config import config
from Logger import logToSlack, logDebugToFile


class DBoperations:
    """
    Base database operations class for handling Database connection, commits, & ensuring connection
    """

    def __init__(self):
        self.conn = None
        self.cur = None

    def commit(self) -> None:
        """"
        Commits cursor data to Database
        @:returns None
        """

        print("Comitting to database\n")
        self.conn.commit()
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
            self.cur.execute(query)
            return HelpfulOperators.convertCandlesToDict(self.cur.fetchall())


        except Exception as e:
            logToSlack(e)
            raise e
