from PaperTrader.PaperTrader import PaperTrader
from Helpers.Enums import *
paper_trader = PaperTrader(5)
paper_trader.trade(Pair.ETHUSDT, Candle.FIVE_MINUTE, "TEST_BUY_STRAT", 1, 2, 1000)