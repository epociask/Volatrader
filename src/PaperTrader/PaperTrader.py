from Helpers.Session import Session
from Helpers.Enums import Pair, Candle
from DB.DBReader import DBReader
from Strategies import strategies
import schedule

convertToVal = lambda candleEnum: candleEnum.value[0: len(candleEnum.value) - 2]
reader = DBReader()


def executeLogic(sess: Session, pair: Pair, candleSize: Candle, indicators: list):
    data = reader.fetchCandlesWithIndicators(pair, candleSize, indicators, 1)
    schedule.every(int(convertToVal(candleSize) / 2)).minutes.do(sess.update, data)

    while True:
        schedule.run_pending()


def paperTrade(pair: Pair, candleSize: Candle, strategy, stopLossPercent: int, takeProfitPercent: int, principle: int):
    takeProfitPercent = f"0{takeProfitPercent}" if takeProfitPercent - 10 <= 0 else f"{takeProfitPercent}"

    strategy, indicators = strategies.getStrat(strategy)
    test = Session(pair, strategy, takeProfitPercent, stopLossPercent)
    executeLogic(test, pair, candleSize, indicators)


#paperTrade(Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, "TEST_BUY_STRAT", 1, 2, 1000)