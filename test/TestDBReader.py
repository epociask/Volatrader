import unittest
from DBReader import DBReader
from DBoperations import DBoperations
import ccxt
import HelpfulOperators
from Enums import Pair, Candle

reader = DBReader()
operator = DBoperations()


class TestDBOperations(unittest.TestCase):

    def testEquality(self):
        expected = None
        actual = operator.connect()
        self.assertEqual(expected, actual)


class TestDBReader(unittest.TestCase):

    received = None

    def testFetchCandleData(self):
        api = ccxt.binance()
        pair = Pair.ETHUSDT
        candleSize = Candle.FIFTEEEN

        received = HelpfulOperators.fetchCandleData(api, pair, candleSize, [15])
        self.assertIsNotNone(received)

        received = HelpfulOperators.fetchCandleData(api, pair, candleSize, ['2020-02-15'])
        self.assertIsNotNone(received)

        received = HelpfulOperators.fetchCandleData(api, pair, candleSize, ['a'])
        self.assertIsNotNone(received)

    def testFetchCandlesWithIndicators(self):
        pair = Pair.ETHUSDT
        candleSize = Candle.FIFTEEEN
        received = reader.fetchCandlesWithIndicators(pair, candleSize, ['threeoutside'])
        print(received)
        self.assertIsNotNone(received)
        self.assertIsNotNone(received[0]['threeoutside']['value'])
        self.assertIsNotNone(received[0]['candle']['timestamp'])
