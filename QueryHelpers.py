from Enums import *

'''
Helper script to functionalize query generation
'''
clean3 = lambda val: val if val.find("3") == -1 else val.replace("3", "three")
clean2 = lambda val: val if val.find('2') == -1 else val.replace("2", "two")
clean100 = lambda val: val if val.find('100') == -1 else val.replace("2", "hundred")
getIndicatorName = lambda indicator: Indicator(indicator.value).name.lower()  # Gets indicator key from enum


def getModifyTableForIndicatorQuery(candleSize: Candle, pair: Pair, indicator: Indicator, indicatorVal: dict) -> str:
    """
    1
    @:param candleSize = Candle enum
    @:param pair = Pair enum
    @:param Indicator = Indicator enum
    @:param indicatorVal = dictionary of indicator values
    @:returns query that creates indicator table
    @:rtype str
    """
    returnString = ""
    for val in indicatorVal:
        temp = f"ALTER TABLE {pair.value}_OHLCV_{candleSize.value} ADD  {clean100(clean3(clean2(indicator.value)))}_{val} VARCHAR; "
        returnString += temp
    return returnString


def getInsertIndicatorsQueryString(indicator: Indicator, indicatorValues: dict, timeStamp: str, candleSize: Candle,
                                   pair: Pair) -> str:
    """
    2
    @:param candleSize = Candle enum
    @:param pair = Pair enum
    @:param Indicator = Indicator enum
    @:param indicatorVal = dictionary of indicator values
    @:returns query that creates indicator table
    @:rtype str
    """
    returnString = f'UPDATE {pair.value}_OHLCV_{candleSize.value} SET'
      # creates appropiate column names
    first = next(iter(indicatorValues))
    returnString += f' {indicator.value}_{first} = \'{indicatorValues[first]}\''

    for value in indicatorValues:
        if value is not first:
            returnString += f', {indicator.value}_{value} = \'{indicatorValues[value]}\''


    returnString += f" WHERE timestamp = '{timeStamp}';"

    return returnString


'''
3
'''


def getTableDataQuery(candleSize: Candle, pair: Pair, args: list):
    return f"SELECT * FROM {pair.value}_OHLCV_{candleSize.value} ORDER BY timestamp ASC LIMIT {str(args[0])};"


'''
4
'''


def getCandleInsertQuery(candle: dict, marketPair: Pair, candleSize: Candle) -> str:
    return f"INSERT INTO {marketPair.value}_OHLCV_{candleSize.value}" \
           f"(timestamp, open, high, low, close, volume) VALUES " \
           f"(to_timestamp({int(candle['timestamp']) / 1000}), \'{candle['open']}\', \'{candle['high']}\', \'{candle['low']}\', \'{candle['close']}\', \'{candle['volume']}\');"


'''
5
'''


def getCreateCandleTableQuery(low, high, marketPair: Pair, candleSize: Candle) -> str:
    lowHigh = f'{low}, {high}'

    return f"CREATE TABLE {marketPair.value}_OHLCV_{candleSize.value}(timestamp TIMESTAMP PRIMARY KEY NOT NULL, " \
           f"open DECIMAL({lowHigh}), high  DECIMAL({lowHigh}), low DECIMAL({lowHigh}), " \
           f"close DECIMAL({lowHigh}), volume numeric(10));"


'''
6
'''


def getCandlesFromDBQuery(pair: Pair, candleSize: Candle, limit):
    query = f"SELECT timestamp, open, high, low, close, volume FROM {pair.value}_OHLCV_{candleSize.value} ORDER BY timestamp DESC"
    return query + ';' if limit is None else query + f" LIMIT {limit};"


def getIndicatorDataWithCandlesQuery(pair: Pair, candleSize: Candle, indicatorList, limit=None):
    select = ""
    notNull = []
    for indicator in indicatorList:
        for key, values in indicator.items():
                for val in values:
                    select += f" {key}_{val},"
                    notNull.append(F"{key}_{val} IS NOT NULL")
    print(notNull)
    end = " AND ".join(e for e in notNull)
    return f"SELECT OPEN, HIGH, LOW, CLOSE, VOLUME, {select} TIMESTAMP FROM {pair.value}_OHLCV_{candleSize.value}  WHERE {end} ORDER BY TIMESTAMP" +  (f" LIMIT {limit} ASC;" if limit is not None else " ASC;")

