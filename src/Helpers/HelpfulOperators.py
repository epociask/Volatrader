import copy
import decimal
import datetime
import time
from unicodedata import numeric
import ccxt
import numpy as np
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
from Helpers.IndicatorConstants import candle
from Helpers.Enums import Indicator, Pair, Candle
import re
import requests 

'''
    Helper Script w/ utility functions that are referenced throughout master program
'''

'''
    Helper Lambda Functions
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

getLow = lambda ticker: str(ticker).find('.')  # used in getLowHighBounds
getHigh = lambda ticker: (len(str(ticker)[str(ticker).find('.'): len(str(ticker))]))  # used in getLowHighBounds
cleaner = lambda word: word if type(word) != decimal.Decimal else str(word)  # cleans bounds to be parsed easier
cleanDate = lambda date: date[0: 10]
getIndicatorName = lambda indicator: Indicator(indicator.value).name
dateFormat = lambda time: str(time) + "T00:00:00Z"
convertToVal = lambda candleEnum: int(candleEnum.value[0: len(candleEnum.value) - 1]) if candleEnum.value[len(candleEnum.value) - 1 : len(candleEnum.value) ] == 'm' else int(candleEnum.value[0: len(candleEnum.value) - 1]) * 60

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
    Helper utility functions     
'''

# common constants

# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------

     #'2017-09-01 00:00:00'

def getFromTime(from_datetime: str, pair: Pair, candleSize: Candle):

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
    hold = 30
    exchange = ccxt.binance()


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

            print(exchange.milliseconds(), 'Fetching candles starting from', exchange.iso8601(from_timestamp))
            ohlcvs = exchange.fetch_ohlcv(pair.value.replace("USD", '/USD'), candleSize.value, from_timestamp)
            print(exchange.milliseconds(), 'Fetched', len(ohlcvs), 'candles')
            first = ohlcvs[0][0]
            last = ohlcvs[-1][0]
            print('First candle epoch', first, exchange.iso8601(first))
            print('Last candle epoch', last, exchange.iso8601(last))
            from_timestamp += len(ohlcvs) * step
            data += ohlcvs

        except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:

            print('Got an error', type(error).__name__, error.args, ', retrying in', hold, 'seconds...')
            time.sleep(hold)

    return data

def rewind(timeStamp: str, limit: int, timeStep: int):
    """
    takes a timestamp and returns a timestamp from a previous time reference
    EXAMPLE rewind('2020-02-29 00:15:00', 1, 60) --> '2020-02-28 23:15:00'
    @param timeStamp = timeStamp string
    @param limit = number of timestamps to count back
    @param timeStep = timeFrame to go back
    """
    return int(datetime.datetime.timestamp(datetime.datetime.strptime(timeStamp, '%Y-%m-%d %H:%M:%S')) * 1000) - (
            limit * 6 * timeStep * 10000)


def convertNumericTimeToString(numeric: (float, int, str)) -> (str, Exception):
    """
    converts numeric timestamp type to string
    @returns Exception if error
    @returns string timestamp
    """

    try:
        date = datetime.datetime.fromtimestamp(numeric / 1e3)

    except Exception as e:
        raise e

    return date.strftime('%Y-%m-%d %H:%M:%S')


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

    return {"candle":{
        'timestamp': time,
        'open': open,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume,
    }
    }


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

    return api.fetchOHLCV(pair.value.replace("USD", "/USD"), candleSize.value, limit=limit)


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
        l['candle'] = candle
        ret.append(l)


    return ret


from Helpers.Enums import  Pair


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



