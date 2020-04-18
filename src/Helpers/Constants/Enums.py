from enum import Enum
import ccxt 
# from Helpers.API.Stock_API import STOCK_MARKET
class Candle(Enum):
    """
    Enum to represent all possible candle sizes
    """
    ONE_MINUTE = "1m"
    FIVE_MINUTE = "5m"
    FIFTEEEN_MINUTE = "15m"
    THIRTY_MINUTE = '30m'
    HOUR = '1h'
    THREE_HOUR = "3h"
    TWELVE_HOUR = "12h"
    ONE_DAY = '1d'
    THREE_DAY = '3d'
    ONE_WEEK = '1w'
    THRE_WEEK = "3w"

class Market(Enum):
    BINANCE = ccxt.binance()
    KRAKEN = ccxt.kraken()
    # STOCK = STOCK_MARKET()

class SessionType(Enum):
    BACKTEST = 0
    PAPERTRADE = 1
    LIVETRADE = 2


class Pair(Enum):
    """
    Enum to represent all base/quote currency pairs
    """
    ETHUSDT = "ETHUSDT"
    BTCUSDT = "BTCUSDT"
    STXUSDT = "STXUSD"
    XRPUSDT = 'XRPUSDT'
    ATOMBTC = "ATOMUSD"
    LTCUSDT = 'LTCUSDT'
    LINKUSDT = 'LINKUSDT'
    ORBS = 'ORBSUSDT'


class Time(Enum):
    """
    enum to represent all time instances
    """
    DAY = 24
    THREEDAY = 72
    ONEWEEK = 168
    TWOWEEK = 336
    THREEWEEK = 504
    MONTH = 700
    TWOMONTH = 1400
    THREEMONTH = 2100
    SIXMONTH = 4200


