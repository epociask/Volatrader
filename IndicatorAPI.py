import requests

def getIndicator(indicatorName: str, candleJSON):
    endpoint = "https://ta.taapi.io/{}".format(indicatorName)


    parameters = {
        'secret':  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVtcG9jaWFza0Bkb25zLnVzZmNhLmVkdSIsImlhdCI6MTU4MzMxNzYwNSwiZXhwIjo3ODkwNTE3NjA1fQ.hfTvshR4HJuCSJ4XJNEgb_xkWIuW0ixZXm7OthcwUFk',
        'candles': candleJSON,
        'kPeriod': 3,
    }
    resp = requests.post(url=endpoint, json={
        'params': parameters
    })

    print(resp.status_code)

    if resp.status_code == 200:
        result = resp.json()
        if not bool(result):
            print("Empty response body-------{}")
            return None

        return result

    else:
        print("Response status code : ",resp.status_code)
        print(resp.headers)
        print(resp.content)
        raise Exception(resp.status_code + " " + resp.headers)

