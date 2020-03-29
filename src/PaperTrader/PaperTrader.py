import time
from datetime import datetime
from Helpers.Logger import logToSlack
from Helpers.Session import Session
from Helpers.Logger import Channel
from Helpers.Enums import Pair, Candle, SessionType
from DB.DBReader import DBReader
from Strategies import strategies


convertToVal = lambda candleEnum: candleEnum.value[0: len(candleEnum.value) - 2]


class PaperTrader:

    def __init__(self, timeStep):
        self.takeProfitPercent = None
        self.strategy = None
        self.tradingSession = None
        self.reader = DBReader()
        self.timeStep = timeStep

    def trade(self, pair: Pair, candleSize: Candle, strategy: str, stopLossPercent: int, takeProfitPercent: int,
              principle: int):
        self.pair = pair
        self.candleSize = candleSize
        self.takeProfitPercent = f"0{takeProfitPercent}" if takeProfitPercent - 10 <= 0 else f"{takeProfitPercent}"
        self.stratName = strategy
        self.strategy, self.indicators = strategies.getStrat(self.stratName)
        print(strategy)
        self.stopLossPercent = stopLossPercent
        self.tradingSession = Session(pair, self.strategy, self.candleSize, takeProfitPercent, self.stopLossPercent, self.stratName,
                                      SessionType.PAPERTRADE)
        self.principle = principle
        self.start()

    def start(self):
        logToSlack(f"Starting Paper Trader for {self.pair.value}/{self.candleSize.value} \nstrat: {self.stratName} takeprofit: %{int(self.takeProfitPercent)} stoploss: %{self.stopLossPercent}")
        while True:
            t = int(str(datetime.now())[14:16])
            if t % self.timeStep == 0 or t == 0:
                time.sleep(60)
                temp = True
                while temp:
                    availableYet = self.reader.fetchRowFromSharedTable(self.pair, self.candleSize)
                    print(availableYet)
                    if availableYet == "True":
                        logToSlack(f"data now available in DB to {self.pair.value}/{self.candleSize.value}[{self.stratName}] to make calculation")
                        data = self.reader.fetchCandlesWithIndicators(self.pair, self.candleSize, self.indicators, 1)
                        self.tradingSession.update(data[0])
                        temp = False

                    else:
                        time.sleep(5)
