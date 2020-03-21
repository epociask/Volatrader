import schedule
from Helpers.Enums import *
from DB.DBwriter import DBwriter
from Helpers.Logger import logToSlack
from datetime import datetime
writer = DBwriter()

"""
noinspection PyTypeChecker
"""
indicatorENUMS = [e for e in Indicator]


def writeIndicators(pair: Pair, candleSize: Candle, limit=None) -> None:
    """
    Calculates & writes indicator data to DataBase
    :param pair: Pair enum
    :param candleSize: Candle enum
    :param limit: limit on how many rows to write for specific indicator
    :returns: Nothing
    """

    ts = datetime.now()
    for indicator in indicatorENUMS:
        if limit is None:
            writer.writeIndicatorForTable(candleSize, pair, True, indicator)
        else:
            writer.writeIndicatorForTable(candleSize, pair, True, indicator, limit)

    logToSlack(f"[WRITE INDICATORS TIME] {datetime.now()-ts}")


def startCollection(pair: Pair, date=None) -> None:
    """
    starts data collection by writing 500 most recent candles & writing indicator values
    :param pair: Pair enum
    :returns: Nothing
    """
    if date is None:
        writer.writeCandlesFromCCXT(Candle.FIVE_MINUTE, pair, True)
        writer.writeCandlesFromCCXT(Candle.FIFTEEEN_MINUTE, pair, True)

    else:
        writer.writeCandlesFromCCXT(Candle.FIVE_MINUTE, pair, date)
        writer.writeCandlesFromCCXT(Candle.FIFTEEEN_MINUTE, pair, date)
    writeIndicators(pair, Candle.FIVE_MINUTE)
    writeIndicators(pair, Candle.FIFTEEEN_MINUTE)


def writeSchedule(pair: Pair) -> None:
    """
    Schedule to write candle & indicator data
    :param pair: Pair enum
    :returns: Nothing
    """
    schedule.every(5).minutes.do(writer.writeCandlesFromCCXT, Candle.FIVE_MINUTE, pair, True, 4)
    schedule.every(5).minutes.do(writeIndicators, pair, Candle.FIVE_MINUTE, limit=2)
    schedule.every(15).minutes.do(writer.writeCandlesFromCCXT, Candle.FIFTEEEN_MINUTE, pair, True, 4)
    schedule.every(15).minutes.do(writeIndicators, pair, Candle.FIFTEEEN_MINUTE, limit=2)

    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            logToSlack(f"DATABASE BREAKING ERROR :: \n{e}", tagChannel=True)
            writeSchedule(pair)


writeIndicators(Pair.ETHUSDT, Candle.FIVE_MINUTE, 2)
