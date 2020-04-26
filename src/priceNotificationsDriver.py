from datetime import datetime
from threading import Thread
from Helpers.API.CMC_api import getTopPercentChange, getTopVolumeCoins
from Helpers.Constants.Enums import Pair
from Helpers.Logger import logToSlack, Channel, MessageType
from SlackNotifier.PriceNotifications import sendAbnormalVolumeNotification
from queue import Queue
import nest_asyncio
import threading
import time
from Helpers.DataOperators import printLogo
nest_asyncio.apply()


que = []

def updateQue(l: list):
    global que 
    que = []
    for coin in l:
        que.append(Thread(target=sendAbnormalVolumeNotification, args=(coin,)))

    for thread in que:
        print("starting for thread ", thread.getName())
        thread.start()
if __name__ == '__main__':

    printLogo(None)
    hasRun = False
    try:
        while True:
            t = int(str(datetime.now())[14:16])
            if not hasRun or t == 0:
                hasRun = True 
                movers = getTopPercentChange("1h", 20, 10000)
                logToSlack(f"Hourly Top price movers:\n {movers}", channel=Channel.VOLATRADER)
                updateQue(getTopVolumeCoins(12))
                time.sleep(60)


    except Exception as e:
        logToSlack(e, messageType=MessageType.ERROR)

            
