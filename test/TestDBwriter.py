from DBwriter import DBwriter
import unittest
from Enums import *
writer = DBwriter()

class TestDBwriter(unittest.TestCase):

    def testWriteCandleData(self):
        try:
            writer.writeCandleData(Candle.HOUR, Pair.XRPUSDT)
        except Exception as e:
            self.fail(f"testWriteCandleData raised ExceptionType {e} unexpectedly!")



    def testWriteCandleDataWithLimit(self):
        try:
            writer.writeCandleData(Candle.HOUR, Pair.XRPUSDT, 200)
        except Exception as e:
            self.fail(f"testWriteCandleData raised ExceptionType {e} unexpectedly!")


    def testWriteCandleDataWithTS(self):
        try:
            writer.writeCandleData(Candle.HOUR, Pair.XRPUSDT, 200)
        except Exception as e:
            self.fail(f"testWriteCandleData raised ExceptionType {e} unexpectedly!")

