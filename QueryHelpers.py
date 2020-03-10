from Enums import *

'''
Helper script to functionalize query generation
'''
clean3 = lambda val: val if val.find("3") == -1 else val.replace("3", "three")
clean2 = lambda val: val if val.find('2') == -1 else val.replace("2", "two")
clean100 = lambda val: val if val.find('100') == -1 else val.replace("2", "hundred")
getIndicatorName = lambda indicator: Indicator(indicator.value).name.lower()  # Gets indicator key from enum



def getCreateIndicatorTableQuery(candleSize: Candle, pair: Pair, indicator: Indicator, indicatorVal: dict) -> str:
    """
    1
    @:param candleSize = Candle enum
    @:param pair = Pair enum
    @:param Indicator = Indicator enum
    @:param indicatorVal = dictionary of indicator values
    @:returns query that creates indicator table
    @:rtype str
    """
    delimeter = " VARCHAR, "
    keys = f"(timestamp{clean100(clean3(clean2(indicator.value)))} timestamp PRIMARY KEY NOT NULL, " + \
           (delimeter.join(indicatorVal.keys())
            if list(indicatorVal.keys())[0] != "value"
            else f" {clean100(clean3(clean2(indicator.value)))}value") + f" VARCHAR, FOREIGN KEY(timestamp{clean100(clean3(clean2(indicator.value)))}) REFERENCES {pair.value}_OHLCV_{candleSize.value}(timestamp))"
    return f"CREATE TABLE {clean100(clean3(clean2(indicator.value)))}_{pair.value}_{candleSize.value} {keys};"


def getInsertIndicatorsQueryString(indicator: Indicator, indicatorValues: list, timeStamp: str, candleSize: Candle,
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

    l = []
    delimiter = ", "
    for ind in indicatorValues.values():
        l.append(str(ind))

    values = f"('{timeStamp}', 'none')" if 'None' in l else f"('{timeStamp}', {delimiter.join(l)})"

    keys = (f"(timestamp{getIndicatorName(indicator)}, " + (delimiter.join(indicatorValues.keys())) if
            list(indicatorValues.keys())[0] != "value" else f"(timestamp{getIndicatorName(indicator)}," +
                                                            f" {getIndicatorName(indicator)}value") + ")"
    return f'INSERT INTO {getIndicatorName(indicator)}_{pair.value.replace("/", "")}_{candleSize.value} {keys} VALUES {values};'


def getCreateIndicatorTableQuery(candleSize: Candle, pair: Pair, indicator: Indicator, indicatorVal: dict) -> str:
    delimeter = " VARCHAR, "
    indicatorName = getIndicatorName(indicator)
    keys = f"(timestamp{indicatorName} timestamp PRIMARY KEY NOT NULL, " + \
           (delimeter.join(indicatorVal.keys())
            if list(indicatorVal.keys())[0] != "value"
            else f" {indicatorName}value") + f" VARCHAR, FOREIGN KEY(timestamp{indicatorName}) REFERENCES {pair.value}_OHLCV_{candleSize.value}(timestamp))"
    return f"CREATE TABLE {indicatorName}_{pair.value}_{candleSize.value} {keys};"

'''

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
    query = f"SELECT * FROM {pair.value}_OHLCV_{candleSize.value} ORDER BY timestamp DESC"
    return query + ';' if limit is None else query + f" LIMIT {limit};"


'''
7
'''


def getIndicatorDataQuery(pair, candleSize, indicator, limit):
    return f"SELECT * FROM {indicator.value}_{pair.value.replace('/', '')}_{candleSize.value} ORDER BY timestamp " \
           f"DESC LIMIT {limit};"


'''
8
'''


def getWhereEqualsQuery(lst):
    s = "WHERE "
    f = " ALTER TABLE mytable "

    for index in range(len(lst)):
        if index != 0:
            s += f"{lst[0]}.timestamp = {lst[index]}.timestamp{lst[index][0: lst[index].find('_')]} " if index == 1 else f"AND {lst[0]}.timestamp = {lst[index]}.timestamp{lst[index][0: lst[index].find('_')]} "
            f += f"DROP COLUMN timestamp{lst[index][0: lst[index].find('_')]} " if index == 1 else f", DROP COLUMN timestamp{lst[index][0: lst[index].find('_')]}"
    s += ";"
    f += ";"
    return s, f
