# import unittest
# from DB.DBReader import DBReader
# from DB.DBoperations import DBoperations
# import ccxt
# from Helpers import HelpfulOperators
# from Helpers.Enums import Pair, Candle
#
# reader = DBReader()
# operator = DBoperations()
#
# #
# # class TestDBOperations(unittest.TestCase):
# #
# #     def testEquality(self):
# #         expected = None
# #         actual = operator.connect()
# #         self.assertEqual(expected, actual)
#
#
# class TestDBReader(unittest.TestCase):
#
#     received = None
#
#     def testFetchCandleData(self):
#         api = ccxt.binance()
#         pair = Pair.ETHUSDT
#         candleSize = Candle.FIFTEEEN_MINUTE
#
#         received = HelpfulOperators.fetchCandleData(api, pair, candleSize, [15])
#         self.assertIsNotNone(received)
#
#         received = HelpfulOperators.fetchCandleData(api, pair, candleSize, ['2020-02-15'])
#         self.assertIsNotNone(received)
#
#         received = HelpfulOperators.fetchCandleData(api, pair, candleSize, ['a'])
#         self.assertIsNotNone(received)
#     #
    # def testFetchCandlesWithIndicators(self):
    #     pair = Pair.ETHUSDT
    #     candleSize = Candle.FIFTEEEN_MINUTE
    #     received = reader.fetchCandlesWithIndicators(pair, candleSize, [Indi])
    #     self.assertIsNotNone(received)
    #     self.assertIsNotNone(received[0]['threeoutside']['value'])
    #     self.assertIsNotNone(received[0]['candle']['timestamp'])