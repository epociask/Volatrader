from enum import Enum

class Candle(Enum):
    ONE = "1m"
    FIVE = "5m"
    FIFTEEEN = "15m"
    THIRTY = '30m'
    HOUR = '1h'
    THREEHOUR = "3h"
    TWELVEHOUR = "12h"
    DAY = '1d'
    THREEDAY = '3d'
    WEEK = '1w'
    THREWEEK = "3w"



class Pair(Enum):
    ETHUSDT = "ETHUSDT"
    BTCUSDT = "BTCUSDT"
    STXUSDT = "STXUSDT"
    XRPUSDT = 'XRPUSDT'
    ATOMBTC = "ATOMBTC"
    LTCUSDT = 'LTCUSDT'


class Time(Enum):
    DAY = 24
    ONEWEEK = 168
    TWOWEEK = 336
    THREEWEEK = 504
    MONTH = 700
    TWOMONTH = 1400
    THREEMONTH = 2100

class Indicator(Enum):
    TWOCROW = "2crow"
    THREEBLACKCROWS = '3blackcrows'
    THREEINSIDE = '3inside'
    THREELINESTRIKE = '3linestrike'
    THREEOUTSIDE = '3outside'
    THREESTARSINSOUTH = '3starsinsouth'
    THREEWHITESOLDIERS = '3whitesoldiers'
    ABS = 'abs'
    ACOS = 'acos'
    ACCBANDS = 'accbands'
    AD = 'ad'
    ADOSC = 'adosc'
    ADVANCEBLOCK = 'advanceblock'
    ADX = 'adx'
    ADXR = 'adxr'
    AO = 'ao'
    APO = 'apo'
    AROON = 'aroon'
    AROONOSC = 'aroonosc'
    ASIN = 'asin'
    ATAN = 'atan'
    ATR = 'atr'
    AVGDEV  = 'avgdev'
    AVGPRICE = 'avgprice'
    BBANDS = 'bbands'
    BELTHOLD = 'belthold'
    BETA = 'beta'
    BOP = 'bop'
    BREAKAWAY = 'breakaway'
    CCI = 'cci'
    CEIL = 'ceil'
    CLOSINGMARUBOZU = 'closingmarubozu'
    CMF = 'cmf'
    CMO = 'cmo'
    CONCEALBABYSWALL = 'concealbabyswall'
    CORREL = 'correl'
    COS = 'cos'
    COSH = 'cosh'
    COUNTERATTACK = 'counterattack'
    CVI = 'cvi'
    DARKCLOUDCOVER = 'darkcloudcover'
    DEMA = 'dema'
    DI = 'di'
    DIV = 'div'
    DM = 'dm'
    DOJI = 'doji'
    DOJISTAR = 'dojistar'
    DPO = 'dpo'
    DRAGONFLYDOJI = 'dragonflydoji'
    DX = 'dx'
    EMV = 'emv'
    ENGULFING = 'engulfing'
    EMA = 'ema'
    EVENINGDOJISTAR = 'eveningdojistar'
    EVENINGSTAR = 'eveningstar'
    EXP = 'exp'
    FIBONACCIRETRACEMENT = 'fibonacciretracement'
    FISHER = 'fisher'
    FLOOR = 'floor'
    FOSC = 'fosc'
    GAPSIDEWHITE = 'gapsidewhite'
    GRAVESTONEDOJI = 'gravestonedoji'
    HARAMI = 'harami'
    HAMMER = 'hammer'
    HANGINGMAN = 'hangingman'
    HARAMICROSS = 'haramicross'
    HIKKAKE = 'hikkake'
    HIGHWAVE = 'highwave'
    HMA = 'hma'
    HIKKAEMOD = 'hikkaemod'
    HOMINGPIGEON = 'homingpigeon'
    HT_DCPHASE = 'ht_dcphase'
    HT_PHASOR = 'ht_phasor'
    HT_SINE = 'ht_sine'
    HT_TRENDLINE = 'ht_trendline'
    IDENTICALTHREECROWS = 'identical3crows'
    INVERTEDHAMMER ='invertedhammer'
    INNECK = 'inneck'
    KICKING = 'kicking'
    KAMA = 'kama'
    KICKINGBYLENGTH = 'kickingbylength'
    KVO = 'kvo'
    LADDERBOTTOM = 'ladderbottom'
    LINEARREG = 'linearreg'
    LINEARREG_ANGLE = 'linearreg_angle'
    LINEARREG_SLOP = 'linearreg_slop'
    LINEARREG_INTERCEPT = 'linearreg_intercept'
    LINREG = 'linereg'
    LINREGSLOP = 'lineregslope'
    LINEREGINTERCEPT = 'lineregintercept'
    LN = 'ln'
    LOG = 'log10'
    LONGLEGGEDDOJI = "longleggeddoji"
    LONGLINE = 'longline'
    MACDEXT = 'macdext'
    MACD = 'macd'
    MA = 'ma'
    MAMA = 'mama'
    MACDFIX = 'macdfix'
    MARKETFI = 'marketfi'
    MARUBOZU = 'marubozu'
    MASS = 'mass'
    MATCHINGLOW = 'matchinglow'
    MATHOLD = 'mathold'
    MAVP = 'mavp'
    MAX = 'max'
    MIDPOINT = 'midpoint'
    MIDPRICE = 'midprice'
    MIN = 'min'
    MININDEX = 'minindex'
    MINMAX = 'minmax'
    MINMAXINDEX = 'minmaxindex'
    MFI = 'mfi'
    MINUS_DI = 'minus_di'
    MAXINDEX = 'maxindex'
    MINUS_DM = 'minus_dm'
    MEDPRICE = 'medprice'
    MORNINGSTAR = 'morningstar'
    MOM = 'mom'
    MORNINGDOJISTAR = 'morningdojistar'
    MSW = 'msw'
    MUL = 'mul'
    NATR = 'natr'
    MULT = 'mult'
    NVI = 'nvi'
    OBV = 'obv'
    ONNECK = 'onneck'
    PD = 'pd'
    PIERCING = 'piercing'
    PLUS_DI = 'plus_di'
    PLUS_DM = 'plus_dm'
    PPO = 'ppo'
    PRIORSWINGHIGH = 'priorswinghigh'
    PRIORSWINGLOW = 'priorswinglow'
    PSAR = 'psar'
    PVI = 'pvi'
    RICKSHAWMAN = 'rickshawman'
    QSTICK = 'qstick'
    RISEFALLTHREEMETHODS = 'risefall3methods'
    ROC = 'roc'
    ROCP = 'rocp'
    ROCR = 'rocr'
    ROCR100 = 'rocr100'
    ROUND = 'round'
    RSI = 'rsi'
    SAR = 'sar'
    SEPERATINGLINES = 'seperatinglines'
    SAREXT = 'sarext'
    SHOOTINGSTAR = 'shootingstar'
    SHORTLINE = 'shortline'
    SIN = 'sin'
    SINH = 'sinh'
    SMA = 'sma'
    SPINNINGTOP = 'spinningtop'
    SQRT = 'sqrt'
    STALLEDPATTERN = 'stalledpattern'
    STDDEV = 'stddev'
    STICKSANDWICH = 'sticksandwich'
    STOCHRSI = 'stochrsi'
    STOCH = 'stoch'
    STOCHF = 'stochf'
    STOCHRSI2 = 'stochrsi2'
    STOCHTV = 'stochtv'
    SUM = 'sum'
    SUB = 'sub'
    T3 = 't3'
    SUPERTREND = 'supertrend'
    TAKURI = 'takuri'
    TAN = 'tan'
    TANH = 'tanh'
    TASUKIGAP = 'tasukigap'
    TEMA = 'tema'
    TDSEQUENTIAL = "tdsequential"
    THRUSTING = 'thrusting'
    TODEG = 'todeg'
    TR  = 'tr'
    TRANGE = 'trange'
    TORAD = 'torad'
    TRIMA = 'trima'
    TRISTAR = 'tristar'
    TRIX = 'trix'
    TRUNC = 'trunc'
    TYPPRICE = 'typprice'
    TSF = 'tsf'
    IMI = 'imi'
    UNIQUE3RIVER = 'unique3river'
    UPSIDEGAP2CROWS = 'upsidegap2crows'
    ULTOSC = 'ultosc'
    VAR = 'var'
    VHF = 'vhf'
    VOLATILITY = 'volatility'
    VIDYA = 'vidya'
    VOSC = 'vosc'
    WAD = 'wad'
    WCLPRICE = 'wclprice'
    WCPRICE = 'wcprice'
    VWMA = 'vwma'
    WILDERS = 'wilders'
    WILLR = 'willr'
    WMA = 'wma'
    ZLEMA = 'zlema'
    XSIDEGAP3METHODS = 'xsidegap3methods'
    HT_TRENDMODE = 'ht_trendmode'