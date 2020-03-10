import requests

from Enums import Indicator

'''
Gets indicator values from json candle data from TAAPIO API
@param indicatorName = name of indicator
@param candleJSON = json representation of candle data 
'''


def getIndicator(indicator: Indicator, candleJSON: list) -> list:
    endpoint = "https://ta.taapi.io/{}".format(indicator.value)
    print(f"------------------------------------- {indicator} -----------------------------")
    parameters = {
        'secret': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVtcG9jaWFza0Bkb25zLnVzZmNhLmVkdSIsImlhdCI6MTU4MzMxNzYwNSwiZXhwIjo3ODkwNTE3NjA1fQ.hfTvshR4HJuCSJ4XJNEgb_xkWIuW0ixZXm7OthcwUFk',
        'candles': candleJSON,
        'kPeriod': 3,
        'period': 48,
    }
    resp = requests.post(url=endpoint, json={
        'params': parameters
    })

    print(resp.status_code)

    if resp.status_code == 200:
        result = resp.json()
        if not bool(result): #empty
            print("Empty response body-------{}")
            return None

        return result

    else:
        print("RESPONSE STATUS : ", resp.status_code)
        print("RESPONSE HEADERS: ", resp.headers)
        raise Exception(resp.status_code + " " + resp.headers)


