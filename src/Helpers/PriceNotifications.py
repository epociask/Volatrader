import statistics as stats

from DB.DBoperations import DBoperations
from Helpers.Enums import Pair, Candle


def getVolumeDataQuery(candleRange: int, pair: Pair, candleSize: Candle) -> str:
	return f'SELECT (VOLUME) FROM {pair.value}_ohlcv_{candleSize.value} ORDER BY TIMESTAMP DESC limit {candleRange};'


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
	print({
		"1SD": mean + stdev,
		"2SD": mean + 2*stdev,
		'3SD': mean + 3*stdev,
		"mean": mean,
		"current_vol": volume[0]
	})

	return {
		"1SD": mean + stdev,
		"2SD": mean + 2*stdev,
		'3SD': mean + 3*stdev,
		"mean": mean,
		"current_vol": volume[0]
	}




def sendAbnormalVolNotif():
	stdDict_5m = getUpperNormalDistrubtion(Pair.ETHUSDT, Candle.FIVE_MINUTE, 500)
	stdDict_15m = getUpperNormalDistrubtion(Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, 500)
	stdDict_30m = getUpperNormalDistrubtion(Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, 500)

	# if stdDict_5m['2SD']:





