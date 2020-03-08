import psycopg2
from config import config

class DBoperations:

    def __init__(self) -> None:
        self.conn = None
        self.cur = None

    # Commits cursor data to Database
    def commit(self) -> None:
        print("Comitting to database\n")
        self.conn.commit()
        print("success :0")

    # connects to DataBase
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

    # returns connection status
    def connStatus(self):
        return self.conn


    def terminateConnection(self):
        self.conn.close()

        # ensures connection is still bounded
    def ensureConnection(self):
        if self.connStatus() is None:
            self.connect()


