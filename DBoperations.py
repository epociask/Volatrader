import psycopg2
import HelpfulOperators
import QueryHelpers
from Enums import Candle, Pair
from config import config
class DBoperations:

    def __init__(self):
        self.conn = None
        self.cur = None
    '''
    Commits cursor data to Database
    '''
    def commit(self) -> None:
        print("Comitting to database\n")
        self.conn.commit()
        print("success :0")
    '''
    connects to DataBase
    @returns None if connection is successful
    @:returns Exception otherwise 
    '''
    def connect(self) -> (None, Exception):

        try:
            params = config()
            print("Connecting to postgreSQL database")
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()

        except(Exception, psycopg2.DatabaseError) as error:
            print("Error : ", error)
            return error


        return None
    '''
    @returns connection status
    '''
    def connStatus(self):
        return self.conn

    '''
    closes connection w/ database 
    '''
    def terminateConnection(self):
        self.conn.close()

    '''
    ensures connection is still bounded
    '''
    def ensureConnection(self):
        if self.connStatus() is None:
            self.connect()

    '''
    returns candle data as dict from psql server
    '''
    def getCandleDataDescFromDB(self, candleSize: Candle, pair: Pair, limit=None) -> list:
        try:
            print("[info]   ", QueryHelpers.getCandlesFromDBQuery(pair, candleSize, limit))
            self.cur.execute(QueryHelpers.getCandlesFromDBQuery(pair, candleSize, limit))
            return(HelpfulOperators.convertCandlesToDict(self.cur.fetchall()))


        except Exception as e:
            print("ERROR : ", e)
            raise e

