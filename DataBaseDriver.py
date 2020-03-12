import time
import schedule
from Enums import *
from DBwriter import DBwriter

writer = DBwriter()

# noinspection PyTypeChecker
indicatorENUMS = [e for e in Indicator]


def writeIndicators(pair: Pair, candeSize: Candle):
    for indicator in indicatorENUMS:
        writer.writeIndicatorForTable(candeSize, pair, True, indicator, 10)


def startCollection(pair: Pair):
    writer.writeCandlesFromCCXT(Candle.ONE_MINUTE, pair)
    writer.writeCandlesFromCCXT(Candle.FIVE_MINUTE, pair)
    writer.writeCandlesFromCCXT(Candle.FIFTEEEN_MINUTE, pair)
    writer.writeCandlesFromCCXT(Candle.THIRTY_MINUTE, pair)
    writer.writeCandlesFromCCXT(Candle.HOUR, pair)
    writeIndicators(pair, Candle.ONE_MINUTE)
    writeIndicators(pair, Candle.FIVE_MINUTE)
    writeIndicators(pair, Candle.FIFTEEEN_MINUTE)
    writeIndicators(pair, Candle.THIRTY_MINUTE)
    writeIndicators(pair, Candle.HOUR)


def writeSchedule(pair: Pair, candleSize: Candle) -> None:
    schedule.every(1).seconds.do(writer.writeCandlesFromCCXT, candleSize, pair, 3)
    schedule.every(1).minutes.do(writer.writeCandlesFromCCXT, candleSize, pair, 3)

    while True:
        schedule.run_pending()


