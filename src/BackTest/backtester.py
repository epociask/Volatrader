from datetime import datetime
from Helpers.HelpfulOperators import rewind
from DB.DBReader import *
from Helpers.Session import Session
from Strategies import strategies
from termcolor import colored
from Helpers.Enums import *


def backTest(pair: Pair, candleSize: Candle, strategy, stopLossPercent, takeProfitPercent, principle, *args):
    """
    main backtest function, prints backtest results
    @:param pair -> pair you wish to run backtest on
    @:param candleSize -> size of candle you wish to use
    @:param strategy -> Buying strategy that you wish to implement
    @:param Stop-Loss percent
    @:param Take profit percent -> percent gain from buy-price at which you wish to sell
    @:param args optional TIME ENUM to specify timeline to test strategy upon
    """

    assert len(args) == 0 or len(args) == 1
    assert stopLossPercent in range(1, 100)
    assert takeProfitPercent in range(1, 100)
    assert type(pair) is Pair
    assert(type(candleSize)) is Candle

    takeProfitPercent = f"0{takeProfitPercent}" if takeProfitPercent - 10 <= 0 else f"{takeProfitPercent}"

    strategy, indicators = strategies.getStrat(strategy)
    test = Session(pair, strategy, takeProfitPercent, stopLossPercent)
    reader = DBReader()

    if len(args) is 0:
        DataSet = reader.fetchCandlesWithIndicators(pair, candleSize, indicators)

    else:
        timeNow = str(datetime.now())[0: -7]
        DataSet = reader.fetchCandlesWithIndicators(pair, candleSize, indicators, rewind(timeNow, args[0].value, 60))
    start = DataSet[0]['candle']['timestamp']
    finish = DataSet[-1]['candle']['timestamp']
    print("Dataset :::: ", DataSet)
    for data in DataSet:
        print(colored(data, "blue", attrs=['blink']))
        test.update(data)
    print(colored(
        "\n\n"
        "------------------------------------------------------------------------------------------------------------\n",
        attrs=['bold']))



    endingPrice = float(principle + float(principle * (test.getTotalPL()*.01)))
    endVal = colored("\t\tEnding Price: ", attrs=['bold']) + "$" + (colored(str(endingPrice), "blue") if float(endingPrice) > float(principle) else colored(str(endingPrice), "red"))

    gainCount, lossCount = test.getTradeData()

    print(
        colored("\t\t Starting Principle Amount: $", attrs=['bold']) + str(principle) + "\n" +
        endVal +
        "\n\t\t" + colored("Total Profit Loss: ", attrs=['bold']) + (
            colored(f"+%{str(test.getTotalPL())}", "green", attrs=['underline']) if test.getTotalPL() > 0 else colored(
                str(f"%{test.getTotalPL()}%"), "red")) +
        colored("\n\t    Total Trades: ",
                attrs=['bold']) + f"{colored(test.getTotalTrades(), 'magenta', attrs=['underline'])}"
                                  "\n\t\t" + colored("Starting Time:  ", attrs=['bold']) + colored(start, attrs=["underline"]) +
        "\n\t\t" + colored("Finish: ", attrs=['bold']) + colored(finish, attrs=["underline"]) +
        colored("\n\t\t Number of profitable trades: ", attrs=['bold']) + f'{colored(str(gainCount), "blue")}' +
        "\n\t\t" + colored("Number of unprofitable trades: ", attrs=['bold']) + colored((lossCount), "red") +
        '\n\t\t'
    )
    print(colored(
        "\n"
        "------------------------------------------------------------------------------------------------------------\n",
        attrs=['bold']))


backTest(Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, "SIMPLE_BUY_STRAT", 2, 4, 10000, Time.MONTH)
