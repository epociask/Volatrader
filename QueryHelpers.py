from Enums import *

clean = lambda val: val if val.find("3") == -1 else val.replace("3", "three")


def getCreateIndicatorTableQuery(candleSize: Candle, pair: Pair, indicator: Indicator, indicatorVal: dict) -> str:
    delimeter = " VARCHAR, "
    keys = f"(timestamp{clean(indicator.value)} VARCHAR PRIMARY KEY NOT NULL, " + \
           (delimeter.join(indicatorVal.keys())
            if list(indicatorVal.keys())[0] != "value"
            else f" {clean(indicator.value)}value") + f" VARCHAR, FOREIGN KEY(timestamp{clean(indicator.value)}) REFERENCES {pair.value.replace('/', '')}_OHLCV_{candleSize.value}(timestamp))"
    return f"CREATE TABLE {indicator.value}_{pair.value}_{candleSize.value} {keys};"


def getInsertIndicatorsQueryString(indicator: Indicator, indicatorValues: list, timeStamp: str, candleSize: Candle, pair: Pair) -> str:
    l = []
    delimiter = ", "
    for ind in indicatorValues.values():
        l.append(str(ind))
    values = f"('{timeStamp}', {delimiter.join(l)} )"
    keys = (f"(timestamp{clean(indicator.value)}, " + (delimiter.join(indicatorValues.keys())) if
            list(indicatorValues.keys())[0] != "value" else f"(timestamp{clean(indicator.value)}," +
                                                            f" {clean(indicator.value)}value") + ")"

    return f'INSERT INTO {clean(indicator.value)}_{pair.value.replace("/", "")}_{candleSize.value} {keys} VALUES {values};'


def getTableDataQuery(candleSize: Candle, pair: Pair, args: list):
    return f"SELECT * FROM {pair.value}_OHLCV_{candleSize.value} ORDER BY timestamp ASC LIMIT {args[0]};"


def getCandleInsertQuery(candle: dict, marketPair: Pair, candleSize: Candle) -> str:
    return f"INSERT INTO {marketPair.value}_OHLCV_{candleSize.value}" \
           f"(timestamp, open, high, low, close, volume) VALUES " \
           f"(to_timestamp({candle['timestamp'] / 1000}), \'{candle['open']}\', \'{candle['high']}\', \'{candle['low']}\', \'{candle['close']}\', \'{candle['volume']}\');"


def getCreateCandleTableQuery(low, high, marketPair: Pair, candleSize: Candle) -> str:
    lowHigh = f'{low}, {high}'

    return f"CREATE TABLE {marketPair.value}_OHLCV_{candleSize.value}(timestamp TIMESTAMP PRIMARY KEY NOT NULL, " \
           f"open DECIMAL({lowHigh}), high  DECIMAL({lowHigh}), low DECIMAL({lowHigh}), " \
           f"close DECIMAL({lowHigh}), volume numeric(10));"


def getCandlesFromDBQuery(pair: Pair, candleSize: Candle, limit):
    query = f"SELECT * FROM {pair.value}_OHLCV_{candleSize.value} ORDER BY timestamp DESC"
    return query + ';' if limit is None else query + f" LIMIT {limit};"

def getIndicatorDataQuery(pair, candleSize, indicator, limit):
    return f"SELECT * FROM {indicator.value}_{pair.value.replace('/','')}_{candleSize.value} ORDER BY timestamp " \
           f"DESC LIMIT {limit};"
