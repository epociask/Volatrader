import statistics as stats
import time
from datetime import datetime
from threading import Thread

import ccxt
from DB.DBoperations import DBoperations
from Helpers.Enums import Pair, Candle
from Helpers.Logger import logToSlack, Channel

f = ccxt.binance()


def getAskBidVolume(pair: Pair):
	pair = pair.value.replace("USDT", "/USDT")
	return f.fetch_ticker(pair)['askVolume'], f.fetch_ticker(pair)['bidVolume']



def getVolumeData(pair: Pair, candleSize: Candle):
	candles = f.fetchOHLCV(pair.value.replace("USDT", "/USDT"), candleSize.value)
	return [int(e[5]) for e in candles]


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


def sendAbnormalVolumeNotification(pair: Pair):

	createMessage = lambda pair, devs, candleSize: f"[VOLATILITY ALERT] CURRENT {pair.value} VOLUME ABOVE {devs} STANDARD DEVIATIONS FOR {candleSize.value} CANDLE"
	tickerMessage = lambda pair, devs, askbid: f"[VOLATILITY ALERT] CURRENT {pair.value} VOLUME ABOVE {devs} STANDARD DEVIATIONS FOR {askbid} VOLUME"
	ask, bid = getAskBidVolume(pair)
	isCorrectTime = lambda t,val : t % val == 0 or t == 0
	while True:
		stdDict_5m = getUpperNormalDistrubtion(pair, Candle.FIVE_MINUTE)
		stdDict_15m = getUpperNormalDistrubtion(pair, Candle.FIFTEEEN_MINUTE)
		stdDict_30m = getUpperNormalDistrubtion(pair, Candle.THIRTY_MINUTE)
		t = int(str(datetime.now())[14:16])

		stdDict_1m = getUpperNormalDistrubtion(pair, Candle.ONE_MINUTE)

		if stdDict_1m['1SD'] < ask:
			logToSlack(tickerMessage(pair, '1', "ask"),  tagChannel=True, channel=Channel.VOLATRADER)

		if stdDict_1m['1SD'] < bid:
			logToSlack(tickerMessage(pair, '1', "bid"),  tagChannel=True, channel=Channel.VOLATRADER)

		# 5m
		if isCorrectTime(t, 5):

			if stdDict_5m['2SD'] < stdDict_5m['current_vol']:
				logToSlack(createMessage(pair, '2', Candle.FIVE_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)

			elif stdDict_5m['3SD'] < stdDict_5m['current_vol']:
				logToSlack(createMessage(pair, '3', Candle.FIVE_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)

		# 15m

		if isCorrectTime(t, 15):
			if stdDict_15m['2SD'] < stdDict_15m['current_vol']:
				logToSlack(createMessage(pair, '2', Candle.FIFTEEEN_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)

			elif stdDict_15m['3SD'] < stdDict_15m['current_vol']:
				logToSlack(createMessage(pair, '3', Candle.FIFTEEEN_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)

		# 30m

		if isCorrectTime(t, 30):
			if stdDict_30m['2SD'] < stdDict_30m['current_vol'] and isCorrectTime(t, 30):
				logToSlack(createMessage(pair, '2', Candle.THIRTY_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)

			elif stdDict_30m['2SD'] < stdDict_30m['current_vol'] and isCorrectTime(t, 30):
				logToSlack(createMessage(pair, '3', Candle.THIRTY_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)

		time.sleep(60)


