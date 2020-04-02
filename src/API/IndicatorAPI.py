import requests
from Helpers.Enums import Indicator
from Helpers.Logger import logErrorToFile, logToSlack
import graphene
IndicatorENUMS = [e for e in Indicator]
def getIndicator(indicator: Indicator, candleJSON: list) -> (list, None):
    """
    Gets indicator values from json candle data from TAAPIO API
    @:param indicatorName = name of indicator
    @:param candleJSON = json representation of candle data
    """
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
        err = f"TAAPIO response status code : {resp.status_code}  \n content: {resp.content}"
        # logErrorToFile(err)
        logToSlack(err)
        raise Exception(resp.status_code + " " + resp.headers)


# query {
#   indicators(
#     secret: "MY_SECRET",
#     candles: [
#     ],
#     queries: [{
#       indicator: "rsi",
#       candles: [
#         {
#           timestamp: 93249032,
#           open: 238,
#           close: 328,
#           high: 382,
#           low: 281,
#           volume: 2839283,
#         },{
#           timestamp: 93249032,
#           open: 238,
#           close: 328,
#           high: 382,
#           low: 281,
#           volume: 2839283,
#         },
#         ... n candles
#       ],
#     },{
#       indicator: "macd",
#       params: [
#          { name: "optInFastPeriod", value: "8" },
#          { name: "optInSlowPeriod", value: "12" },
#          { name: "optInSignalPeriod", value: "5" },
#       ],
#     }]
#   ) {
#     id,
#     indicator,
#     result {
#       key,
#       value
#     }
#   }
# }


def getIndicators(candleJSON: str):

    const = "query{\n" \
            "indicators(\n" \
            "secret: "

    for indicator in IndicatorENUMS:

    endpoint = "https://ta.taapi.io/graphql"

    resp = requests.post(url=endpoint, json={


    print(resp.status_code)

    if resp.status_code == 200:
        result = resp.json()
        if not bool(result):  # empty
            print("Empty response body-------{}")
            return None

        return result

    else:
        err = f"TAAPIO response status code : {resp.status_code}  \n content: {resp.content}"
        logToSlack(err)
        raise Exception(resp.status_code + " " + resp.headers)


