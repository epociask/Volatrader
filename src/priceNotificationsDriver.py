from datetime import datetime
from threading import Thread
from API.CMC_api import getTopPercentChange, getTopVolumeCoins
from Helpers.Enums import Pair
from Helpers.Logger import logToSlack, Channel
from SlackNotifier.PriceNotifications import sendAbnormalVolumeNotification
from queue import Queue
import nest_asyncio
import threading
nest_asyncio.apply()
hasRun = False


que = []

def updateQue(l: list):
    global  que
    for val in list:
        que.append(Thread(args=sendAbnormalVolumeNotification, args=(val),))
        
    for thread in que:
        thread.start()


if __name__ == '__main__':
    try:
        while True:
            t = int(str(datetime.now())[14:16])
            if not hasRun or t == 0:
                movers = getTopPercentChange("1h", 20, 10000)
                logToSlack(f"Hourly Top price movers:\n {movers}", channel=Channel.VOLATRADER)
                updateQue(getTopVolumeCoins(12))
                time.sleep(60)


    except Exception as e:
        logToSlack(e)

            