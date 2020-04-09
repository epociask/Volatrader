from datetime import datetime
from threading import Thread
from API.CMC_api import getTopPercentChange, getTopVolumeCoins
from Helpers.Enums import Pair
from Helpers.Logger import logToSlack, Channel
from SlackNotifier.PriceNotifications import sendAbnormalVolumeNotification
from queue import Queue
import nest_asyncio
nest_asyncio.apply()
hasRun = False

que = []

def emptyQueue():
    global  que
    for thread in que:
        thread.kill()
    que = []

def startQueue():
    global que
    for thread in que:
        thread.start()

if __name__ == '__main__':
    try:
        while True:
            t = int(str(datetime.now())[14:16])
            if not hasRun or t == 0:
                movers = getTopPercentChange("1h", 20, 10000)
                logToSlack(f"Hourly Top price movers:\n {movers}", channel=Channel.VOLATRADER)

                emptyQueue()
                if not hasRun:
                    hasRun = True
                l = getTopVolumeCoins(12)
                for coin in l:
                    que.append(Thread(target=sendAbnormalVolumeNotification, args=(coin,),))
                
                startQueue()


    except Exception as e:
        logToSlack(e)

