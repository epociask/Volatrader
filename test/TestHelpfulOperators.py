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

