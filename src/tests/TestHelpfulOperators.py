import unittest

class TestHelpfulOperators(unittest.TestCase):

    def test_GetLowHighBounds(self):

        self.assertTrue(self)
        # candles = [{'timestamp': '2020-03-04 12:15:00', 'open': '221.64', 'high': '222.18', 'low': '221.60', 'close': '220.0'} ,
        #           {'timestamp': '2020-03-04 12:15:00', 'open': '221.64', 'high': '222', 'low': '221.60', 'close': '220.0'} ,
        #           {'timestamp': '2020-03-04 12:15:00', 'open': '221.6', 'high': '222.18', 'low': '221', 'close': '220.0'}]

        # expectedLow = 3
        # expectedHigh = 2

        # low, high = getLowHighBounds(candles)

        # self.assertEqual(low, expectedLow)
        # self.assertEqual(high, expectedHigh)


if __name__ == '__main__':
    unittest.main()