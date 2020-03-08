# import unittest
# from BackTesterSession import Session
# from Enums import *
# from strategies import *
#
# class TestBacktester(unittest.TestCase):
#
#     ## TODO: This is not correct. Need to mock BacktestSession.Session Object in order to test its methods.
#     ## TODO: Need confidence in methods checkForSell, update, getTotalPandL
#     def __init__(self):
#         super().__init__()
#         self.pair = Pair.ETHUSDT
#         self.strat, self.indicators = getStrat('SIMPLY_BUY_STRAT')
#         self.takeProfit = 4
#         self.stopLoss = 2
#         self.session = Session(self.pair, self.strat, self.takeProfit, self.stopLoss)
#     def testAddResult(self):
#         self.session.addResult()
#         self.assertIsNotNone(self.results[0]['buytime'])