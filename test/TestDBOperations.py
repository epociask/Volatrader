import unittest

import ccxt
import DBoperations
import HelpfulOperators

dbOperations = DBoperations.DBoperations()

class TestDBOperations(unittest.TestCase):

    def testFetchCandleData(self):

        api = ccxt.binance()
        pair = 'ETH/USDT'
        candleSize = '15m'

        received = dbOperations.fetchCandleData(api, pair, candleSize)

        self.assertIsNotNone(received)

        received = dbOperations.fetchCandleData(api, pair, candleSize, 15)
        self.assertIsNotNone(received)

        received = dbOperations.fetchCandleData(api, pair, candleSize, '2020-02-15')
        self.assertIsNotNone(received)

        received = dbOperations.fetchCandleData(api, pair, candleSize, 'a')
        self.assertIsNotNone(received)

    def testGetCandleInsertQuery(self):
        candle = {'timestamp': 1583535600000, 'open': 239.99, 'high': 240.59, 'low': 239.75, 'close': 240.59, 'volume': 1768.84486 }
        marketPair = 'ETHUSDT'
        candleSize = '15m'
        print('TS: ' + HelpfulOperators.convertNumericTimeToString(candle['timestamp']))

        expected = "INSERT INTO ETHUSDT_OHLCV_15m(timestamp, open, high, low, close, volume) VALUES ('2020-03-06 15:00:00', '239.99', '240.59', '239.75', '240.59', '1768.84486');"
        received = dbOperations.getCandleInsertQuery(candle, marketPair, candleSize)
        self.assertEqual(expected, received)

    def testCreateCandleTableQuery(self):
        low = 3
        high = 2
        marketPair = 'ETHUSDT'
        candleSize = '15m'

        expected = "CREATE TABLE ETHUSDT_OHLCV_15m(timestamp VARCHAR PRIMARY KEY NOT NULL, open DECIMAL(3, 2), high  DECIMAL(3, 2), low DECIMAL(3, 2), close DECIMAL(3, 2), volume numeric(10));"
        received = dbOperations.getCreateCandleTableQuery(low, high, marketPair, candleSize)
        self.assertEqual(expected, received)