class Indicator(Enum):
    """
    Enum to represent all TAAPIO indicator instances
    """
    TWOCROW = "2crows"
    THREEBLACKCROWS = '3blackcrows'
    THREEINSIDE = '3inside'
    THREELINESTRIKE = '3linestrike'
    THREEOUTSIDE = '3outside'
    THREESTARSINSOUTH = '3starsinsouth'
    THREEWHITESOLDIERS = '3whitesoldiers'
    ABS = 'abs'
    ACOS = 'acos'
    # ACCBANDS = 'accbands'
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
    # AVGDEV  = 'avgdev'                      #required period param
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
    # CVI = 'cvi'                           #        requires mandatory parameter
    DARKCLOUDCOVER = 'darkcloudcover'
    DEMA = 'dema'
    # DI = 'di'                              #          requires mandatory parameter
    DIV = 'div'
    # DM = 'dm'                               #         requires mandatory parameter
    DOJI = 'doji'
    DOJISTAR = 'dojistar'
    # DPO = 'dpo'
    DRAGONFLYDOJI = 'dragonflydoji'
    DX = 'dx'
    EMV = 'emv'
    ENGULFING = 'engulfing'
    # EMA = 'ema'```````             not working atm
    EVENINGDOJISTAR = 'eveningdojistar'
    EVENINGSTAR = 'eveningstar'
    EXP = 'exp'
    FIBONACCIRETRACEMENT = 'fibonacciretracement'
    FISHER = 'fisher'
    FLOOR = 'floor'
    # FOSC = 'fosc'
    GAPSIDEWHITE = 'gapsidesidewhite'
    GRAVESTONEDOJI = 'gravestonedoji'
    HARAMI = 'harami'
    HAMMER = 'hammer'
    HANGINGMAN = 'hangingman'
    HARAMICROSS = 'haramicross'
    HIKKAKE = 'hikkake'
    HIGHWAVE = 'highwave'
    HMA = 'hma'
    HIKKAE = 'hikkake'
    HOMINGPIGEON = 'homingpigeon'
    # HT_DCPHASE = 'ht_dcphase'
    # HT_PHASOR = 'ht_phasor'
    #  HT_SINE = 'ht_sine'
    # HT_TRENDLINE = 'ht_trendline'
    IDENTICALTHREECROWS = 'identical3crows'
    INVERTEDHAMMER = 'invertedhammer'
    INNECK = 'inneck'
    KICKING = 'kicking'
    KAMA = 'kama'
    # KICKINGBYLENGTH = 'kickingbylength'
    # KVO = 'kvo'
    # LADDERBOTTOM = 'ladderbottom'
    # LINEARREG = 'linearreg'
    # LINEARREG_ANGLE = 'linearreg_angle'
    # LINEARREG_SLOP = 'linearreg_slope'
    # LINEARREG_INTERCEPT = 'linearreg_intercept'
    # LINREG = 'linreg'
    # LINREGSLOP = 'lineregslope'
    LINEREGINTERCEPT = 'linregintercept'
    LN = 'ln'
    LOG = 'log10'
    LONGLEGGEDDOJI = "longleggeddoji"
    LONGLINE = 'longline'
    # MACDEXT = 'macdext'
    # MACD = 'macd'
    MA = 'ma'
    MAMA = 'mama'
    MACDFIX = 'macdfix'
    # MARKETFI = 'marketfi'
    MARUBOZU = 'marubozu'
    MASS = 'mass'
    MATCHINGLOW = 'matchinglow'
    MATHOLD = 'mathold'
    # MAVP = 'mavp'
    MAX = 'max'
    MIDPOINT = 'midpoint'
    MIDPRICE = 'midprice'
    MIN = 'min'
    MININDEX = 'minindex'
    MINMAX = 'minmax'
    # MINMAXINDEX = 'minmaxindex'
    MFI = 'mfi'
    # MINUS_DI = 'minus_di'
    MAXINDEX = 'maxindex'
    # MINUS_DM = 'minus_dm'
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
    # PLUS_DI = 'plus_di'
    # PLUS_DM = 'plus_dm'
    PPO = 'ppo'
    PRIORSWINGHIGH = 'priorswinghigh'
    # PRIORSWINGLOW = 'priorswinglow'
    # PSAR = 'psar'
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
    # SEPERATINGLINES = 'separatinglines'
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
    # STOCHF = 'stochf'
    # STOCHRSI2 = 'stochrsi2'
    STOCHTV = 'stochtv'
    SUM = 'sum'
    SUB = 'sub'
    T3 = 't3'
    # SUPERTREND = 'supertrend'  giving weird error @TODO fix
    TAKURI = 'takuri'
    TAN = 'tan'
    TANH = 'tanh'
    TASUKIGAP = 'tasukigap'
    TEMA = 'tema'
    TDSEQUENTIAL = "tdsequential"
    THRUSTING = 'thrusting'
    TODEG = 'todeg'
    TR = 'tr'
    TRANGE = 'trange'
    TORAD = 'torad'
    TRIMA = 'trima'
    TRISTAR = 'tristar'
    TRIX = 'trix'
    TRUNC = 'trunc'
    TYPPRICE = 'typprice'
    TSF = 'tsf'
    # IMI = 'imi'
    UNIQUE3RIVER = 'unique3river'
    UPSIDEGAP2CROWS = 'upsidegap2crows'
    ULTOSC = 'ultosc'
    VAR = 'var'
    VHF = 'vhf'
    VOLATILITY = 'volatility'
    # VIDYA = 'vidya'        #requires mandatory params
    # VOSC = 'vosc'          #requires mandatory params
    WAD = 'wad'
    WCLPRICE = 'wclprice'
    WCPRICE = 'wcprice'
    # VWMA = 'vwma'           #requires mandatory params
    # WILDERS = 'wilders'        #requires mandatory params
    WILLR = 'willr'
    WMA = 'wma'
    # ZLEMA = 'zlema'            #requires mandatory params
    XSIDEGAP3METHODS = 'xsidegap3methods'
    # HT_TRENDMODE = 'ht_trendmode'
