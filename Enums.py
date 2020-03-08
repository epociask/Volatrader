from enum import Enum

class Candle(Enum):
    ONE = "1m"
    FIVE = "5m"
    FIFTEEEN = "15m"
    THIRTY = '30m'
    HOUR = '1h'
    THREEHOUR = "3h"
    TWELVEHOUR = "12h"
    DAY = '1d'
    THREEDAY = '3d'
    WEEK = '1w'
    THREWEEK = "3w"



class Pair(Enum):
    ETHUSDT = "ETHUSDT"
    BTCUSDT = "BTCUSDT"
    STXUSDT = "STXUSDT"
    XRPUSDT = 'XRPUSDT'
    ATOMBTC = "ATOMBTC"
    LTCUSDT = 'LTCUSDT'


class Time(Enum):
    DAY = 24
    ONEWEEK = 168
    TWOWEEK = 336
    THREEWEEK = 504
    MONTH = 700
    TWOMONTH = 1400
    THREEMONTH = 2100