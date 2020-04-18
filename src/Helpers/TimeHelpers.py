from sys import platform
import sys
import os 
sys.path.append(os.path.dirname(os.getcwd()))
import datetime 
from Helpers.Constants.Enums import Time 


'''
    Helper Lambda Functions
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
cleanDate = lambda date: date[0: 10]
getIndicatorName = lambda indicator: Indicator(indicator.value).name
dateFormat = lambda time: str(time) + "T00:00:00Z"
convertToVal = lambda candleEnum: int(candleEnum.value[0: len(candleEnum.value) - 1]) if candleEnum.value[len(candleEnum.value) - 1 : len(candleEnum.value) ] == 'm' else int(candleEnum.value[0: len(candleEnum.value) - 1]) * 60

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


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
    if type(numeric) == datetime.datetime:
        return numeric

    try:
        date = datetime.datetime.fromtimestamp(numeric / 1e3)

    except Exception as e:
        raise e

    return date.strftime('%Y-%m-%d %H:%M:%S')


