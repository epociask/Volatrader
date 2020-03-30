from PaperTrader.PaperTrader import PaperTrader
from Helpers.Enums import *
from Strategies.strategies import STRAT

paper_trader = PaperTrader(5)
paper_trader.trade(Pair.ETHUSDT, Candle.FIVE_MINUTE, STRAT.CANDLESTRAT, 1, 0, 1000)