import ccxt
from DB import DBoperations
import os
from Helpers.Enums import Pair, Candle

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