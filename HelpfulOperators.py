import datetime
import decimal

'''
    Helper Script w/ utility functions that are referenced throughout master program
'''


def makeEqualities(list):
    s = "WHERE "
    f = " ALTER TABLE mytable "

    for index in range(len(list)):
        if index != 0:
            s += f"{list[0]}.timestamp = {list[index]}.timestamp{list[index][0: list[index].find('_')]} " if index == 1 else f"AND {list[0]}.timestamp = {list[index]}.timestamp{list[index][0: list[index].find('_')]} "
            f += f"DROP COLUMN timestamp{list[index][0: list[index].find('_')]} " if index == 1 else f", DROP COLUMN timestamp{list[index][0: list[index].find('_')]}"
    s += ";"
    f += ";"
    return s, f


# takes a timestamp and returns a timestamp from a previous time reference
# X rewind('2020-02-29 00:15:00', 1, 60) --> '2020-02-28 23:15:00'

def rewind(timeStamp: str, limit: int, timeStep: int):
    return convertNumericTimeToString(
        int(datetime.datetime.timestamp(datetime.datetime.strptime(timeStamp, '%Y-%m-%d %H:%M:%S')) * 1000) - (
                    limit * 6 * timeStep * 10000))


# takes a timestamp and returns a timestamp from a previous time reference
# EX rewind('2020-02-29 00:15:00', 1, 60) --> '2020-02-28 23:15:00'
def rewind(timeStamp: str, limit: int, timeStep: int):
    return convertNumericTimeToString(
        int(datetime.datetime.timestamp(datetime.datetime.strptime(timeStamp, '%Y-%m-%d %H:%M:%S')) * 1000) - (
                limit * 6 * timeStep * 10000))


# converts numeric timestamp type to string
# @returns Exception if error
# @returns string timestamp
def convertNumericTimeToString(numeric: (float, int, str)) -> (str, Exception):
    try:
        date = datetime.datetime.fromtimestamp(numeric / 1e3)

    except Exception as e:
        raise e

    return date.strftime('%Y-%m-%d %H:%M:%S')


# Helper lambda functions

#<<<<<<< HEAD
getLow = lambda ticker: str(ticker).find('.') #used in getLowHighBounds
getHigh = lambda ticker: (len(str(ticker)[str(ticker).find('.'): len(str(ticker))]))  #used in getLowHighBounds
cleanBounds = lambda bounds: bounds.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]", "") #cleans bounds to be parsed easier
cleaner = lambda word: word if type(word) != decimal.Decimal else str(word)
#=======
getLow = lambda ticker: str(ticker).find('.')  # used in getLowHighBounds
getHigh = lambda ticker: (len(str(ticker)[str(ticker).find('.'): len(str(ticker))]))  # used in getLowHighBounds
cleanBounds = lambda bounds: bounds.replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("]",
                                                                                                                "")  # cleans bounds to be parsed easier
#>>>>>>> dfdadf7ad11f96dd442d17433bf86a47e063ddca


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

        it = iter(candle)
        time = next(it)
        open = cleaner(next(it))
        high = cleaner(next(it))
        low = cleaner(next(it))
        close = cleaner(next(it))
        volume = cleaner(next(it))

        try:
            new.append({
                'timestamp': time,
                'open': open,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume,
            })


        except Exception as e:
            print("Error", e)

    return new


# TODO ASSERTION TESTS

print(rewind('2020-02-29 00:15:00', 100, 15))
