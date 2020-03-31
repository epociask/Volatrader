import statistics as stats

from DB.DBoperations import DBoperations
from Helpers.Enums import Pair, Candle
from Helpers.Logger import logToSlack, Channel


def getVolumeDataQuery(candleRange: int, pair: Pair, candleSize: Candle) -> str:
	return f'SELECT (VOLUME) FROM {pair.value}_ohlcv_{candleSize.value} ORDER BY timestamp desc limit {candleRange}'


def getVolumeData(pair: Pair, candleSize: Candle, candleRange: int):
	query = getVolumeDataQuery(candleRange, pair, candleSize)
	db = DBoperations()
	db.connect()
	print(db.connStatus())
	db.cur.execute(query)
	return [int(e[0]) for e in db.cur.fetchall()]


def getUpperNormalDistrubtion(pair: Pair, candleSize: Candle, candleRange: int):

	volume = getVolumeData(pair, candleSize, candleRange)
	stdev = stats.stdev(volume)
	mean = sum(volume)/len(volume)

	return {
		"1SD": mean + stdev,
		"2SD": mean + 2*stdev,
		'3SD': mean + 3*stdev,
		"mean": mean,
		"current_vol": volume[0]
	}


def sendAbnormalVolumeNotification():
	stdDict_5m = getUpperNormalDistrubtion(Pair.ETHUSDT, Candle.FIVE_MINUTE, 500)
	stdDict_15m = getUpperNormalDistrubtion(Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, 500)
	stdDict_30m = getUpperNormalDistrubtion(Pair.ETHUSDT, Candle.THIRTY_MINUTE, 500)
	createMessage = lambda pair, devs, candleSize: f"[VOLATILITY ALERT] CURRENT {pair.value} VOLUME ABOVE {devs} STANDARD DEVIATIONS FOR {candleSize.value} CANDLE"

	print(stdDict_30m)

	# 5m
	if stdDict_5m['2SD'] < stdDict_5m['current_vol']:
		logToSlack(createMessage(Pair.ETHUSDT, '2', Candle.FIVE_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)

	elif stdDict_5m['3SD'] < stdDict_5m['current_vol']:
		logToSlack(createMessage(Pair.ETHUSDT, '3', Candle.FIVE_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)

	# 15m
	if stdDict_15m['2SD'] < stdDict_15m['current_vol']:
		logToSlack(createMessage(Pair.ETHUSDT, '2', Candle.FIFTEEEN_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)

	elif stdDict_15m['3SD'] < stdDict_15m['current_vol']:
		logToSlack(createMessage(Pair.ETHUSDT, '3', Candle.FIFTEEEN_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)

	# 30m
	if stdDict_30m['2SD'] < stdDict_30m['current_vol']:
		logToSlack(createMessage(Pair.ETHUSDT, '2', Candle.THIRTY_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)

	elif stdDict_30m['2SD'] < stdDict_30m['current_vol']:
		logToSlack(createMessage(Pair.ETHUSDT, '3', Candle.THIRTY_MINUTE), tagChannel=True, channel=Channel.VOLATRADER)

sendAbnormalVolumeNotification()