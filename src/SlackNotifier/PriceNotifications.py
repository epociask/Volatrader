import statistics as stats
import time
from datetime import datetime
from threading import Thread
import ccxt
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
from DB.DBoperations import DBoperations
from Helpers.Enums import Pair, Candle
from Helpers.Logger import logToSlack, Channel, logDebugToFile
from Indicators import IndicatorFunctions
exchange = ccxt.kraken()


# def getAskBidVolume(pair: str):
# 	print(exchange.has['fetchTicker'])
# 	return exchange.fetch_ticker("ETH/USD")['askVolume'], exchange.fetch_ticker("ETH/USD")['bidVolume']



def getVolumeData(pair: str, candleSize: Candle):
	logDebugToFile(f"Getting volume data for {pair} {candleSize}")
	candles = exchange.fetchOHLCV(pair, candleSize.value)
	return [float(e[5]) for e in candles]


def getUpperNormalDistrubtion(pair: Pair, candleSize: Candle, volume=None):

	if volume is None:
		volume = getVolumeData(pair, candleSize)
	stdev = stats.stdev(volume)
	mean = sum(volume)/len(volume)

	return {
		"1SD": mean + stdev,
		"2SD": mean + 2*stdev,
		'3SD': mean + 3*stdev,
		"mean": mean,
		"current_vol": volume[0]
	}


def getUrl(pair: str, candleSize: Candle):
	base_url = "https://trade.kraken.com/markets/kraken/" + pair.lower() + "/" + candleSize.value
	print(base_url)


def crossover(pair, candleSize):
	close = [e[4] for e in exchange.fetch_ohlcv(pair.replace("USD", "/USD"), candleSize, limit=14)]
	sma_5 = IndicatorFunctions.SMA(close, 5)[-1]
	sma_8 = IndicatorFunctions.SMA(close, 8)[-1]
	sma_13 = IndicatorFunctions.SMA(close, 13)[-1]

	string = f'\n SMA_5 {sma_5}  SMA_8 {sma_8}  SMA_13 {sma_13}'

	if sma_5 >= sma_13 and sma_5 >= sma_8:
		return "STRONG BUY" + string
	elif sma_13 <= sma_5 and sma_13 <= sma_8:
		return "HOLD" + string
	elif sma_5 <= sma_8:
		return "SOFT SELL" + string
	elif sma_5 <= sma_13 and sma_5 <= sma_8:
		return "STRONG SELL" + string 
	else:
  		return "No Signal"





def sendAbnormalVolumeNotification(pair: Pair):

	global exchange
	createMessage = lambda pair, devs, candleSize: f"[VOLATILITY ALERT] CURRENT {pair} VOLUME ABOVE {devs} STANDARD DEVIATIONS FOR {candleSize.value} CANDLE"
	tickerMessage = lambda pair, devs, askbid: f"[VOLATILITY ALERT] CURRENT {pair} VOLUME ABOVE {devs} STANDARD DEVIATIONS FOR {askbid} VOLUME"
	# ask, bid = getAskBidVolume(pair)
	# print("askval", ask, "bidval", bid)
	getUrl(pair, Candle.FIFTEEEN_MINUTE)
	isCorrectTime = lambda t,val : t % val == 0 or t == 0
	while True:
		stdDict_5m = getUpperNormalDistrubtion(pair, Candle.FIVE_MINUTE)
		stdDict_15m = getUpperNormalDistrubtion(pair, Candle.FIFTEEEN_MINUTE)
		stdDict_30m = getUpperNormalDistrubtion(pair, Candle.THIRTY_MINUTE)
		t = int(str(datetime.now())[14:16])

		stdDict_1m = getUpperNormalDistrubtion(pair, Candle.ONE_MINUTE)

		# if stdDict_1m['1SD'] < ask:
		# 	logToSlack(tickerMessage(pair, '1', "ask"),  tagChannel=True, channel=Channel.VOLATRADER)

		# if stdDict_1m['1SD'] < bid:
		# 	logToSlack(tickerMessage(pair, '1', "bid"),  tagChannel=True, channel=Channel.VOLATRADER)

		# 5m
		if isCorrectTime(t, 5):

			if stdDict_5m['2SD'] < stdDict_5m['current_vol']:
				logToSlack(createMessage(pair, '2', Candle.FIVE_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)

			elif stdDict_5m['3SD'] < stdDict_5m['current_vol']:
				logToSlack(createMessage(pair, '3', Candle.FIVE_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)
				
			logToSlack(crossover(pair, 5) + getUrl(pair, Candle.FIVE_MINUTE), channel=Channel.VOLATRADER)
		# 15m

		if isCorrectTime(t, 15):
			if stdDict_15m['2SD'] < stdDict_15m['current_vol']:
				logToSlack(createMessage(pair, '2', Candle.FIFTEEEN_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)

			elif stdDict_15m['3SD'] < stdDict_15m['current_vol']:
				logToSlack(createMessage(pair, '3', Candle.FIFTEEEN_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)
			logToSlack(crossover(pair, 15) + getUrl(pair, Candle.FIFTEEEN_MINUTE), channel=Channel.VOLATRADER)

		# 30m

		if isCorrectTime(t, 30):
			if stdDict_30m['2SD'] < stdDict_30m['current_vol'] and isCorrectTime(t, 30):
				logToSlack(createMessage(pair, '2', Candle.THIRTY_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)

			elif stdDict_30m['2SD'] < stdDict_30m['current_vol'] and isCorrectTime(t, 30):
				logToSlack(createMessage(pair, '3', Candle.THIRTY_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)
			logToSlack(crossover(pair, 30) + getUrl(pair, Candle.THIRTY_MINUTE), channel=Channel.VOLATRADER)

		# time.sleep(60)
