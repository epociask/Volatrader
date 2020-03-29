"""
Helper script to functionalize query generation
"""
from Helpers.Enums import *
from Helpers import *

clean3 = lambda val: val if val.find("3") == -1 else val.replace("3", "three")
clean2 = lambda val: val if val.find('2') == -1 else val.replace("2", "two")
clean100 = lambda val: val if val.find('100') == -1 else val.replace("2", "hundred")
getIndicatorName = lambda indicator: Indicator(indicator.value).name.lower()  # Gets indicator key from enum


def getModifyTableForIndicatorQuery(candleSize: Candle, pair: Pair, indicator: Indicator, indicatorVal: dict) -> str:
    """
    Creates and returns query that alters OHLCV table to be compatible w/ specific indicators
    @:param candleSize = Candle enum
    @:param pair = Pair enum
    @:param Indicator = Indicator enum
    @:param indicatorVal = dictionary of indicator values
    @:returns str
    """
    returnString = ""
    for val in indicatorVal:
        temp = f"ALTER TABLE {pair.value}_OHLCV_{candleSize.value} ADD  {clean100(clean3(clean2(indicator.value)))}_{val} VARCHAR; "
        returnString += temp
    return returnString


def getInsertIndicatorsQueryString(indicator: Indicator, indicatorValues: dict, timeStamp: str, candleSize: Candle,
                                   pair: Pair) -> str:
    """
    Creates and returns query that inserts indicators into OHLCV table by timestamp
    @:param candleSize = Candle enum
    @:param pair = Pair enum
    @:param Indicator = Indicator enum
    @:param indicatorVal = dictionary of indicator values
    @:returns query
    """
    returnString = f'UPDATE {clean2(clean3(clean100(pair.value)))}_OHLCV_{candleSize.value} SET'
    # creates appropiate column names
    first = next(iter(indicatorValues))
    returnString += f' {clean2(clean3(clean100(indicator.value)))}_{first} = \'{indicatorValues[first]}\''

    for value in indicatorValues:
        if value is not first:
            returnString += f', {indicator.value}_{value} = \'{indicatorValues[value]}\''

    returnString += f" WHERE timestamp = '{timeStamp}';"

    return returnString


def getTableDataQuery(candleSize: Candle, pair: Pair, args: list) -> str:
    """
    Creates and returns query that
    :param candleSize: Candle enum
    :param pair: Pair enum
    :param args: specifies limit for how many rows to pull out
    :return: str
    """
    return f"SELECT (timestamp, open, high, low, close, volume) FROM {pair.value}_OHLCV_{candleSize.value} ORDER BY timestamp ASC LIMIT {str(args[0])};"


def getCandleInsertQuery(candle: dict, pair: Pair, candleSize: Candle) -> str:
    """
    Creates and returns query that inserts OHLCV candle dictionary into table
    :param candle: dictionary representation of candle
    :param pair: Pair enum
    :param candleSize: Candle enum
    :return: str
    """
    return f"INSERT INTO {pair.value}_OHLCV_{candleSize.value}" \
           f"(timestamp, open, high, low, close, volume) VALUES " \
           f"(to_timestamp({int(candle['timestamp']) / 1000}), \'{candle['open']}\', \'{candle['high']}\', \'{candle['low']}\', \'{candle['close']}\', \'{candle['volume']}\');"


def getCreateCandleTableQuery(low, high, pair: Pair, candleSize: Candle) -> str:
    """
    Creates and returns query that creates OHLCV table
    :param low: low decimal bounds
    :param high: high decimal bounds --> count after 0.
    :param pair: Pair enum
    :param candleSize: Candle enum
    :return: str
    """
    lowHigh = f'{low}, {high}'

    return f"CREATE TABLE {pair.value}_OHLCV_{candleSize.value}(timestamp TIMESTAMP PRIMARY KEY NOT NULL, " \
           f"open DECIMAL({lowHigh}), high  DECIMAL({lowHigh}), low DECIMAL({lowHigh}), " \
           f"close DECIMAL({lowHigh}), volume numeric(10));"


