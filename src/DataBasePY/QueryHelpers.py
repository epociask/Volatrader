"""
Helper script to functionalize query generation
"""
from Helpers.Constants.Enums import *

clean3 = lambda val: val if val.find("3") == -1 else val.replace("3", "three")
clean2 = lambda val: val if val.find('2') == -1 else val.replace("2", "two")
clean100 = lambda val: val if val.find('100') == -1 else val.replace("2", "hundred")
getIndicatorName = lambda indicator: Indicator(indicator.value).name.lower()  # Gets indicator key from enum


def getCandlesWithIndicatorsFromDBQuery(pair: Pair, candleSize: Candle, limit: (int, None)):
    """
    Gets OHLCV candle data from database
    :param pair: Pair enum
    :param candleSize: Candle enum
    :param limit: either None or integer --> specifies amount of rows to return if not none
    :return: str
    """
    return f"SELECT * FROM {pair.value}_OHLCV_{candleSize.value} ORDER BY TIMESTAMP DESC " + (
        ";" if limit is None else f"LIMIT {limit};")


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
