from datetime import datetime
from Helpers.HelpfulOperators import rewind
from DB.DBReader import *
from Helpers.Session import Session
from Strategies import strategies
from termcolor import colored
from Helpers.Enums import *
import re
# from Strategies.strategies import STRAT


def backTest(pair: Pair, candleSize: Candle, strategy, stopLossPercent, takeProfitPercent, principle, timeEnum = None, shouldOutputToConsole = True) -> Session:
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
    strategy = strategy(pair, candleSize)
    indicators = strategy.indicatorList
    backTestingSession = Session(pair, strategy, takeProfitPercent, stopLossPercent, stratString, SessionType.BACKTEST)
    reader = DBReader()

    if timeEnum is None:
        DataSet = reader.fetchCandlesWithIndicators(pair, candleSize, indicators)

    else:
        DataSet = reader.fetchCandlesWithIndicators(pair, candleSize, indicators, (timeEnum.value * (60 / int(re.findall(r'\d+', candleSize.value)[0]))))

    DataSet = sorted(DataSet, key=lambda i: i['candle']['timestamp'], reverse=False)
    start = DataSet[0]['candle']['timestamp']
    finish = DataSet[-1]['candle']['timestamp']
    # print("Dataset :::: ", DataSet)
    for data in DataSet:
        if shouldOutputToConsole:
            print(colored(data, "blue", attrs=['blink']))
        backTestingSession.update(data)

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
        colored("\n\t    Total Trades: ",
                attrs=['bold']) + f"{colored(backTestingSession.getTotalTrades(), 'magenta', attrs=['underline'])}"
                                  "\n\t\t" + colored("Starting Time:  ", attrs=['bold']) + colored(start, attrs=[
            "underline"]) +
        "\n\t\t" + colored("Finish: ", attrs=['bold']) + colored(finish, attrs=["underline"]) +
        colored("\n\t\t Number of profitable trades: ", attrs=['bold']) + f'{colored(str(gainCount), "blue")}' +
        "\n\t\t" + colored("Number of unprofitable trades: ", attrs=['bold']) + colored((lossCount), "red") +
        '\n\t\t' + f"Take Profit: {takeProfitPercent}" +
        '\n\t\t' + f"Stop Loss: {stopLossPercent}"
    )
    print(colored(
        "\n"
        "------------------------------------------------------------------------------------------------------------\n",
        attrs=['bold']))

    return backTestingSession, start, finish