def getCandlesFromDBQuery(pair: Pair, candleSize: Candle, limit: (int, None)):
    """
    Gets OHLCV candle data from database
    :param pair: Pair enum
    :param candleSize: Candle enum
    :param limit: either None or integer --> specifies amount of rows to return if not none
    :return: str
    """
    query = f"SELECT timestamp, open, high, low, close, volume FROM {pair.value}_OHLCV_{candleSize.value} ORDER BY timestamp DESC"
    return query + ';' if limit is None else query + f" LIMIT {limit};"


def getIndicatorDataWithCandlesQuery(pair: Pair, candleSize: Candle, indicatorList, limit=None) -> str:
    """
    returns query string for getting candle data w/ indicator data by timestamp
    :param pair: Pair enum
    :param candleSize: Candle enum
    :param indicatorList: List of indicators from IndicatorConstants.py
    :param limit: specifies how many rows to extrapolate
    :return: query string
    """
    select = ""
    notNull = []
    for indicator in indicatorList:
        for key, values in indicator.items():
            for val in values:
                key = clean100(clean3(clean2(key)))
                select += f" {key}_{val},"
                notNull.append(F"{key}_{val} IS NOT NULL")
    end = " AND ".join(e for e in notNull)
    return f"SELECT OPEN, HIGH, LOW, CLOSE, VOLUME, {select} TIMESTAMP FROM {pair.value}_OHLCV_{candleSize.value}  WHERE {end} ORDER BY TIMESTAMP" + (
        f" DESC LIMIT {limit};" if limit is not None else " DESC;")


# def getInsertBackTestDataQuery(session:, candleSize: Candle, start: str, finish: str):
#     """
#     Creates & returns query that inserts into backtesting table in  DB
#     :param session: finshed instance of Session class
#     :param start: Start timestamp
#     :param finish: Finish timestamp
#     :return:
#     """
#     return f"INSERT INTO BACKTEST_TABLE (PAIR, CANDLESIZE, STRATEGY, POSTIVE_TRADES, NEGATIVE_TRADES, START_TIME, FINISH_TIME, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT, PROFIT_LOSS) " \
#            f"VALUES ({session.pair.value}, {candleSize}, {session.stratString}, {session.positiveTrades}, {session.negativeTrades}, {start}, {finish}, {str(session.getStopLossPercent())}, {str(session.getTakeProfitPercent())}, {session.getTotalPL()});"
#

def getCreateBackTestTableQuery() -> str:
    """
    :return:
    """
    return f"CREATE TABLE BACKTEST_TABLE (pkey UUID NOT NULL DEFAULT uuid_generate_v1(), " \
           f"PAIR VARCHAR, CANDLESIZE VARCHAR, STRATEGY VARCHAR, POSTIVE_TRADES VARCHAR, NEGATIVE_TRADES VARCHAR, START_TIME VARCHAR, FINISH_TIME VARCHAR, " \
           f"STOP_LOSS_PERCENT VARCHAR, TAKE_PROFIT_PERCENT VARCHAR, PROFIT_LOSS VARCHAR " \
           f", CONSTRAINT pkey_tbl PRIMARY KEY ( pkey ));"


#
# def getInsertRowIntoSharedTableQuery(pair: Pair, candleSize: Candle, b: bool):
#     return

def getFetchFromSharedTableQuery(pair: Pair, candleSize: Candle):
    return f"SELECT AVAILABLE FROM SHARED WHERE \'{pair.value}_{candleSize.value}\' = PAIR_CANDLE;"


def getUpdateRowInSharedTableQuery(pair: Pair, candleSize: Candle, available: bool):
    """
    :param pair: Pair enum
    :param candleSize: Candle enum
    :param available: boolean
    :return:
    """
    return f"INSERT INTO SHARED(PAIR_CANDLE, AVAILABLE) VALUES (\'{pair.value}_{candleSize.value}\', {available}) ON CONFLICT(PAIR_CANDLE)" \
           f" DO UPDATE SET AVAILABLE = EXCLUDED.AVAILABLE WHERE EXCLUDED.PAIR_CANDLE = \'{pair.value}_{candleSize.value}\';"