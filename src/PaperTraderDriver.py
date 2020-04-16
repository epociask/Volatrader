import argparse
from PaperTrader.PaperTrader import PaperTrader
from Helpers.Constants.Enums import *
from Helpers.Logger import logToSlack


def main(args):
	paper_trader = PaperTrader()

	try:
		paper_trader.trade(args.pair, args.candlesize, args.strategy, args.stoploss, args.takeprofit, args.principle)
  			

	except Exception as e:
		logToSlack(e)


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

	args = ap.parse_args()

	main(args)
