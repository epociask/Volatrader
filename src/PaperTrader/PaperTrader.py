import time
import datetime
from Helpers.Logger import logToSlack, logDebugToFile
from Trader.TradeSession import TradeSession
from Helpers.Logger import Channel
from Helpers.Constants.Enums import Pair, Candle, SessionType
from DataBasePY.DBReader import DBReader
from DataBasePY.DBwriter import DBwriter
from Strategies import strategies
from Helpers.DataOperators import fetchCandleData, convertCandlesToDict
from Helpers.API.MarketFunctions import getCurrentBinancePrice
import ccxt
import re
from Helpers.DataOperators import printLogo
import uuid


convertToVal = lambda candleEnum: candleEnum.value[0: len(candleEnum.value) - 2]


class PaperTrader:

    def __init__(self):
        self.takeProfitPercent = None
        self.strategy = None
        self.tradingSession = None
        self.pair = None
        self.candleSize = None
        self.stratName = None
        self.strategy = None
        self.takeProfitPercent = None
        self.stopLossPercent = None
        self.principle = None
        self.startTime = None
        self.currentPrice = None
        self.writer = DBwriter()
        self.sessionid = uuid.uuid4()
        self.timeToRun = None

    def getResults(self) -> str:
        return self.tradingSession.getResults()


    def trade(self, pair: Pair, candleSize: Candle, strategy: str, stopLossPercent: int, takeProfitPercent: int,
            principle: int, timeToRun):
        """

        :param pair:
        :param candleSize:
        :param strategy:
        :param stopLossPercent:
        :param takeProfitPercent:
        :param principle:
        :return:
        """
        self.timeStep = int(re.sub("[^0-9]", "", candleSize.value))
        print(self.timeStep)
        self.pair = pair
        self.candleSize = candleSize
        self.takeProfitPercent = f"0{takeProfitPercent}" if takeProfitPercent - 10 <= 0 else f"{takeProfitPercent}"
        self.stratName = strategy
        strategy = strategies.getStrat(self.stratName)
        self.strategy = strategy(pair, candleSize, principle)
        self.stopLossPercent = stopLossPercent
        self.tradingSession = TradeSession(pair, self.strategy, takeProfitPercent, self.stopLossPercent, self.stratName,
                                    SessionType.PAPERTRADE, sessionid=self.sessionid)
        self.principle = principle
        self.timeToRun = timeToRun
        self.start()



    def start(self):
        """

        :return: unique session id
        """

        try:

            first = True
            bought = False
            end_time = datetime.datetime.now() + datetime.timedelta(hours=self.timeToRun)

            logToSlack(f"Starting Paper Trader for {self.pair.value}/{self.candleSize.value} \nstrat: {self.stratName}\n takeprofit: %{int(self.takeProfitPercent)}\n stoploss: %{self.stopLossPercent}\n Finishing on {end_time}", channel=Channel.PAPERTRADER)

            while datetime.datetime.now() < end_time:
                t = int(str(datetime.datetime.now())[14:16])

                if first:
                    first = False

                    try:
                        logDebugToFile("starting preinstall for strat")
                        for candle in convertCandlesToDict(fetchCandleData(ccxt.binance(), self.pair, self.candleSize, self.strategy.candleLimit)):
                            self.tradingSession.update(candle)


                    except:
                        logDebugToFile("Error instantiating strategy in paper trader")

                    try:
                        logDebugToFile(f"Writing data to db for paper trader session {self.sessionid}")
                        self.writer.writePaperTradeStart(self.sessionid, datetime.datetime.now(), self.stratName, self.pair, self.candleSize, self.principle)
                    except Exception as e:
                        logDebugToFile("Eror writing to postgres")
                        raise e

                if (t % self.timeStep == 0 or t == 0):
                    time.sleep(6)
                    data = convertCandlesToDict(fetchCandleData(ccxt.binance(), self.pair, self.candleSize, 1))
                    bought = self.tradingSession.update(data[0], True)
                    logDebugToFile(F"bought status ->{bought}")
                    if not bought:
                        time.sleep(60)


                if (t == 0) and datetime.datetime.now().second in range(0, 15):
                    logToSlack(f"[PAPERTRADER] hourly update for {self.pair.value} for strat: {self.stratName} \n {self.getResults()}", channel=Channel.PAPERTRADER)

                if bought:
                    time.sleep(5)
                    self.currentPrice, _ = getCurrentBinancePrice(self.pair)
                    ts = datetime.datetime.now()
                    logDebugToFile(f"Checking for sell w/ {self.pair} @ {self.currentPrice}")
                    dummyCandle = {"close": self.currentPrice, "timestamp": ts}
                    logDebugToFile(dummyCandle)
                    bought = self.tradingSession.update(dummyCandle, False)

                
                if datetime.datetime.now().minute % 5 == 0 and self.currentPrice is not None:
                    logDebugToFile(f"WRITING CURRENT PNL for session{self.sessionid}")
                    currentpnl = self.tradingSession.getCurrentPnl(self.currentPrice)
                    logDebugToFile(f'PNL being written ---- > {currentpnl}')                
                    self.writer.writeTotalPnl(currentpnl, self.principle, self.sessionid)



                if not DBReader().getActiveStatus(self.sessionid):
                    raise Exception("I've been terminated")
                    return self.sessionid
        except Exception as e:
            logToSlack(e)
            self.writer.writePaperTradeEnd(self.sessionid)

        except KeyboardInterrupt:
            self.writer.writePaperTradeEnd(self.sessionid)
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
