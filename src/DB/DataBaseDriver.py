import schedule
from Helpers.Enums import *
from DB.DBwriter import DBwriter
from Helpers.Logger import logToSlack

writer = DBwriter()

# noinspection PyTypeChecker
indicatorENUMS = [e for e in Indicator]


def writeIndicators(pair: Pair, candeSize: Candle):
    for indicator in indicatorENUMS:
        writer.writeIndicatorForTable(candeSize, pair, True, indicator)


def startCollection(pair: Pair):
    writer.writeCandlesFromCCXT(Candle.FIVE_MINUTE, pair, True)
    writer.writeCandlesFromCCXT(Candle.FIFTEEEN_MINUTE, pair, True)
    writer.writeCandlesFromCCXT(Candle.THIRTY_MINUTE, pair, True)
    writeIndicators(pair, Candle.FIVE_MINUTE)
    writeIndicators(pair, Candle.FIFTEEEN_MINUTE)
    writeIndicators(pair, Candle.THIRTY_MINUTE)


def writeSchedule(pair: Pair):
    schedule.every(5).minutes.do(writer.writeCandlesFromCCXT, Candle.FIVE_MINUTE, pair, True, 4)
    schedule.every(5).minutes.do(writeIndicators, pair, Candle.FIVE_MINUTE)
    schedule.every(15).minutes.do(writer.writeCandlesFromCCXT, Candle.FIFTEEEN_MINUTE, pair, True, 4)
    schedule.every(15).minutes.do(writeIndicators, pair, Candle.FIFTEEEN_MINUTE)
    schedule.every(30).minutes.do(writer.writeCandlesFromCCXT, Candle.THIRTY_MINUTE, pair, True, 4)
    schedule.every(30).minutes.do(writeIndicators, pair, Candle.THIRTY_MINUTE)

    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            logToSlack(f"DATABASE BREAKING ERROR :: \n{e}", tagChannel=True)


startCollection(Pair.ETHUSDT)
writeSchedule(Pair.ETHUSDT)
