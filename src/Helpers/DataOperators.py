import copy
import decimal
import datetime
import time
from unicodedata import numeric
import ccxt
import numpy as np
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
from Helpers.Constants.Enums import Indicator, Pair, Candle, SessionType
import re   
import requests 
from colorama import init
from termcolor import cprint 
from pyfiglet import figlet_format
from termcolor import colored

'''
    Helper Script w/ utility functions that are referenced throughout master program
'''
# common constants

# -----------------------------------------------------------------------------
cleaner = lambda word: word if type(word) != decimal.Decimal else str(word)  # cleans bounds to be parsed easier


# -----------------------------------------------------------------------------

     #'2017-09-01 00:00:00'

def getCandlesFromTime(from_datetime: str, pair: Pair, candleSize: Candle, market):
    from_datetime = from_datetime[0 : 10] + " 00:00:00"
    print("------------------>", from_datetime)

        # function to get unique values 
    def unique(list1): 
        
        # insert the list to the set 
        list_set = set(list1) 
        # convert the set to the list 
        unique_list = (list(list_set)) 
        
        return unique_list
    msec = 1000
    minute = 60 * msec
    fifteen_minute = minute * 15
    five_minute = minute * 5
    thirty_minute = minute * 30
    hour = minute * 60 
    hold = 30
    exchange = market.value
    if candleSize.value == "1h":
        step = hour

    if candleSize.value == "15m":
        step = fifteen_minute

    elif candleSize.value == "5m":
        step = five_minute

    else:
        step = thirty_minute
    # -----------------------------------------------------------------------------
    from_timestamp = exchange.parse8601(from_datetime)

    # -----------------------------------------------------------------------------

    now = exchange.milliseconds()

    # -----------------------------------------------------------------------------

    data = []

    while from_timestamp < now:

        try:
         
            print(exchange.milliseconds(), colored('Fetching candles starting from', color="grey"), exchange.iso8601(from_timestamp))
            ohlcvs = exchange.fetch_ohlcv(pair.value.replace("USDT", '/USDT'), candleSize.value, from_timestamp)
            print(exchange.milliseconds(), 'Fetched', len(ohlcvs), 'candles')
            first = ohlcvs[0][0]
            last = ohlcvs[-1][0]
            if first == last:
                return data
            print(colored('First candle epoch', color='grey'), first, exchange.iso8601(first))
            print(colored('Last candle epoch', color='grey'), last, exchange.iso8601(last))
            from_timestamp += len(ohlcvs) * step
            data += ohlcvs

        except(ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:

            print('Got an error', type(error).__name__, error.args, ', retrying in', hold, 'seconds...')
            time.sleep(hold)

        # finally:
        #     data += fetchCandleData(exchange, pair, candleSize)
    return data



def convertCandlesToDict(candles: list) -> str:
    """
    converts list candle data to list of dictionary
    ..... ie: list ==> list[dict{}]
    @:param candles = list of candles
    @:returns dictionary of candles
    """
    assert type(candles) == list
    new = []
    for candle in candles:
        try:
            new.append(cleanCandle(candle))

        except Exception as e:
            print("Error", e)

    return new


def cleanCandle(candle: dict) -> dict:
    """
    Cleans candle OHLCV values to only extrapolate numeric values
    @:param candle = candle dictionary ex = {'timestamp': 3982435, 'open': '.235', high: '.325', low: '.20', close: '2.7', volume: '69'}
    @:returns cleaned candle
    """

    it = iter(candle)
    time = int(next(it))
    open = cleaner(next(it))
    high = cleaner(next(it))
    low = cleaner(next(it))
    close = cleaner(next(it))
    volume = cleaner(next(it))

    return {
        'timestamp': time,
        'open': open,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume,
    }
    


import random

def printLogo(type: SessionType=None):
    colors = [ 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'grey']

    fonts = ['speed', 'starwars', "stampatello"]

    font = random.choice(fonts)
    text_color = random.choice(colors).lower()
    highlight = f'on_{random.choice(colors)}'.lower()

    init(strip=not sys.stdout.isatty()) 
    cprint(figlet_format('VolaTrade', font=font),
       text_color, None, attrs=['blink'])
    time.sleep(1)

    if type is SessionType.BACKTEST:
        cprint(figlet_format('[BACKTEST]', font=font),
    text_color, None, attrs=['blink'])

    if type is SessionType.PAPERTRADE:
        cprint(figlet_format('[PAPERTRADE]', font=font),
        text_color, None, attrs=['blink'])

    if type is SessionType.LIVETRADE:
        cprint(figlet_format('[VOLATRADER]', font=font),
        text_color, None, attrs=['blink']) 

    if type is None:
        cprint(figlet_format('[NOTIFICATIONS]', font=font),
        text_color, None, attrs=['blink']) 

def fetchCandleData(api: ccxt.Exchange, pair: Pair, candleSize: Candle, limit=500):
    """
    @:returns candles fetched from an exchange
    @:param api = CCXT API instance
    @:param pair = Pair enum
    @:param candleSize = Candle enum
    @:param args --> can either be None type, integer, or string
                --> None type == default limit of past 500 candles
                --> integer type == limit number of recent candles to fetch
                --> string type == Timestamp to collect candles from
    """

    return api.fetchOHLCV(pair.value.replace("USDT", "/USDT"), candleSize.value, limit=limit)


def cleanCandlesWithIndicators(data: list) -> list:
    """

    :param data: data that's to be reformatted
    :param indicators: indicators that are used in data
    :return: clean/reformatted data that can easily be accessible
    """
    ret = []
    for i in data:
        it = iter(i)
        candle = {}

        candle['timestamp'] = int(next(it).strftime("%Y%m%d%H%M"))
        candle['open'] = str(next(it))
        candle['high'] = str(next(it))
        candle['low'] = str(next(it))
        candle['close'] = str(next(it))
        candle['volume'] = str(next(it))
        l = (next(it))
        ret.append(l)


    return ret

