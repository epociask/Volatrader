from BackTesterSession import Session
from Enums import Pair,Candle
from DBReader import DBReader
import strategies
import schedule

def executeLogic(sess: Session, candleSize: Candle):
    schedule.every(sess)

def PaperTrader(pair: Pair, candleSize: Candle, strategy, stopLossPercent: int, takeProfitPercent: int, principle: int):
    reader = DBReader()
    takeProfitPercent = f"0{takeProfitPercent}" if takeProfitPercent - 10 <= 0 else f"{takeProfitPercent}"

    strategy, indicators = strategies.getStrat(strategy)
    test = Session(pair, strategy, takeProfitPercent, stopLossPercent)
    while True:
        data = reader.fetchCandlesWithIndicators(pair, candleSize, indicators, 1)
        test.update(data)

