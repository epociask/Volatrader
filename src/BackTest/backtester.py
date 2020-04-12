from datetime import datetime
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
from Helpers.HelpfulOperators import rewind
from DB.DBReader import *
from Helpers.Session import Session
from Strategies import strategies
from termcolor import colored
from Helpers.Enums import Pair, Candle 
import ccxt
import pandas as pd
from empyrical import max_drawdown, alpha_beta, sharpe_ratio
from empyrical.periods import DAILY, WEEKLY, MONTHLY, QUARTERLY, YEARLY
import numpy as np
import argparse
# from Strategies.strategies import STRAT


def backTest(pair: Pair, candleSize: Candle, strategy, stopLossPercent, takeProfitPercent, principle, timeEnum = None, shouldOutputToConsole = True, readFromDataBase=True, timeStart=None, outputToCSV=False) -> Session:
    """
    main backtest function, prints backtest results
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
    backTestingSession = Session(pair, strategy, takeProfitPercent, stopLossPercent, stratString, SessionType.BACKTEST)

    if readFromDataBase:
        reader = DBReader()

        if timeEnum is None:
            DataSet = reader.fetchCandlesWithIndicators(pair, candleSize)

        else:
            DataSet = reader.fetchCandlesWithIndicators(pair, candleSize, (timeEnum.value * (60 / int(re.findall(r'\d+', candleSize.value)[0]))))
    else:

        if timeStart is not None:
            DataSet = HelpfulOperators.convertCandlesToDict(HelpfulOperators.getFromTime(timeStart, pair, candleSize))

        else:
            DataSet = HelpfulOperators.convertCandlesToDict(HelpfulOperators.fetchCandleData(ccxt.kraken(), pair, candleSize, [500]))
    
    DataSet = sorted(DataSet, key=lambda i: int(i['candle']['timestamp']), reverse=False)

    start = HelpfulOperators.convertNumericTimeToString(DataSet[0]['candle']['timestamp']) if type(DataSet[0]['candle']['timestamp']) is int else DataSet[0]['candle']['timestamp'] 
    finish = HelpfulOperators.convertNumericTimeToString(DataSet[-1]['candle']['timestamp'])   if type(DataSet[-1]['candle']['timestamp']) is int else DataSet[-1]['candle']['timestamp'] 
    
    for candle in DataSet:
        backTestingSession.update(candle)
            

    if shouldOutputToConsole:
        print(colored(
            "\n\n"
            "------------------------------------------------------------------------------------------------------------\n",
            attrs=['bold']))

    endingPrice = float(principle + float(principle * (backTestingSession.getTotalPL() * .01)))
    endVal = colored("\t\tEnding Price: ", attrs=['bold']) + "$" + (
        colored(str(endingPrice), "blue") if float(endingPrice) > float(principle) else colored(str(endingPrice),
                                                                                                "red"))

    gainCount, lossCount = backTestingSession.getTradeData()

    print(
        f"\t\tPair: {pair.value}" + f"\n\t\tCandleSize: {candleSize.value}" +
        colored("\n\t\t Starting Principle Amount: $", attrs=['bold']) + str(principle) + "\n" +
        endVal +
        "\n\t\t" + colored("Total Profit Loss: ", attrs=['bold']) + (
            colored(f"+%{str(backTestingSession.getTotalPL())}", "green",
                    attrs=['underline']) if backTestingSession.getTotalPL() > 0 else colored(
                str(f"%{backTestingSession.getTotalPL()}%"), "red")) +
        colored("\n\t\tTotal Trades: ",
                attrs=['bold']) + f"{colored(backTestingSession.getTotalTrades(), 'magenta', attrs=['underline'])}"
                                  "\n\t\t" + colored("Starting Time:  ", attrs=['bold']) + colored(start, attrs=[
            "underline"]) +
        "\n\t\t" + colored("Finish: ", attrs=['bold']) + colored(finish, attrs=["underline"]) +
        colored("\n\t\t Number of profitable trades: ", attrs=['bold']) + f'{colored(str(gainCount), "blue")}' +
        "\n\t\t" + colored("Number of unprofitable trades: ", attrs=['bold']) + colored((lossCount), "red") +
        '\n\t\t' + f"Take Profit: {takeProfitPercent}" +
        '\n\t\t' + f"Stop Loss: {stopLossPercent}"
    )
    print(colored(f"\t\tSharp ratio: {sharpe_ratio(np.array(backTestingSession.profitlosses))}"))
    print(f"\n\t\tMax Drawdown: {max_drawdown(np.array(backTestingSession.profitlosses))}")

    print(colored(
        "\n"
        "------------------------------------------------------------------------------------------------------------\n",
        attrs=['bold']))

    if outputToCSV:
        print(backTestingSession.results())

        # returns = pd.DataFrame()
        

def main(args):
    backTest(args.pair, args.candleSize, args.strategy, args.stoploss, args.takeprofit, args.principle, args.readFromDatabase, args.outputToCSV)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Use this to backtest your strategies")
    parser.add_argument('--pair', type=Pair, required=True,
                    help='Pair to backtest for. Reference Enums.py for more details')
    parser.add_argument('--candleSize', type=Candle, required=True,
                    help="Candle size to get data for (5m, 15m, 30m, etc)")
    parser.add_argument('--strategy', type=str, required=True,
                    help="Strategy to backtest")
    parser.add_argument('-sl', '--stoploss', type=float, default=1.0,
                    help="Trailing stop loss percentage")
    parser.add_argument('-tp', '--takeprofit', type=float, default=2.0,
                    help="Take profit percentage")
    parser.add_argument('-p', '--principle', type=float, default=10000,
                    help="Starting capital")
    parser.add_argument('--readFromDatabase', type=bool, default=False)

    args = parser.parse_args(parser)
    main(args)
    #backTest(Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, "MA_STRATEGY", 2, 4, 10000, readFromDataBase=False, outputToCSV=True)
    
