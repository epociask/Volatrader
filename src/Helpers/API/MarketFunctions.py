from Helpers.Constants.Enums import Pair 
import datetime as datetime 
import requests
import time 

def getCurrentBinancePrice(pair: Pair):
    """
    gets and returns current price of binance asset 
    :param pair: Pair enum
    :return: float
    """
    time.sleep(5)
    req = requests.get(f"https://api.binance.com/api/v1/ticker/price?symbol={pair.value}")
    return float(req.json()['price']), datetime.datetime.now()


def getCurrentKrakenPrice(pair: Pair):
    """
    gets and returns the most recent kraken price of a given asset
    """
    args = {
        "pair" : pair.value,
        "count" : 1, 
    }
    req = requests.post("https://api.kraken.com/0/public/Depth", args)
    data = req.json()
    return data['result']['XETHZUSD']['bids'][0][0], data['result']['XETHZUSD']['bids'][0][1]


import ccxt
from DataBasePY import DBoperations
import os
from Helpers.Constants.Enums import Pair, Candle

'''
    Holds public/private key authentification for our api Exchange data
'''

binance = {
    "PUBLIC": os.environ.get('BINANCE_API_KEY'),
    "PRIVATE": os.environ.get('BINANCE_PRIVATE_KEY'),
    "NAME": 'binance'
}

authList = [binance]

#returns a ccxt instance of a connected exchange
def getExchangeInstance(authInfo: dict) -> (ccxt.Exchange, Exception):

    if authInfo['NAME'] == "kraken":
        return ccxt.kraken({
            'apiKey' : authInfo["PUBLIC"],
            'secret' : authInfo["PRIVATE"]
        })

    try:
        exchange_class = getattr(ccxt, authInfo['NAME'])
    except Exception as e:
        print("ERROR Creating  Exchange instance : ", e)
        raise e
    try:
        exchange = exchange_class({
            'apiKey': authInfo["PUBLIC"],
            'secret': authInfo["PRIVATE"],
            'timeout': 30000,
            'enableRateLimit': True,
            'options': {'adjustForTimeDifference': True},
        })

    except Exception as e:
        print("ERROR: ", e)
        raise e

    return exchange


# returns portfolio data
def getPortfolio(exchange: ccxt.Exchange) -> dict:
    assert str(type(exchange)) == "<class \'ccxt.{}.{}\'>".format(str(exchange).lower(), str(
        exchange).lower())  # verifies exchange object is passed through as PARAM properly
    active = {}
    valid = lambda x: bool(x != '0.00000000')

    # Creates dictionary of holdings like {btc: '0.1'}
    active = {entry['asset']:entry['free'] for entry in exchange.fetchBalance()['info']['balances'] if valid(entry['free'])}
    return active


# gets current price of currency from given exchange
def getCurrentPrice(pair: Pair, candleSize: Candle) -> (float, Exception):
    x = DBoperations()
    x.connect()
    try:
        candles = x.getCandleDataFromDB(candleSize.value, pair.value, 1)
        return candles[0]['close']
    except Exception as e:
        raise e



#commmits limit sell order
def sell(pair: str, exch: ccxt.Exchange, porfolio: dict) -> bool:

    assert pair.find("/") != -1 and pair.replace(".", "").isupper()
    print("SELLING ", pair)

    try:
        exch.create_order(
            symbol=pair,
            type='limit',
            side='sell',
            price=getCurrentPrice(pair, exch),
            amount=porfolio[pair[0: pair.find("/")]]
        )

    except Exception as e:
        return False

    return True
