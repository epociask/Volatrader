import unittest
import HelpfulOperators



class TestHelpfulOperators(unittest.TestCase):

    def testMakeEqualities(self):
        testBTC =  ['BTCUSDT_OHLCV_15m', 'stochrsi_BTCUSDT_15m']
        expected_query1 = "WHERE BTCUSDT_OHLCV_15m.timestamp = stochrsi_BTCUSDT_15m.timestampstochrsi ;"
        expected_query2 = " ALTER TABLE mytable DROP COLUMN timestampstochrsi ;"

        result1, result2 = HelpfulOperators.makeEqualities(testBTC)
        self.assertEqual(result1, expected_query1 , 'Correct WHERE statement generated')
        self.assertEqual(result2, expected_query2, 'Correct ALTER TABLE statement generated')


    def testGetLowHighBounds(self):
        candles = [{'timestamp': '2020-03-04 12:15:00', 'open': '221.64', 'high': '222.18', 'low': '221.60', 'close': '220.0'} ,
                  {'timestamp': '2020-03-04 12:15:00', 'open': '221.64', 'high': '222', 'low': '221.60', 'close': '220.0'} ,
                  {'timestamp': '2020-03-04 12:15:00', 'open': '221.6', 'high': '222.18', 'low': '221', 'close': '220.0'}]

        expectedLow = 3
        expectedHigh = 2

        low, high = HelpfulOperators.getLowHighBounds(candles)

        self.assertEqual(low, expectedLow)
        self.assertEqual(high, expectedHigh)
