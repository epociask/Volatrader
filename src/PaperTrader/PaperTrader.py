import time
from datetime import datetime
from Helpers.Logger import logToSlack
from Helpers.Session import Session
from Helpers.Logger import Channel
from Helpers.Enums import Pair, Candle, SessionType
from DB.DBReader import DBReader
from Strategies import strategies
from Helpers.HelpfulOperators import getCurrentBinancePrice, fetchCandleData, convertCandlesToDict
import ccxt

convertToVal = lambda candleEnum: candleEnum.value[0: len(candleEnum.value) - 2]


class PaperTrader:

    def __init__(self, timeStep):
        self.takeProfitPercent = None
        self.strategy = None
        self.tradingSession = None
        self.timeStep = timeStep


    def trade(self, pair: Pair, candleSize: Candle, strategy: str, stopLossPercent: int, takeProfitPercent: int,
            principle: int):
        """

        :param pair:
        :param candleSize:
        :param strategy:
        :param stopLossPercent:
        :param takeProfitPercent:
        :param principle:
        :return:
        """
        self.pair = pair
        self.candleSize = candleSize
        self.takeProfitPercent = f"0{takeProfitPercent}" if takeProfitPercent - 10 <= 0 else f"{takeProfitPercent}"
        self.stratName = strategy
        strategy = strategies.getStrat(self.stratName)
        self.strategy = strategy(pair, candleSize, 100)
        self.indicators = self.strategy.indicatorList
        print(self.indicators)
        self.stopLossPercent = stopLossPercent
        self.tradingSession = Session(pair, self.strategy, takeProfitPercent, self.stopLossPercent, self.stratName,
                                    SessionType.PAPERTRADE)
        self.principle = principle
        self.start()


    def start(self):
        """

        :return:
        """
        first = True 
        logToSlack(f"Starting Paper Trader for {self.pair.value}/{self.candleSize.value} \nstrat: {self.stratName}\n takeprofit: %{int(self.takeProfitPercent)}\n stoploss: %{self.stopLossPercent}", channel=Channel.VOLATRADER)
        while True:
            t = int(str(datetime.now())[14:16])
            if (t % self.timeStep == 0 or t == 0):
                time.sleep(30)
                data = convertCandlesToDict(fetchCandleData(ccxt.kraken(), self.pair, self.candleSize, [1]))
                self.tradingSession.update(data[0])

            if first:
                first = False 

                data = convertCandlesToDict(fetchCandleData(ccxt.kraken(), self.pair, self.candleSize, [14]))

                for i in range(14):
                    self.tradingSession.update(data[i])
