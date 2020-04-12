from datetime import datetime
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
from Helpers.HelpfulOperators import convertNumericTimeToString
from DB.DBReader import *
from Helpers.Session import Session
from Strategies import strategies
from termcolor import colored
from Helpers.Enums import Pair, Candle, Time
import ccxt
import pandas as pd
from empyrical import max_drawdown, alpha_beta, sharpe_ratio
from empyrical.periods import DAILY, WEEKLY, MONTHLY, QUARTERLY, YEARLY
import numpy as np
import argparse
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from colorama import init
from termcolor import cprint 
from pyfiglet import figlet_format



def printLogo():
    init(strip=not sys.stdout.isatty()) 
    cprint(figlet_format('VolaTrade\n Backtest', font='starwars'),
       'white', 'on_cyan', attrs=['blink'])

def generateGraph(candle_data):

    candle_data.index = pd.to_datetime(candle_data['timestamp'])
    print("COLS: ", candle_data.columns)
    # del candle_data['Unnamed: 0']
    del candle_data['timestamp']
    print(candle_data)

    fig = make_subplots(rows=1, cols=1)

    fig.add_trace(go.Ohlc(x=candle_data.index,
                        open=candle_data['open'],
                        high=candle_data['high'],
                        low=candle_data['low'],
                        close=candle_data['close'],
                        name="Candles"))

    fig.add_trace(go.Scatter(x=candle_data.index, y=candle_data['buy'], mode='markers', line=dict(color='royalblue', width=4), name = "BUY"))
    fig.add_trace(go.Scatter(x=candle_data.index, y=candle_data['sell'], mode='markers', line=dict(color='yellow', width=4), name="SELL"))

    fig.update_layout(autosize=True)
    return fig


def backTest(pair: Pair, candleSize: Candle, strategy, stopLossPercent, takeProfitPercent, principle, shouldOutputToConsole = True, readFromDataBase=False, timeStart=None, outputGraph=False) -> Session:
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
    printLogo()
    if readFromDataBase:
        reader = DBReader()

        DataSet = reader.fetchCandlesWithIndicators(pair, candleSize)

    else:

        if timeStart is not None:
            DataSet = HelpfulOperators.convertCandlesToDict(HelpfulOperators.getFromTime(timeStart, pair, candleSize))

        else:
            DataSet = HelpfulOperators.convertCandlesToDict(HelpfulOperators.fetchCandleData(ccxt.binance(), pair, candleSize, 500))

    DataSet = sorted(DataSet, key=lambda i: int(i['candle']['timestamp']), reverse=False)

    start = HelpfulOperators.convertNumericTimeToString(DataSet[0]['candle']['timestamp']) if type(DataSet[0]['candle']['timestamp']) is int else DataSet[0]['candle']['timestamp']
    finish = HelpfulOperators.convertNumericTimeToString(DataSet[-1]['candle']['timestamp'])   if type(DataSet[-1]['candle']['timestamp']) is int else DataSet[-1]['candle']['timestamp']
    count = 0 
    for candle in DataSet:
        backTestingSession.update(candle)


    if shouldOutputToConsole:
        print(colored(
            "\n\n"
            "------------------------------------------------------------------------------------------------------------\n",
            attrs=['bold']))
    if count % 3 == 0:
        os.system("clear")

    count+=1


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
        candles = [e['candle'] for e in DataSet]
        
        for index, candle in enumerate(candles):
            if candle['timestamp'] in buyTimes:
                candle['buy'] = candle['close']
                candle['sell'] = "NaN"
            

            elif candle['timestamp'] in sellTimes:
                candle['sell'] = candle['close']
                candle['buy'] = 'NaN'

            else:
                candle['sell'] = 'NaN'
                candle['buy'] = 'NaN'

            candle['timestamp'] = convertNumericTimeToString(candle['timestamp'])
            candles[index] = candle
                

        pnl_returns = pd.Series(index=timestamps, data=profitlosses)
        candles_returns = pd.DataFrame(candles)
        generateGraph(candles_returns).show()


def main(args):
    print("RUNNING BACKTEST WITH ARGS: ", args)
    backTest(args.pair, args.candleSize, args.strategy, args.stoploss, args.takeprofit, args.principle, args.readFromDatabase, outputGraph=args.outputGraph, timeStart="2020-04-01 00:00:00")

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
    parser.add_argument('-t','--time', type=Time, default=Time.MONTH,
                    help="Total time to backtest on")

    args = parser.parse_args()
    main(args)
