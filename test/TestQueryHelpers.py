import unittest
import QueryHelpers
from Enums import Candle, Pair, Indicator
import IndicatorConstants
from QueryHelpers import *

class TestQueryHelpers(unittest.TestCase):

    def testGetCandleInsertQuery(self):
        candle = {'timestamp': 1583535600000, 'open': 239.99, 'high': 240.59, 'low': 239.75, 'close': 240.59, 'volume': 1768.84486 }
        marketPair = Pair.ETHUSDT
        candleSize = Candle.FIFTEEEN_MINUTE
        expected = "INSERT INTO ETHUSDT_OHLCV_15m(timestamp, open, high, low, close, volume) VALUES (to_timestamp(1583535600.0), '239.99', '240.59', '239.75', '240.59', '1768.84486');"
        received = getCandleInsertQuery(candle, marketPair, candleSize)
        self.assertEqual(expected, received)

    def testCreateCandleTableQuery(self):
        low = 3
        high = 2
        marketPair = Pair.ETHUSDT
        candleSize = Candle.FIFTEEEN_MINUTE

        expected = "CREATE TABLE ETHUSDT_OHLCV_15m(timestamp TIMESTAMP PRIMARY KEY NOT NULL, open DECIMAL(3, 2), high  DECIMAL(3, 2), low DECIMAL(3, 2), close DECIMAL(3, 2), volume numeric(10));"
        received = getCreateCandleTableQuery(low, high, marketPair, candleSize)
        self.assertEqual(expected, received)

    def testCreateIndicatorTableQuery(self):
        candle = Candle.FIFTEEEN_MINUTE
        pair = Pair.ETHUSDT
        indicator = Indicator.MORNINGSTAR

        expected = "CREATE TABLE morningstar_ETHUSDT_15m (timestampmorningstar timestamp PRIMARY KEY NOT NULL,  morningstarvalue VARCHAR, FOREIGN KEY(timestampmorningstar) REFERENCES ETHUSDT_OHLCV_15m(timestamp));"
        received = QueryHelpers.getCreateIndicatorTableQuery(candle, pair, indicator, IndicatorConstants.getIndicator(indicator.value))
        self.assertEqual(expected, received)
        indicator = Indicator.STOCHRSI
        expected = "CREATE TABLE stochrsi_ETHUSDT_15m (timestampstochrsi timestamp PRIMARY KEY NOT NULL, valuefastK VARCHAR, valueFastD VARCHAR, FOREIGN KEY(timestampstochrsi) REFERENCES ETHUSDT_OHLCV_15m(timestamp));"
        received = getCreateIndicatorTableQuery(candle, pair, indicator, IndicatorConstants.getIndicator(indicator.value))
        self.assertEqual(expected, received)

    def testGetCandlesFromDBQuery(self):
        pair = Pair.ETHUSDT
        candleSize = Candle.FIFTEEEN_MINUTE
        limit = 10

        expected = 'SELECT * FROM ETHUSDT_OHLCV_15m ORDER BY timestamp DESC LIMIT 10;'
        received = getCandlesFromDBQuery(pair, candleSize, limit)
        self.assertEqual(expected, received)

        expected = 'SELECT * FROM ETHUSDT_OHLCV_15m ORDER BY timestamp DESC;'
        received = getCandlesFromDBQuery(pair, candleSize, None)
        self.assertEqual(expected, received)

    def testMakeEqualities(self):
        testBTC = ['BTCUSDT_OHLCV_15m', 'stochrsi_BTCUSDT_15m']
        expected_query1 = "WHERE BTCUSDT_OHLCV_15m.timestamp = stochrsi_BTCUSDT_15m.timestampstochrsi ;"
        expected_query2 = " ALTER TABLE mytable DROP COLUMN timestampstochrsi ;"

        result1, result2 = getWhereEqualsQuery(testBTC)
        self.assertEqual(result1, expected_query1 , 'Correct WHERE statement generated')
        self.assertEqual(result2, expected_query2, 'Correct ALTER TABLE statement generated')

    def testInsertIndicatorsQueryString(self):
        indicator = Indicator.ACOS
        indicatorValues = {'value': None}
        timestamp = '2020-03-09 16:00:00'
        candleSize = Candle.FIFTEEEN_MINUTE
        pair = Pair.ETHUSDT

        expected = "INSERT INTO acos_ETHUSDT_15m (timestampacos, acosvalue) VALUES ('2020-03-09 16:00:00', 'none');"
        received = getInsertIndicatorsQueryString(indicator, indicatorValues, timestamp, candleSize, pair)
        self.assertEqual(expected, received)

        indicator = Indicator.AROON
        indicatorValues = {'valueAroonDown': 64.28571428571429, 'valueAroonUp': 28.571428571428573}

        received = getInsertIndicatorsQueryString(indicator, indicatorValues, timestamp, candleSize, pair)
        expected = "INSERT INTO aroon_ETHUSDT_15m (timestamparoon, valueAroonDown, valueAroonUp) VALUES ('2020-03-09 16:00:00', 64.28571428571429, 28.571428571428573);"

        self.assertEqual(expected, received)