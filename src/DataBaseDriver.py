from Helpers.Enums import *
from DB.DBwriter import DBwriter
from Helpers.Logger import logToSlack
from datetime import datetime
from multiprocessing import Process
import time

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
    logToSlack(f"[STARTING INDICATOR WRITE FOR {pair.value}/{candleSize.value}]")
    ts = datetime.now()
    for indicator in indicatorENUMS:
        if limit is None:
            writer.writeIndicatorForTable(candleSize, pair, True, indicator)
        else:
            writer.writeIndicatorForTable(candleSize, pair, True, indicator, limit)

    logToSlack(f"[INDICATOR WRITE TIME {pair.value}/{candleSize.value}] {datetime.now() - ts}")


def startCollection(pair: Pair, date=None) -> None:
    """
    starts data collection by writing 500 most recent candles & writing indicator values
    :param date:
    :param pair: Pair enum
    :returns: Nothing
    """
    if date is None:
        count5 = writer.writeCandlesFromCCXT(Candle.FIVE_MINUTE, pair, True)
        count15 = writer.writeCandlesFromCCXT(Candle.FIFTEEEN_MINUTE, pair, True)
        count30 = writer.writeCandlesFromCCXT(Candle.THIRTY_MINUTE, pair, True)

    else:
        count5 = writer.writeCandlesFromCCXT(Candle.FIVE_MINUTE, pair, True, date)
        count15 = writer.writeCandlesFromCCXT(Candle.FIFTEEEN_MINUTE, pair, True, date)
        count30 = writer.writeCandlesFromCCXT(Candle.THIRTY_MINUTE, pair, True, date)

    if count5 is not None:
        writeIndicators(pair, Candle.FIVE_MINUTE, count5)

    else:
        writeIndicators(pair, Candle.FIVE_MINUTE)

    if count15 is not None:
        writeIndicators(pair, Candle.FIFTEEEN_MINUTE, count15)

    else:
        writeIndicators(pair, Candle.FIFTEEEN_MINUTE, count15)

    if count30 is not None:
        writeIndicators(pair, Candle.THIRTY_MINUTE, count30)

    else:
        writeIndicators(pair, Candle.THIRTY_MINUTE, count30)


def writeSchedule(pair: Pair, timeStep, candleSize: Candle) -> None:
    """
    Schedule to write candle & indicator data
    :param timeStep:
    :param candleSize:
    :param pair: Pair enum
    :returns: Nothing
    """
    while True:

        try:
            t = int(str(datetime.now())[14:16])
            if t % timeStep == 0 or t == 0:
                time.sleep(10)
                writer.writeCandlesFromCCXT(candleSize, pair, True, 1)
                writeIndicators(pair, candleSize, limit=0)

        except Exception as e:
            logToSlack(f"DATABASE BREAKING ERROR :: \n{e}", tagChannel=True)
            writeSchedule(pair, timeStep, candleSize)


def main():
    """
    Main function for Driver script...
    :returns: Nothing
    """
    p1 = Process(target=writeSchedule, args=(Pair.ETHUSDT, 5, Candle.FIVE_MINUTE,))
    p2 = Process(target=writeSchedule, args=(Pair.ETHUSDT, 15, Candle.FIFTEEEN_MINUTE,))
    p3 = Process(target=writeSchedule, args=(Pair.ETHUSDT, 30, Candle.THIRTY_MINUTE,))

    p1.start()
    p2.start()
    p3.start()



if __name__ == '__main__':
    main()
