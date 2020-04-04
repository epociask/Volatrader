from threading import Thread

from Helpers.Enums import Pair
from Helpers.PriceNotifications import sendAbnormalVolumeNotification


def startThread(pair: Pair):
    p = Thread(target=sendAbnormalVolumeNotification, args=(pair,), )
    p.start()


if __name__ == '__main__':

    list = [Pair.ETHUSDT, Pair.ATOMBTC, Pair.BTCUSDT, Pair.STXUSDT, Pair.LTCUSDT, Pair.XRPUSDT]

    threadCount = 1
    for pair in list:
        print(f"Starting thread # {threadCount} for {pair.value}")
        startThread(pair)
        threadCount += 1
