import schedule
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

    ts = datetime.now()
    for indicator in indicatorENUMS:
        if limit is None:
            writer.writeIndicatorForTable(candleSize, pair, True, indicator)
        else:
            writer.writeIndicatorForTable(candleSize, pair, True, indicator, limit)

    logToSlack(f"[WRITE INDICATORS TIME] {datetime.now() - ts}")


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


def writeSchedule(pair: Pair, timeStep, candleSize: Candle) -> None:
    """
    Schedule to write candle & indicator data
    :param pair: Pair enum
    :returns: Nothing
    """
    schedule.every(timeStep).minutes.do(writer.writeCandlesFromCCXT, candleSize, pair, True, 4)
    schedule.every(timeStep).minutes.do(writeIndicators, pair, candleSize, limit=2)

    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            logToSlack(f"DATABASE BREAKING ERROR :: \n{e}", tagChannel=True)
            writeSchedule(pair)


def main():
    """
    Main function for Driver script...
    :returns: Nothing
    """
    p1 = Process(target=writeSchedule, args=(Pair.ETHUSDT, 5, Candle.FIVE_MINUTE,))
    p2 = Process(target=writeSchedule, args=(Pair.ETHUSDT, 15, Candle.FIFTEEEN_MINUTE,))
    p3 = Process(target=writeSchedule, args=(Pair.ETHUSDT, 30, Candle.THIRTY_MINUTE,))
    time = int(str(datetime.now())[14:16])

    # if time == 0 or time == 30:  # ensure time is either 0th or 30th minute to make calls appropiately w/ candle release times ... ex: 8:00 , 8:30
    p1.start()
    p2.start()
    p3.start()

    # else:
    #     time.sleep(60)
    #     main()


if __name__ == '__main__':
    main()
