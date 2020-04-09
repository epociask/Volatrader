from PaperTrader.PaperTrader import PaperTrader
from Helpers.Enums import *

paper_trader = PaperTrader(15)
paper_trader.trade(Pair.ETHUSD, Candle.FIFTEEEN_MINUTE, "MA_STRATEGY", 1, 2, 1000)
