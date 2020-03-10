import unittest
import QueryHelpers
from Enums import Candle, Pair, Indicator
import IndicatorConstants

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
    3
    '''
    def testCreateIndicatorTableQuery(self):
        candle = Candle.FIFTEEEN_MINUTE
        pair = Pair.ETHUSDT
        indicator = Indicator.MORNINGSTAR

        expected = "CREATE TABLE morningstar_ETHUSDT_15m (timestampmorningstar timestamp PRIMARY KEY NOT NULL,  morningstarvalue VARCHAR, FOREIGN KEY(timestampmorningstar) REFERENCES ETHUSDT_OHLCV_15m(timestamp));"
        received = QueryHelpers.getCreateIndicatorTableQuery(candle, pair, indicator, IndicatorConstants.getIndicator(indicator.value))
        self.assertEqual(expected, received)
        indicator = Indicator.STOCHRSI
        indicator = Indicator.STOCHRSI
        expected = "CREATE TABLE stochrsi_ETHUSDT_15m (timestampstochrsi timestamp PRIMARY KEY NOT NULL, valuefastK VARCHAR, valueFastD VARCHAR, FOREIGN KEY(timestampstochrsi) REFERENCES ETHUSDT_OHLCV_15m(timestamp));"
        received = QueryHelpers.getCreateIndicatorTableQuery(candle, pair, indicator, IndicatorConstants.getIndicator(indicator.value))
        self.assertEqual(expected, received)

    '''
    4
    '''
    def testGetCandlesFromDBQuery(self):
        pair = Pair.ETHUSDT
        candleSize = Candle.FIFTEEEN_MINUTE
        limit = 10

        expected = 'SELECT * FROM ETHUSDT_OHLCV_15m ORDER BY timestamp DESC LIMIT 10;'
        received = QueryHelpers.getCandlesFromDBQuery(pair, candleSize, limit)
        self.assertEqual(expected, received)

        expected = 'SELECT * FROM ETHUSDT_OHLCV_15m ORDER BY timestamp DESC;'
        received = QueryHelpers.getCandlesFromDBQuery(pair, candleSize, None)
        self.assertEqual(expected, received)

    '''
    5
    '''
    def testMakeEqualities(self):
        testBTC = ['BTCUSDT_OHLCV_15m', 'stochrsi_BTCUSDT_15m']
        expected_query1 = "WHERE BTCUSDT_OHLCV_15m.timestamp = stochrsi_BTCUSDT_15m.timestampstochrsi ;"
        expected_query2 = " ALTER TABLE mytable DROP COLUMN timestampstochrsi ;"

        result1, result2 = QueryHelpers.getWhereEqualsQuery(testBTC)
        self.assertEqual(result1, expected_query1 , 'Correct WHERE statement generated')
        self.assertEqual(result2, expected_query2, 'Correct ALTER TABLE statement generated')

    '''
    6
    '''
    def testGetIndicatorDataQuery(self):
        pair = Pair.ETHUSDT
        candleSize = Candle.FIFTEEEN_MINUTE
        indcator = Indicator.THREEOUTSIDE
        values = {"valuethreeoutside": 100}
        expected = 'INSERT INTO threeoutside_ETHUSDT_15m (timestampthreeoutside, valuethreeoutside) VALUES (\'2020:01:01 00:00:00\', 100);'

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

        expected = "SELECT * FROM ETHUSDT_OHLCV_15m ORDER BY timestamp ASC LIMIT 80;"
        actual = QueryHelpers.getTableDataQuery(candleSize, pair, [args])
        self.assertEqual(expected, actual)

    def testFetchgetIndicatorDataQuery(self):
        pair = Pair.ETHUSDT
        candleSize = Candle.FIFTEEEN_MINUTE
        indicator = Indicator.MORNINGSTAR
        limit = 30

        expected = "SELECT * FROM morningstar_ETHUSDT_15m ORDER BY timestamp DESC LIMIT 30;"
        actual = QueryHelpers.getIndicatorDataQuery(pair, candleSize, indicator, limit)
        self.assertEqual(expected, actual)