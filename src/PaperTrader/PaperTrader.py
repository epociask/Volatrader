import time
from datetime import datetime
from Helpers.Logger import logToSlack, logDebugToFile
from Trader.TradeSession import TradeSession
from Helpers.Logger import Channel
from Helpers.Constants.Enums import Pair, Candle, SessionType
from DataBasePY.DBReader import DBReader
from DataBasePY.DBwriter import DBwriter
from Strategies import strategies
from Helpers.DataOperators import fetchCandleData, convertCandlesToDict
from Helpers.API.MarketFunctions import getCurrentBinancePrice
import ccxt
import re 
from Helpers.DataOperators import printLogo

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
        self.startTime = None
        self.currentPrice = None
        self.writer = DBwriter()
        self.sessionId = None


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
        self.tradingSession = TradeSession(pair, self.strategy, takeProfitPercent, self.stopLossPercent, self.stratName,
                                    SessionType.PAPERTRADE)
        self.principle = principle
        self.sessionId = self.tradingSession.getSessionId()
        self.start()



    def start(self):
        """

        :return:
        """
        printLogo(SessionType.PAPERTRADE)
        first = True 
        sold = False 
        logToSlack(f"Starting Paper Trader for {self.pair.value}/{self.candleSize.value} \nstrat: {self.stratName}\n takeprofit: %{int(self.takeProfitPercent)}\n stoploss: %{self.stopLossPercent}", channel=Channel.PAPERTRADER)
        while True:
            t = int(str(datetime.now())[14:16])

            if first:
                first = False 

                try:
                    print("starting preinstall for strat")
                    for candle in convertCandlesToDict(fetchCandleData(ccxt.binance(), self.pair, self.candleSize, self.strategy.candleLimit)):
                        self.tradingSession.update(candle)


                except:
                    logDebugToFile("Error instantiating strategy in paper trader")

            if (t % self.timeStep == 0 or t == 0):
                time.sleep(6)
                data = convertCandlesToDict(fetchCandleData(ccxt.binance(), self.pair, self.candleSize, 1))
                bought = self.tradingSession.update(data[0], True)
                print("bought status ->", sold)
                if not bought:    
                    time.sleep(60)


            if (t == 0) and datetime.now().seconds == 0:
                logToSlack(f"[PAPERTRADER] hourly update for {self.pair.value} for strat: {self.stratName} \n {self.getResults()}", channel=Channel.PAPERTRADER)

            if datetime.now().minutes % 5 == 0 and datetime.now().seconds == 0 and currentPrice not None:
                currentpnl = self.tradingSessison.getCurrentPnl(self.currentPrice)
                writer.writeCurrentPnl(currentPnl, self.sessionid)


            if bought:
                time.sleep(5)
                self.currentPrice, _ = getCurrentBinancePrice(self.pair)
                ts = datetime.now()
                print(f"Checking for sell w/ {self.pair} @ {price}")
                dummyCandle = {"close": self.currentPrice, "timestamp": ts}
                print(dummyCandle)
                bought =  self.tradingSession.update(dummyCandle, False)

