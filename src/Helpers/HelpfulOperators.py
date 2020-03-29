import copy
import decimal
import datetime
import ccxt
from Helpers.IndicatorConstants import candle
from Helpers.Enums import Indicator, Pair, Candle

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


def getLowHighBounds(candles: list) -> (int, int):
    """
    @returns low,high integer bounds of candleset to effectively format decimal size for CREATE TABLE query
    @param candles = list of candles
    """

    lows = []
    highs = []

    for candle in candles:
        for key in candle:
            if key is not 'timestamp' and key is not 'volume':
                lows.append(getLow(candle[key]))
                highs.append(getHigh(candle[key]))

    low = max(set(lows), key=lows.count)
    high = max(set(highs), key=highs.count) - 1

    return low, high


def convertCandlesToDict(candles: list) -> list:
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
    time = str(next(it))
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


def fetchCandleData(api: ccxt.Exchange, pair: Pair, candleSize: Candle, args: (int, None)):
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

    arg = args[0]
    if type(arg) == int:
        candles = api.fetchOHLCV(pair.value.replace("USDT", "/USDT"), candleSize.value, limit=args[0])

    else:
        candle = api.parse8601(dateFormat(arg))
        candles = api.fetchOHLCV(pair.value.replace("USDT", "/USDT"), candleSize.value, candle)
    return candles


def cleanCandlesWithIndicators(data: list, indicators: list) -> list:
    """

    :param data: data that's to be reformatted
    :param indicators: indicators that are used in data
    :return: clean/reformatted data that can easily be accessible
    """


    returnList = []
    for row in data:
        rowDict = {}
        rowDict.update({"candle": candle.copy()})
        # print(temp)
        it = iter(row)
        rowDict['candle']['open'] = str(next(it))
        rowDict['candle']['high'] = str(next(it))
        rowDict['candle']['low'] = str(next(it))
        rowDict['candle']['close'] = str(next(it))
        rowDict['candle']['volume'] = str(next(it))
        indicators1 = indicators.copy()
        for indicator in indicators1:
            rowDict.update(copy.deepcopy(indicator))
            for key in indicator:
                for val in indicator.values():
                    for i in val:
                        rowDict[key][i] = str(next(it))

        rowDict['candle']['timestamp'] = str(next(it))

        returnList.append(rowDict.copy())
    return returnList

#
# ts = 25
# while True:
#         print(str(datetime.now()))
#         print(fetchCandleData(ccxt.binance(), Pair.ETHUSDT, Candle.FIVE_MINUTE, [1]))
#




