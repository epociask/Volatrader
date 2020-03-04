import requests


def getIndicator(indicatorName: str, candleJSON):
    endpoint = "https://ta.taapi.io/{}".format(indicatorName)


    parameters = {
        'secret':  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..RzHJZLnEb4HzluravWjaQZg1W9jd7Jl4wDi0lgnY5jc',
        'candles': candleJSON,
        'optInFastK_Period': 6,
    }
    resp = requests.post(url=endpoint, json={
        'params': parameters
    })

    print(resp.status_code)

    if resp.status_code == 200:
        result = resp.json()
        print(resp)
        return result

    else:
        print(resp.status_code)
        print(resp.headers)
        print(resp.content)
        raise Exception(resp.status_code + " " + resp.headers)


