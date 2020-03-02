import schedule
from DBwriter import writeCandleData, writeIndicatorData
from multiprocessing import Process


#TODO ENSURE TIMESTAMP IS THE SAME FOR ALL INDICATOR VALUES WHEN INSERTING TO ALLOW COHESION AMONGST TABLES


def writeDataSchedule(pair: str):
    print("Starting {} candle schedule thread".format(pair))
    schedule.every(5).minutes.do(writeCandleData, "5m", pair)
    schedule.every(1).minutes.do(writeCandleData, "1m", pair)
    schedule.every(15).minutes.do(writeCandleData, "15m", pair)
    schedule.every(30).minutes.do(writeCandleData, "30m", pair)

    while 1:
        schedule.run_pending()


def writeIndicatorSchedule(pair: str):
    print("Starting {} indicator schedule thread".format(pair))
    writeIndicatorData("5m", pair, "morningdojistar", 100)

    schedule.every(5).minutes.do(writeIndicatorData, "5m", pair, "morningdojistar", 5)

    while 1:
        schedule.run_pending()


writeIndicatorSchedule('ETH/USDT')