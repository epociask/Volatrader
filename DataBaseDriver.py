import time

import schedule
from Enums import *
from DBwriter import DBwriter

writer = DBwriter()

# noinspection PyTypeChecker
indicatorENUMS = [e for e in Indicator]


def writeIndicators(pair: Pair, candeSize: Candle):
    for indicator in indicatorENUMS:
        writer.writeIndicatorForTable(candeSize, pair, True, indicator)


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


def writeSchedule(pair: Pair):
    schedule.every(1).seconds.do(writer.writeCandlesFromCCXT, Candle.ONE_MINUTE, pair, 3)
    schedule.every(1).minutes.do(writer.writeCandlesFromCCXT, Candle.ONE_MINUTE, pair, 3)
    schedule.every(1).minutes.do(writeIndicators, Candle.ONE_MINUTE, pair)
    schedule.every(5).minutes.do(writer.writeCandlesFromCCXT, Candle.FIVE_MINUTE, pair, 2)
    schedule.every(5).minutes.do(writeIndicators, Candle.FIVE_MINUTE, pair)
    schedule.every(15).minutes.do(writer.writeCandlesFromCCXT, Candle.FIFTEEEN_MINUTE, pair, 2)
    schedule.every(15).minutes.do(writeIndicators, Candle.FIFTEEEN_MINUTE, pair)
    schedule.every(30).minutes.do(writer.writeCandlesFromCCXT, Candle.THIRTY_MINUTE, pair, 2)
    schedule.every(30).minutes.do(writeIndicators, Candle.THIRTY_MINUTE, pair)
    schedule.every(1).hour.do(writer.writeCandlesFromCCXT, Candle.HOUR, pair, 2)
    schedule.every(1).hour.do(writeIndicators, Candle.HOUR, pair)

    while True:
        schedule.run_pending()


startCollection(Pair.ETHUSDT)
writeIndicators(Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE)