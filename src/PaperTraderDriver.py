from PaperTrader.PaperTrader import PaperTrader
from Helpers.Constants.Enums import *

paper_trader = PaperTrader()
paper_trader.trade(Pair.ETHUSDT, Candle.FIVE_MINUTE, "TEST_STRAT", 1, 1, 1000)
