from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


parameters1 = {
    'start': '1',
    'limit': '5000',
    'convert': 'USD'
}

parmameters2 = {

    'convert': 'USD'
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '417e71e6-cb02-4155-99e5-1f70c20316a8',
}

marketURL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
macroURL = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'
infoURL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
session = Session()
session.headers.update(headers)


def getMarketData():
    try:
        response = session.get(marketURL, params=parameters1)
        data = json.loads(response.text)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return data["data"]


def getMacroEconomicData():
    try:
        response = session.get(macroURL, params=parmameters2)
        data = json.loads(response.text)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


    print(data)
    return data["data"]


## Gets top percent change coins
def getTopPercentChange(timePeriod, numCoins, minVolume=10000.00):
    assert timePeriod in ['1h', '24h', '7d'], "Time period must be 1h, 24h, or 7d"
    timePeriod = f'percent_change_{timePeriod}'

    def filt(val):
        if str(type(val['quote']['USD'][timePeriod])) != '<class \'NoneType\'>' and val['quote']['USD']['volume_24h'] is not None:
            if float(val['quote']['USD']['volume_24h']) > minVolume:
                return True 
        return False 
    results = [e for e in filter(filt, [e for e in sorted(getMarketData(), key = lambda i: i['quote']['USD'][timePeriod] if i['quote']['USD'][timePeriod] is not None else 0, reverse=True)])]
    return {e['symbol'] : {"%change": f"%{e['quote']['USD'][timePeriod]}", "volume" : e['quote']['USD']['volume_24h']} for e in results[:numCoins]}
 

def getTopVolumeCoins(numCoins):
    getVal = lambda key : key['quote']['USD']['volume_24h'] if key['quote']['USD']['volume_24h'] is not None else 0.0
    whitelist_coins = ['ETH', 'BTC', 'XRP', 'LTC', 'EOS', 'BCH', 'XMR', 'XTZ']
    x = lambda x: x in whitelist_coins
    recent = [f"{e}/USDT" for e in filter(x , [e['symbol'] for e in sorted(getMarketData(), key = lambda key: getVal(key), reverse=True)[:14]])]
    return recent[:numCoins]