import time
from datetime import datetime
from Helpers.Logger import logToSlack, logDebugToFile
from Helpers.Session import Session
from Helpers.Logger import Channel
from Helpers.Enums import Pair, Candle, SessionType
from DB.DBReader import DBReader
from Strategies import strategies
from Helpers.HelpfulOperators import getCurrentKrakenPrice, fetchCandleData, convertCandlesToDict
import ccxt
import re 

convertToVal = lambda candleEnum: candleEnum.value[0: len(candleEnum.value) - 2]


class PaperTrader:

    def __init__(self):
        self.takeProfitPercent = None
        self.strategy = None
        self.tradingSession = None
        self.pair = None
        self.candleSize = None
        self.stratName = None
        self.strategy = None
        self.takeProfitPercent = None
        self.stopLossPercent = None
        self.principle = None



    def getResults(self) -> str:
        return self.tradingSession.getResults()


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
        self.timeStep = int(re.sub("[^0-9]", "", candleSize.value))
        print(self.timeStep)
        self.pair = pair
        self.candleSize = candleSize
        self.takeProfitPercent = f"0{takeProfitPercent}" if takeProfitPercent - 10 <= 0 else f"{takeProfitPercent}"
        self.stratName = strategy
        strategy = strategies.getStrat(self.stratName)
        self.strategy = strategy(pair, candleSize, principle)
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
        sold = False 
        logToSlack(f"Starting Paper Trader for {self.pair.value}/{self.candleSize.value} \nstrat: {self.stratName}\n takeprofit: %{int(self.takeProfitPercent)}\n stoploss: %{self.stopLossPercent}", channel=Channel.PAPERTRADER)
        while True:
            t = int(str(datetime.now())[14:16])

            if first:
                first = False 


                try:
                    print("starting preinstall for strat")
                    for candle in convertCandlesToDict(fetchCandleData(ccxt.kraken(), self.pair, self.candleSize, self.strategy.candleLimit)):
                        self.tradingSession.update(candle)


                except:
                    logDebugToFile("Error instantiating strategy in paper trader")

            if (t % self.timeStep == 0 or t == 0) and not sold:
                time.sleep(6)
                data = convertCandlesToDict(fetchCandleData(ccxt.kraken(), self.pair, self.candleSize, 1))
                sold = self.tradingSession.update(data[0], True)
                if not sold:    
                    time.sleep(60)


            if t == 0 or t == 15 or t == 30 or t == 45:
                logToSlack(f"[PAPERTRADER] hourly update for {self.pair.value} for strat: {self.stratName} \n {self.getResults()}", channel=Channel.PAPERTRADER)


            if sold:
                time.sleep(5)
                price, ts = getCurrentKrakenPrice(self.pair)
                dummyCandle = {"candle" : {"close": price, "timestamp": ts}}
                self.tradingSession.update(dummyCandle)