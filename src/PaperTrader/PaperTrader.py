from Helpers.Session import Session
from Helpers.Enums import Pair, Candle, SessionType
from DB.DBReader import DBReader
from Strategies import strategies
import schedule
from Helpers.authent import getCurrentPrice

convertToVal = lambda candleEnum: candleEnum.value[0: len(candleEnum.value) - 2]


class PaperTrader:

    def __init__(self):
        self.takeProfitPercent = None
        self.strategy = None
        self.tradingSession = None
        self.reader = DBReader()

    def trade(self, pair: Pair, candleSize: Candle, strategy: str, stopLossPercent: int, takeProfitPercent: int,
                   principle: int):
        self.pair = pair
        self.candleSize = candleSize
        self.takeProfitPercent = f"0{takeProfitPercent}" if takeProfitPercent - 10 <= 0 else f"{takeProfitPercent}"
        self.stratName = strategy
        self.strategy, self.indicators = strategies.getStrat(self.stratName)
        print(strategy)
        self.tradingSession = Session(pair, self.strategy, takeProfitPercent, stopLossPercent, self.stratName,
                                      SessionType.PAPERTRADE)
        self.principle = principle
        self.start()

    def start(self):
        while True:
            data = self.reader.fetchCandlesWithIndicators(self.pair, self.candleSize, self.indicators, 1)
            self.tradingSession.update(data[0])


paper_trader = PaperTrader()
paper_trader.trade(Pair.ETHUSDT, Candle.FIVE_MINUTE, "SIMPLE_BUY_STRAT", 1, 2, 1000)
