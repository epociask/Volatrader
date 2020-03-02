import requests
def getIndicator(indicatorName: str, candleJSON):
    endpoint = "https://ta.taapi.io/{}".format(indicatorName)

    parameters = {
        'secret': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVtcG9jaWFza0Bkb25zLnVzZmNhLmVkdSIsImlhdCI6MTU4MDM2NjEzMCwiZXhwIjo3ODg3NTY2MTMwfQ.0WA7JOq3lPPHOdhgbUCdx7NDr3L9_4374Z44oNM5KiE',
        'candles': candleJSON,
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
        raise Exception(resp.status_code + " " + resp.headers)


