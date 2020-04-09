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
from ccxt.base.errors import BadSymbol

exchange = ccxt.kraken({
    'enableRateLimit': True,  # this option enables the built-in rate limiter
})

def getVolumeData(pair: str, candleSize: Candle):
	logDebugToFile(f"Getting volume data for {pair} {candleSize}")
	pair = pair.value.replace("USD", "/USD") if type(pair) is not str else pair
	candles = exchange.fetchOHLCV(pair, candleSize.value)
	return [float(e[5]) for e in candles]


def getUpperNormalDistrubtion(pair: Pair, candleSize: Candle, volume=None):

	# if volume is None:
	try:
		volume = getVolumeData(pair, candleSize)
		stdev = stats.stdev(volume) if volume is not None else "Volume data not available"
		mean = sum(volume) / len(volume)

		return {
			"1SD": mean + stdev,
			"2SD": mean + 2 * stdev,
			'3SD': mean + 3 * stdev,
			"mean": mean,
			"current_vol": volume[0]
		}

	except BadSymbol:
		raise BadSymbol("Bad symbol provided to Kraken")






def getUrl(pair: str, candleSize: Candle):
	return 	"https://trade.kraken.com/markets/kraken/" + pair.lower() + "/" + candleSize.value
	

def crossover(pair, candleSize):		
	pair = pair.value.replace("USD", "/USD") if type(pair) is not str else pair

	close = [e[4] for e in exchange.fetch_ohlcv(pair, timeframe=candleSize.value, limit=14)]
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
		return None 


def handleLogging(stdDict: str, pair: str, candleSize: Candle):
  
	createMessage = lambda pair, devs, candleSize: f"[VOLATILITY ALERT] CURRENT {pair} VOLUME ABOVE {devs} STANDARD DEVIATIONS FOR {candleSize.value} CANDLE"
	tickerMessage = lambda pair, devs, askbid: f"[VOLATILITY ALERT] CURRENT {pair} VOLUME ABOVE {devs} STANDARD DEVIATIONS FOR {askbid} VOLUME"

	if stdDict['2SD'] < stdDict['current_vol']:
		logToSlack(createMessage(pair, '2', candleSize.value), tagChannel=True, channel=Channel.VOLATILITY_ALERTS)

	elif stdDict['3SD'] < stdDict['current_vol']:
		logToSlack(createMessage(pair, '3', candleSize.value), tagChannel=True, channel=Channel.VOLATILITY_ALERTS)
		
	# co = crossover(pair, candleSize.value) 

	# if co is not None:
	# 	logToSlack(co + f" [{pair}/{candleSize.value}]" + "\n" + getUrl(pair, candleSize.value) , channel=Channel.VOLATRADER)

def sendAbnormalVolumeNotification(pair: Pair):
	pair = pair.value if type(pair) is not str else pair
	global exchange
	isCorrectTime = lambda t,val : t % val == 0 or t == 0
	while True:
		t = int(str(datetime.now())[14:16])
		# 5m
		if isCorrectTime(t, 5):
			stdDict_5m = getUpperNormalDistrubtion(pair, Candle.FIVE_MINUTE)
			handleLogging(stdDict_5m, pair, Candle.FIVE_MINUTE)
	
		# 15m

		if isCorrectTime(t, 15):
			stdDict_15m = getUpperNormalDistrubtion(pair, Candle.FIFTEEEN_MINUTE)
			handleLogging(stdDict_15m, pair, Candle.FIFTEEEN_MINUTE)
		# 30m

		if isCorrectTime(t, 30):
			stdDict_30m = getUpperNormalDistrubtion(pair, Candle.THIRTY_MINUTE)
			handleLogging(stdDict_30m, pair, Candle.THIRTY_MINUTE)
		# time.sleep(60)
