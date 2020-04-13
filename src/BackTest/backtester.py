import datetime
import sys, os
from sys import platform
sys.path.append(os.path.dirname(os.getcwd()))
from Helpers.TimeHelpers import convertNumericTimeToString
from DataBasePY.DBReader import *
from Trader.TradeSession import TradeSession
from Strategies import strategies
from Helpers.Constants.Enums import Pair, Candle, Time
import ccxt
import pandas as pd
from empyrical import max_drawdown, alpha_beta, sharpe_ratio
from empyrical.periods import DAILY, WEEKLY, MONTHLY, QUARTERLY, YEARLY
import numpy as np
import argparse
import subprocess, platform
from Helpers.DataOperators import printLogo
from Helpers import TimeHelpers
from BacktestBuilder import * 
from Trader.Indicators import IndicatorFunctions


def backTest(pair: Pair, candleSize: Candle, strategy: str, stopLossPercent: int, takeProfitPercent: int, principle: int, timeStart: Time, readFromDataBase=False, outputGraph=False):
    """
    main backtest function, prints backtest results, outputs graph results to html if desired 
    @:param pair -> pair you wish to run backtest on
    @:param candleSize -> size of candle you wish to use
    @:param strategy -> Buying strategy that you wish to implement
    @:param Stop-Loss percent
    @:param Take profit percent -> percent gain from buy-price at which you wish to sell
    @:param args optional TIME ENUM to specify timeline to test strategy upon
    """

    assert stopLossPercent in range(1, 100)
    assert takeProfitPercent in range(1, 100)
    assert type(pair) is Pair
    assert (type(candleSize)) is Candle

    takeProfitPercent = f"0{takeProfitPercent}" if takeProfitPercent - 10 <= 0 else f"{takeProfitPercent}"
    stratString = strategy
    strategy = strategies.getStrat(stratString)
    strategy = strategy(pair, candleSize, principle)
    backTestingSession = TradeSession(pair, strategy, takeProfitPercent, stopLossPercent, stratString, SessionType.BACKTEST)
    printLogo(type=SessionType.BACKTEST)


    if readFromDataBase:
        reader = DBReader()
        DataSet = reader.fetchCandlesWithIndicators(pair, candleSize)

    else:
        DataSet = DataOperators.convertCandlesToDict(DataOperators.getCandlesFromTime(convertNumericTimeToString(TimeHelpers.rewind(str(datetime.datetime.now())[0: -7], 60, timeStart.value )), pair, candleSize))

        # else:
        #     DataSet = DataOperators.convertCandlesToDict(DataOperators.fetchCandleData(ccxt.binance(), pair, candleSize, 500))

    DataSet = sorted(DataSet, key=lambda i: int(i['candle']['timestamp']), reverse=False)

    for candle in DataSet:
        backTestingSession.update(candle)


    # Printing Results
    start = TimeHelpers.convertNumericTimeToString(DataSet[0]['candle']['timestamp']) if type(DataSet[0]['candle']['timestamp']) is int else DataSet[0]['candle']['timestamp']
    finish = TimeHelpers.convertNumericTimeToString(DataSet[-1]['candle']['timestamp'])   if type(DataSet[-1]['candle']['timestamp']) is int else DataSet[-1]['candle']['timestamp']

    totalPl = backTestingSession.getTotalPL()
    endingPrice = float(principle + float(principle * (totalPl * .01)))

    gainCount, lossCount = backTestingSession.getTradeData()

    print(getBacktestResultsString(stratString, candleSize, pair, principle, endingPrice, totalPl, 
        gainCount+lossCount, start, finish, gainCount, lossCount, stopLossPercent, takeProfitPercent))


    # Outputs Graphs to dashboard.html, rename file to save for future reference
    if outputGraph:
        getInt = lambda val : int(convertNumericTimeToString(val['buytime'])[8 : 10])
        results = backTestingSession.getResults()['tradeResults']
        ts = getInt(results[0])
        timestamps = []
        profitlosses = []
        prevData = None
        pl = 0
        for val in backTestingSession.getResults()['tradeResults']:
            if ts == getInt(val):
                pl += val['profitloss']

            else:
                ts = getInt(val)
            
                timestamps.append(convertNumericTimeToString(prevData['buytime'])[0 : 10])
                profitlosses.append(pl)
                pl = val['profitloss']
            prevData = val

        buyTimes = [e['buytime'] for e in results]
        sellTimes = [e['selltime'] for e in results]
        pls = [e['profitloss'] for e in results]
        print('profit losses ----------->', pls)
        candles = [e['candle'] for e in DataSet]
        plIndex = 0
        candleLimit = 15
        closes = []
        for index, candle in enumerate(candles):
            if candle['timestamp'] in buyTimes:
                candle['buy'] = candle['close']
                candle['sell'] = "NaN"

            elif candle['timestamp'] in sellTimes:
                candle['sell'] = candle['close']
                candle['buy'] = 'NaN'
                plIndex+=1

            else:
                candle['sell'] = 'NaN'
                candle['buy'] = 'NaN'

            if candleLimit <= 0:
                candle['sma_15'] = IndicatorFunctions.SMA(closes, 15)[-1]
                candle['sma_5'] = IndicatorFunctions.SMA(closes, 5)[-1]
                candle['sma_8'] = IndicatorFunctions.SMA(closes, 8)[-1]
            candle['timestamp'] = convertNumericTimeToString(candle['timestamp'])
            candle['principle'] = backTestingSession.principleOverTime[index]
            candles[index] = candle

            closes.append(candle['close'])
            candleLimit -= 1 
                
        sharpe_ratios = []
        temp = []
        for pnl in profitlosses:
            temp.append(pnl)
            sharpe_ratios.append(sharpe_ratio(np.array(temp)))
        candles_returns = pd.DataFrame(candles)
        filename = figures_to_html(generateGraphs(candles_returns, pair, candleSize, stratString))

        # Open html doc on windows or mac
        os.system(f"{'start' if platform.system() == 'Windows' else 'open'} {filename}")



def main(args):
    print("RUNNING BACKTEST WITH ARGS: ", args)
    print(type(args.time))
    backTest(args.pair, args.candleSize, args.strategy, args.stoploss, args.takeprofit, args.principle, Time[args.time], readFromDataBase=args.readFromDatabase,  outputGraph=args.outputGraph)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Use this to backtest your strategies")
    parser.add_argument('-p', '--pair', type=Pair, required=True,
                    help='Pair to backtest for. Reference Enums.py for more details')
    parser.add_argument('--candleSize', '-candle', type=Candle, required=True,
                    help="Candle size to get data for (5m, 15m, 30m, etc)")
    parser.add_argument('--strategy', '-strat', type=str, required=True,
                    help="Strategy to backtest")
    parser.add_argument('-sl', '--stoploss', type=int, default=1,
                    help="Trailing stop loss percentage")
    parser.add_argument('-tp', '--takeprofit', type=int, default=2,
                    help="Take profit percentage")
    parser.add_argument('--principle', '-investment', type=int, default=10000,
                    help="Starting capital")
    parser.add_argument('--readFromDatabase', type=bool, default=False,
                    help="Reads from database if true, otherwise gets live candle data from API")
    parser.add_argument('--outputGraph', type=bool, default=True,
                    help="Outputs backtest results into csv if true, otherwise does not")
    parser.add_argument('-t','--time', type=str, default="MONTH",
                    help="Total time to backtest on")

    args = parser.parse_args()
    main(args)
