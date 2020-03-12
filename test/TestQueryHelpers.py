import unittest
from src.DB import QueryHelpers
from src.Helpers.Enums import Candle, Pair, Indicator


class TestQueryHelpers(unittest.TestCase):
    '''
    1
    '''
    def testGetCandleInsertQuery(self):
        candle = {'timestamp': 1583535600000, 'open': 239.99, 'high': 240.59, 'low': 239.75, 'close': 240.59, 'volume': 1768.84486 }
        marketPair = Pair.ETHUSDT
        candleSize = Candle.FIFTEEEN_MINUTE
        expected = "INSERT INTO ETHUSDT_OHLCV_15m(timestamp, open, high, low, close, volume) VALUES (to_timestamp(1583535600.0), '239.99', '240.59', '239.75', '240.59', '1768.84486');"
        received = QueryHelpers.getCandleInsertQuery(candle, marketPair, candleSize)
        self.assertEqual(expected, received)
    '''
    2
    '''
    def testCreateCandleTableQuery(self):
        low = 3
        high = 2
        marketPair = Pair.ETHUSDT
        candleSize = Candle.FIFTEEEN_MINUTE

        expected = "CREATE TABLE ETHUSDT_OHLCV_15m(timestamp TIMESTAMP PRIMARY KEY NOT NULL, open DECIMAL(3, 2), high  DECIMAL(3, 2), low DECIMAL(3, 2), close DECIMAL(3, 2), volume numeric(10));"
        received = QueryHelpers.getCreateCandleTableQuery(low, high, marketPair, candleSize)
        self.assertEqual(expected, received)


    '''
    4
    '''
    def testGetCandlesFromDBQuery(self):
        pair = Pair.ETHUSDT
        candleSize = Candle.FIFTEEEN_MINUTE
        limit = 10

        expected = 'SELECT timestamp, open, high, low, close, volume FROM ETHUSDT_OHLCV_15m ORDER BY timestamp DESC LIMIT 10;'
        received = QueryHelpers.getCandlesFromDBQuery(pair, candleSize, limit)
        self.assertEqual(expected, received)

        expected = 'SELECT timestamp, open, high, low, close, volume FROM ETHUSDT_OHLCV_15m ORDER BY timestamp DESC;'
        received = QueryHelpers.getCandlesFromDBQuery(pair, candleSize, None)
        self.assertEqual(expected, received)


    '''
    6
    '''
    def testGetIndicatorDataQuery(self):
        pair = Pair.ETHUSDT
        candleSize = Candle.FIFTEEEN_MINUTE
        indcator = Indicator.THREEOUTSIDE
        values = {"valuethreeoutside": 100}
        expected = "UPDATE ETHUSDT_OHLCV_15m SET threeoutside_valuethreeoutside = '100' WHERE timestamp = \'2020:01:01 00:00:00\';"

        actual = QueryHelpers.getInsertIndicatorsQueryString(indcator, values, '2020:01:01 00:00:00', candleSize, pair)
        self.assertEqual(actual, expected)

        #TODO add test for mulitple value case

    '''
    7
    '''
    def testGetTableDataQuery(self):
        pair = Pair.ETHUSDT
        candleSize = Candle.FIFTEEEN_MINUTE
        args = 80

        expected = "SELECT (timestamp, open, high, low, close, volume) FROM ETHUSDT_OHLCV_15m ORDER BY timestamp ASC LIMIT 80;"
        actual = QueryHelpers.getTableDataQuery(candleSize, pair, [args])
        self.assertEqual(expected, actual)
