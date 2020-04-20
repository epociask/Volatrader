
"""
Helper script w/ all TAAPIO indicators to be referenced for referencing strats as dictionaries
"""


def getIndicator(name:  str):

    name = "".join(e for e in name if not e.isdigit() and e != "_")
    return globals()[name]

#    return{ "ADX VALUE" :adx_values.adx().iat[-1], "DI+": adx_values.adx_neg().iat[-1], "DI-": adx_values.adx_pos().iat[-1]}
ADX = [False, 'ADX VALUE', "DI+", "DI-"]
BB = [True, 'MOVING AVERAGE BB', 'UPPER BAND BB', 'LOWER BAND BB']
PATTERNTHREEINSIDE = [True]
PATTERNTHREEBULLISHSOLDIERS = [True]
PATTERNTHREEBEARISHSOLDIERS = [True]
PATTERNONNECKLINE = [True]
PATTERNTHREELINESTRIKE = [True]
PATTERNMORNINGSTAR = [True]
PATTERNTWEEZER = [True]
PATTERNTHREELINESTRIKEBEARISHREVERSAL = [True]
PATTERNBEARISHENGULFING = [True]
HAMMER = [True]
EMA = [True]
MACD = [False, "MACD Line", "MACD Histogram", "Signal Line"]
SMA = [True]
RSI = [False]
RSIDIVERGENCE = [False]
UPTREND = [True]
















accbands = {
    "valueUpperBand": None,
    "valueMiddleBand": None,
    "valuelowerband": None,
}

aroon = {
    "valueAroonDown": None,
    "valueAroonUp": None,
}

bbands = {
    "valueUpperBand": None,
    "valueMiddleBand": None,
    "valueLowerBand": None,
}

candle = {
    'timestamp': None,
    'open': None,
    'high': None,
    'low': None,
    'close': None,
    'volume': None,
}

di = {
    'plus_di': None,
    'minus_di': None,
}

dm = {
    'plus_dm': None,
    'minus_dm': None,
}

fisher = {
    "fisher": None,
    "fisher_signal": None,
}

ht_phasor = {
    'valueInPhase': None,
    'valueQuadrature': None,
}

ht_sine = {
    'valueSine': None,
    'valueLeadSine': None,
}

macd = {
    "valueMACD": None,
    "valueMACDSignal": None,
    "valueMACDHist": None,
}

macdext = {
    "valueMACD": None,
    "valueMACDSignal": None,
    "valueMACDHist": None,
}

macdfix = {
    "valueMACD": None,
    "valueMACDSignal": None,
    "valueMACDHist": None,
}

mama = {
    'valueMAMA': None,
    'valueFAMA': None,
}

minmax = {
    "valueMin": None,
    "valueMaxIdx": None,
}

minmaxindex = {
    "valueMin": None,
    "valueMaxIdx": None,
}

msw = {
    "msw_sine": None,
    "msw_lead": None,
}

priorswinghigh = {
    "valueClose": None,
    "valueHigh": None,
}

priorswinglow = {
    "valueClose": None,
    "valueHigh": None,
}

stoch = {
    "valueSlowK": None,
    "valueSlowD": None,
}
stochf = {
    "valuefastK": None,
    "valueFastD": None,
}

stochrsi = {
    "valuefastK": None,
    "valueFastD": None,
}
stochrsi2 = {
    "valueK": None,
    "valueD": None,
}

stochtv = {
    'valueK': None,
    'valueD': None,
}

supertrend = {
    "value": None,
    "valueAdvice": None,
}

tdsequential = {

    "buySetupIndex": None,
    "sellSetupIndex": None,
    "buyCoundownIndex": None,
    "sellCoundownIndex": None,
    "countdownIndexIsEqualToPreviousElement": None,
    "sellSetup": None,
    "buySetup": None,
    "sellSetupPerfection": None,
    "buySetupPerfection": None,
    "bearishFlip": None,
    "bullishFlip": None,
    "TDSTBuy": None,
    "TDSTSell": None,
    "countdownResetForTDST": None,

}


