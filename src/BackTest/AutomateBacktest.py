import os 
import sys
from sys import platform
sys.path.append(os.path.dirname(os.getcwd()))
from BackTest.BackTester import backTest
from Helpers.Constants.Enums import Pair, Candle, Time
import argparse
import os 


def automateAndVariate(pairs: list, candleSizes: list, stopLossRange: int, strategy, timeFrame=None, principle=1000):
    results = {}
    for pair in pairs:
        pair = Pair(pair)    
    
        for sl in range(stopLossRange):
            sl+=1
            tp = sl * 2
            for candleSize in candleSizes:
                candleSize = Candle(candleSize)
                result = backTest(pair, candleSize, strategy, sl, tp, principle, outputGraph=False, timeStart=Time["TWOWEEK"])
                results[result] = [pair, candleSize, sl, tp]
                os.system("cls")

    best = 0
    for result in results.keys():
        if int(result) > best:
            best = result 

    best_results = results[best]

    print("RUNNING BEST RESULT TO WEBPAGE")
    backTest(best_results[0], best_results[1], strategy, best_results[2], best_results[3], principle, outputGraph=True, timeStart=Time["TWOWEEK"])
if __name__ == "__main__":

    automateAndVariate(['ETHUSDT', 'BTCUSDT', 'XRPUSDT'], ['5m', '15m', '30m'], 4, 'FIFTY_MOVING_AVERAGE_STRATEGY', 'TWOWEEK', 10000)
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--Pairs")