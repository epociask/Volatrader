import sys, os
from sys import platform
sys.path.append(os.path.dirname(os.getcwd()))
import requests 
from Constants.Enums import Candle 



def getOHLCV(stock: str, candleSize: Candle) -> dict:

    resp = requests.get(f'https://financialmodelingprep.com/api/v3/historical-chart/{candleSize.value}in/{stock}')
    return resp.json()






print(getOHLCV("TSLA", Candle.FIVE_MINUTE))