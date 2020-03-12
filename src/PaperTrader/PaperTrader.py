from BackTest.BackTesterSession import Session
from Helpers.Enums import Pair, Candle
from DB.DBReader import DBReader
from Strategies import strategies
import schedule

convertToVal = lambda candleEnum: candleEnum.value[0 : len(candleEnum.value) - 2]
reader = DBReader()


def executeLogic(sess: Session, candleSize: Candle, indicators: list):
    schedule.every(int(convertToVal(candleSize)/2)).minutes.do(sess.update,)

def PaperTrader(pair: Pair, candleSize: Candle, strategy, stopLossPercent: int, takeProfitPercent: int, principle: int):
    takeProfitPercent = f"0{takeProfitPercent}" if takeProfitPercent - 10 <= 0 else f"{takeProfitPercent}"

    strategy, indicators = strategies.getStrat(strategy)
    test = Session(pair, strategy, takeProfitPercent, stopLossPercent)
    while True:
        data = reader.fetchCandlesWithIndicators(pair, candleSize, indicators, 1)
        test.update(data)


x = [e.value for e in Pair]
print(x)