import unittest
from BackTest.BackTesterSellLogic import Instance
from Helpers.Enums import Pair

class TestBackTesterSellLogic(unittest.TestCase):


    def testStopLossSell(self):
        instance = Instance(Pair.ETHUSDT)
        instance.setStopLossPercent(2)
        instance.run(100.00)
        self.assertEqual(instance.run(98.00), True)

    def testGlobalHigh(self):
        instance = Instance(Pair.ETHUSDT)
        instance.setStopLossPercent(2)
        instance.run(100.00)
        instance.run(101.00)
        instance.run(102.00)
        instance.run(100.00)
        print(instance.globalHigh)
        self.assertEqual(instance.globalHigh, 102.00)


    def testProfitLossEquation(self):
        instance = Instance(Pair.ETHUSDT)
        instance.setStopLossPercent(25)
        instance.run(100.00)
        self.assertEqual(instance.slVal, 75.00)


