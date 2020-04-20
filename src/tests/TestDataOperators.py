import unittest
import sys, os
from sys import platform
sys.path.append(os.path.dirname(os.getcwd()))
from Helpers.DataOperators import convertCandlesToDict


class TestDataOperators(unittest.TestCase):


    def testConvertCandlesToDict(self):

        candles = [[113234, 1,1,1,1, 3], [14341234, 2,2,2,2, 4]]
        expected = [{"timestamp": 113234, 'open': 1, 'high': 1, 'low': 1,'close': 1, 'volume': 3}, {"timestamp": 14341234,    'open': 2, 'high': 2, 'low': 2,'close': 2, 'volume': 4}]
        output = convertCandlesToDict(candles)
        print(candles)
        self.assertEqual(expected, output)