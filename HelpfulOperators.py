import datetime
import decimal

import ccxt

from Enums import Indicator, Pair, Candle

'''
    Helper Script w/ utility functions that are referenced throughout master program
'''

# Helper Lambda Functions
getLow = lambda ticker: str(ticker).find('.')  # used in getLowHighBounds
getHigh = lambda ticker: (len(str(ticker)[str(ticker).find('.'): len(str(ticker))]))  # used in getLowHighBounds
cleanBounds = lambda bounds: bounds.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]",
                                                                                                                "")  # cleans bounds to be parsed easier
cleaner = lambda word: word if type(word) != decimal.Decimal else str(word)  # cleans bounds to be parsed easier
getIndicatorName = lambda indicator: Indicator(indicator.value).name
dateFormat = lambda time: str(time) + "T00:00:00Z"


def makeEqualities(lst):
    s = "WHERE "
    f = " ALTER TABLE mytable "

    for index in range(len(lst)):
        if index != 0:
            s += f"{lst[0]}.timestamp = {lst[index]}.timestamp{lst[index][0: lst[index].find('_')]} " if index == 1 else f"AND {lst[0]}.timestamp = {lst[index]}.timestamp{lst[index][0: lst[index].find('_')]} "
            f += f"DROP COLUMN timestamp{lst[index][0: lst[index].find('_')]} " if index == 1 else f", DROP COLUMN timestamp{lst[index][0: lst[index].find('_')]}"
    s += ";"
    f += ";"
    return s, f


# takes a timestamp and returns a timestamp from a previous time reference
# X rewind('2020-02-29 00:15:00', 1, 60) --> '2020-02-28 23:15:00'

def rewind(timeStamp: str, limit: int, timeStep: int):
    return int(datetime.datetime.timestamp(datetime.datetime.strptime(timeStamp, '%Y-%m-%d %H:%M:%S')) * 1000) - (
            limit * 6 * timeStep * 10000)


# converts numeric timestamp type to string
# @returns Exception if error
# @returns string timestamp
# def convertNumericTimeToString(numeric: (float, int, str)) -> (str, Exception):
#     try:
#         date = datetime.datetime.fromtimestamp(numeric / 1e3)
#
#     except Exception as e:
#         raise e
#
#     return date.strftime('%Y-%m-%d %H:%M:%S')


# TODO FUNCTION IS PROBABLY UNECESSARY.. TEST TO MAKE SURE

def cleanCandle(candle, high):
    for key in candle:
        print(len(str((candle[key]))))
        if len(str((candle[key]))) < high:
            candle[key] = str(candle[key]) + "0"

    print(candle)
    return candle


# returns low high bounds of candleset to effectively format decimal size for CREATE TABLE query
def getLowHighBounds(candles: list) -> (int, int):
    lows = []
    highs = []

    for candle in candles:
        for key in candle:
            if key is not 'timestamp' and key is not 'volume':
                lows.append(getLow(candle[key]))
                highs.append(getHigh(candle[key]))

    low = max(set(lows), key=lows.count)
    high = max(set(highs), key=highs.count) - 1

    print(low)
    print(high)
    return low, high


# converts list candle data to list of dictionary..... ie list[dict{}]
def convertCandlesToDict(candles: list):
    assert type(candles) == list
    new = []
    for candle in candles:
        try:
            new.append(cleanCandle(candle))


        except Exception as e:
            print("Error", e)

    print(new)
    return new


def cleanCandle(candle):
    it = iter(candle)
    time = str(next(it))
    print(time)
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


# TODO MAKE ADD HELPER CLEANING FUNCTION FOR PASSING PAIR ENUM TO FETCHOHLCV
# Returns candles fetched from an exchange
def fetchCandleData(api: ccxt.Exchange, pair: Pair, candleSize: Candle, args: (int, None)):
    arg = args[0]
    if type(arg) == int:
        candles = api.fetchOHLCV(pair.value.replace("USDT", "/USDT"), candleSize.value, limit=args[0])

    else:
        candle = api.parse8601(dateFormat(arg))
        candles = api.fetchOHLCV(pair.value.replace("USDT", "/USDT"), candleSize.value, candle)
    return candles
