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

