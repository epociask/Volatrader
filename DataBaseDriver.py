import schedule
from Enums import *
from DBwriter import DBwriter

writer = DBwriter()
# noinspection PyTypeChecker
indicatorENUMS = [e for e in Indicator]

print(indicatorENUMS)
def startCollection(pair: Pair):
    # writer.writeCandlesFromCCXT(Candle.FIFTEEEN_MINUTE, pair)
    # writer.writeCandlesFromCCXT(Candle.THIRTY_MINUTE, pair)
    # writer.writeCandlesFromCCXT(Candle.HOUR, pair)
    # writer.writeCandlesFromCCXT(Candle.FIVE_MINUTE, pair)
    # writer.writeCandlesFromCCXT(Candle.ONE_MINUTE, pair)

    for indicator in indicatorENUMS:
        print(indicator.value)
        writer.writeIndicatorForTable(Candle.FIFTEEEN_MINUTE, pair, True, indicator, 10)
        # writer.writeIndicatorForTable(Candle.THIRTY_MINUTE, pair, True, indicator, 2)
        # writer.writeIndicatorForTable(Candle.HOUR, pair, True, indicator, 2)
        # writer.writeIndicatorForTable(Candle.ONE_MINUTE, pair, True, indicator, 2)


def writeSchedule(pair: Pair):
    schedule.every(1).minute.do(writer.writeCandlesFromCCXT, (Candle.ONE_MINUTE, pair, 2))
    schedule.every(5).minutes.do(writer.writeCandlesFromCCXT, (Candle.FIVE_MINUTE, pair, 2))
    schedule.every(15).minutes.do(writer.writeCandlesFromCCXT, (Candle.FIFTEEEN_MINUTE, pair, 2))
    schedule.every(30).minutes.do(writer.writeCandlesFromCCXT, (Candle.THIRTY_MINUTE, pair, 2))
    schedule.every(1).hour.do(writer.writeCandlesFromCCXT, (Candle.HOUR, pair, 2))


startCollection(Pair.STXUSDT)