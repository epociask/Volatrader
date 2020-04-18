import argparse
import sys, os
from PaperTrader.PaperTrader import PaperTrader
from Helpers.Constants.Enums import *
from Helpers.Logger import logToSlack
from DataBasePY.DBwriter import DBwriter
from datetime import datetime

def main(args):
	paper_trader = PaperTrader()
	writer = DBwriter()

	try:
		paper_trader.trade(args.pair, args.candlesize, args.strategy, args.stoploss, args.takeprofit, args.principle, Time[args.time].value)

	except Exception as e:
		raise e
		logToSlack(e)

	except KeyboardInterrupt:
		writer.writePaperTradeEnd(paper_trader.sessionid)
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

if __name__ == '__main__':
	ap = argparse.ArgumentParser()

	ap.add_argument('--pair', '-p', required=True, type=Pair,
	                help="The pair to simulate strategy on. Must be of type Pair")
	ap.add_argument('--candlesize', '-c', required=True, type=Candle,
	                help="Candle size to use for strategy simulation. Must be of type Candle")
	ap.add_argument('--strategy', '-s', required=True, type=str,
	                help="Strategy to trade with. Strategy must exist in src/Strategies/strategies.py")
	ap.add_argument('--stoploss', '-sl', required=True, type=int,
	                help="Desired trailing stop loss percentage.")
	ap.add_argument('--takeprofit', '-tp', required=True, type=int,
	                help="Desired take profit percentage.")
	ap.add_argument('--principle', '-pr', required=True, type=int,
	                help="Desired base principle investment to run strategy with")
	ap.add_argument('--time', '-t', required=True, type=str,
	                help="How long to run paper trader for")

	args = ap.parse_args()

	main(args)
