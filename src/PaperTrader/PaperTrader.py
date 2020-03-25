from Helpers.Session import Session
from Helpers.Enums import Pair, Candle, SessionType
from DB.DBReader import DBReader
from Strategies import strategies
import schedule
from Helpers.authent import getCurrentPrice

convertToVal = lambda candleEnum: candleEnum.value[0: len(candleEnum.value) - 2]
reader = DBReader()


class PaperTrader:

    def __init__(self):
        self.takeProfitPercent = None
        self.strategy = None
        self.tradingSession = None

    def paperTrade(self, pair: Pair, candleSize: Candle, strategy, stopLossPercent: int, takeProfitPercent: int,
                   principle: int):
        self.pair = pair
        self.candleSize = candleSize
        self.takeProfitPercent = f"0{takeProfitPercent}" if takeProfitPercent - 10 <= 0 else f"{takeProfitPercent}"
        self.stratName = strategy
        self.strategy, indicators = strategies.getStrat(strategy)
        self.tradingSession = Session(pair, strategy, takeProfitPercent, stopLossPercent, self.stratName,
                                      SessionType.PAPERTRADE)
        self.start()

    def start(self):
        while True:
            data = reader.getCandleDataDescFromDB(self.candleSize, self.pair, 1)
            self.tradingSession.update()

    paperTrade(Pair.ETHUSDT, Candle.FIVE_MINUTE, "TEST_BUY_STRAT", 1, 2, 1000)
