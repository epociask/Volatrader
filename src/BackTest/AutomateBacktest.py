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

    print("===================BEST RESULT FOUND.... CONVERTING TO TEARSHEET==================================")
    backTest(best_results[0], best_results[1], strategy, best_results[2], best_results[3], principle, outputGraph=True, timeStart=Time["TWOWEEK"])


def main(args):
    print("running w/ args ", args)
    automateAndVariate(args.pairs, args.candles, args.stoploss, args.strategy, args.time, args.principle)
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Use this to backtest your strategies")
    parser.add_argument('-p', '--pairs', type=str, required=True, nargs='*',
                    help='Pairs to backtest for. Reference Enums.py for more details')
    parser.add_argument('--candles', '-candleSizes', type=str, required=True, nargs='*',
                    help="Candle size to get data for (5m, 15m, 30m, etc)")
    parser.add_argument('--strategy', '-strat', type=str, required=True,
                    help="Strategy to backtest")
    parser.add_argument('-sl', '--stoploss', type=int, default=1,
                    help="Trailing stop loss percentage")
    parser.add_argument('--principle', '-investment', type=int, default=10000,
                    help="Starting capital")
    parser.add_argument('-t','--time', type=str, default="MONTH",
                    help="Total time to backtest on")
    parser.add_argument("--market", type=str, default="BINANCE",
                    help="Market to be used")

    args = parser.parse_args()
    main(args)

