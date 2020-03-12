import schedule
from Helpers.Enums import *
from DB.DBwriter import DBwriter
from Helpers.Logger import logToSlack

writer = DBwriter()

# noinspection PyTypeChecker
indicatorENUMS = [e for e in Indicator]


def writeIndicators(pair: Pair, candleSize: Candle, limit=None):
    for indicator in indicatorENUMS:
        if limit is None:
            writer.writeIndicatorForTable(candleSize, pair, True, indicator)
        else:
            writer.writeIndicatorForTable(candleSize, pair, True, indicator, limit)


def startCollection(pair: Pair):
    writer.writeCandlesFromCCXT(Candle.FIVE_MINUTE, pair, True)
    writer.writeCandlesFromCCXT(Candle.FIFTEEEN_MINUTE, pair, True)
    writer.writeCandlesFromCCXT(Candle.THIRTY_MINUTE, pair, True)
    writeIndicators(pair, Candle.FIVE_MINUTE)
    writeIndicators(pair, Candle.FIFTEEEN_MINUTE)
    writeIndicators(pair, Candle.THIRTY_MINUTE)


def writeSchedule(pair: Pair):
    schedule.every(5).minutes.do(writer.writeCandlesFromCCXT, Candle.FIVE_MINUTE, pair, True, 4)
    schedule.every(5).minutes.do(writeIndicators, pair, Candle.FIVE_MINUTE, limit=2)
    schedule.every(15).minutes.do(writer.writeCandlesFromCCXT, Candle.FIFTEEEN_MINUTE, pair, True, 4)
    schedule.every(15).minutes.do(writeIndicators, pair, Candle.FIFTEEEN_MINUTE, limit=2)
    schedule.every(30).minutes.do(writer.writeCandlesFromCCXT, Candle.THIRTY_MINUTE, pair, True, 4)
    schedule.every(30).minutes.do(writeIndicators, pair, Candle.THIRTY_MINUTE, limit=2)

    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            logToSlack(f"DATABASE BREAKING ERROR :: \n{e}", tagChannel=True)
            pass


startCollection(Pair.ETHUSDT)
writeSchedule(Pair.ETHUSDT)
