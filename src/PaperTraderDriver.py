from PaperTrader.PaperTrader import PaperTrader
from Helpers.Constants.Enums import *
from Helpers.Logger import logToSlack, Channel

try:
  paper_trader = PaperTrader()
  paper_trader.trade(Pair.ETHUSDT, Candle.FIVE_MINUTE, "TEST_STRAT", 1, 1, 1000)

except Exception as e:
  logToSlack(f"PAPER TRADER ERROR: {e}", channel=Channel.DEBUG, tagChannel=True)