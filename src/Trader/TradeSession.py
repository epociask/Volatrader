import time
from termcolor import colored
from Trader.SellLogic import Instance
from Helpers.Constants.Enums import *
from Helpers.Logger import logDebugToFile, logToSlack, Channel
from Helpers.API.MarketFunctions  import getCurrentBinancePrice
import ccxt
from Helpers.TimeHelpers import convertNumericTimeToString
import uuid
from DataBasePY.DBwriter import DBwriter


class TradeSession:
    """
    Class to hold buying and selling logic and execute each accordingly to price updates
    """

    def __init__(self, pair, buyStrategy, takeProfitPercent, percentSL, stratString: str, sessionType: Enum, principle= 1000, sessionid=None):
        self.pair = pair
        self.sellStrat = Instance(pair)
        self.sellStrat.setStopLossPercent(percentSL)
        self.profitlosses = []
        self.stratString = stratString
        self.buy = False
        self.buyPrice = 0
        self.buyTime = ""
        self.sellTime = ""
        self.takeProfit = 0
        self.sellPrice = 0
        self.profitLoss = None
        self.sell = False
        self.quantity = None
        self.STRATEGY = buyStrategy
        self.takeProfitPercent = float(f"1.{takeProfitPercent}")
        self.results = []
        self.positiveTrades = 0
        self.NegativeTrades = 0
        self.type = sessionType
        self.prevcandle = None
        self.fee = .1/100
        self.calcWithFee = lambda price: price * float(1 - self.fee)
        self.totalFees = []
        self.principle = principle
        self.principleOverTime = []
        self.writer = DBwriter()
        self.sessionid = sessionid


    def getTotalFees(self):
        return sum(self.totalFees)

    def getCurrentPnl(self, currentPrice):
            allPnl = self.profitlosses

            if self.buyPrice is not 0:
                print("first condition in getCurrentPNl")
                currentPnl = ((currentPrice - self.buyPrice) / self.buyPrice) * 100
                allPnl.append(currentPnl)

            
            try:
                return sum(allPnl)

            except Exception as e:
                logDebugToFile(e)

            

       

    def getStopLossPercent(self):
        """
        :returns: Percent stop loss
        """
        return self.sellStrat.percentStopLoss

    def getTakeProfitPercent(self):
        """
        :returns: percent take profit
        """
        return self.takeProfitPercent

    def getTradeData(self) -> (int, int):
        """
        @returns # of winning and # of losing trades
        """
        return self.positiveTrades, self.NegativeTrades


    def addResult(self) -> None:
        """
        Adds trade result to results list
        updates winning and losing trade counts
        @:returns None
        """

        self.results.append({"buytime": convertNumericTimeToString(self.buyTime), "buyprice": self.buyPrice, "selltime": convertNumericTimeToString(self.sellTime),
                             "sellprice": self.sellPrice, "profitloss": self.profitLoss})
        if self.profitLoss > 0:
            self.positiveTrades += 1
        else:
            self.NegativeTrades += 1

    def reset(self) -> None:
        """
        reset function to reset class members after selling
        """
        # logDebugToFile(f"Resetting for {self.pair}")

        self.addResult()
        self.sellStrat.reset()
        self.buy = False
        self.buyPrice = 0
        self.sellPrice = 0
        self.profitLoss = None
        self.sell = False
        self.quantity = 0

    def calcPL(self) -> None:
        """
        Calculate profit loss function
        @:returns None
        """

        self.profitLoss = (100 - (100 * (self.buyPrice / self.sellPrice))) if self.sellPrice > self.buyPrice else -(
                100 - (100 * (self.sellPrice / self.buyPrice)))

    def toString(self) -> str:
        """
        ToString method
        @:returns toString representation of Session instance
        """

        return "Buy Price {} Buy Time: {} \nSell Price {} Sell time: {}\nProfit Loss: {}\n".format(self.buyPrice, self.buyTime,
                                                                                        self.sellPrice, self.sellTime,
                                                                                        self.profitLoss)

    def getTotalPL(self):
        """
        @:returns total profit-loss percentage after running strategy
        """

        return sum(self.profitlosses)

    def CHECK_STOPLOSS(self, candle):
        """
        Uses sell logic instance to see if it's time to sell
        @:returns boolean
        """
        # logDebugToFile("Checking sell")
        if self.sellStrat.run(float(candle['close'])) or self.takeProfit <= float(candle['close']):

            return True

        return False


    def update(self, candle, update=True) -> bool:
        """
        main function
        @:param candle
        takes in @:param candle and makes buy/sell or do-nothing decisions accordingly
        @:returns None
        """
        if not self.buy:    #not bought

            self.principleOverTime.append(self.principle)

            if self.prevcandle is None or self.prevcandle != candle:
                #   logDebugToFile(f"Checking buy condition for {self.pair} w/ {candle}")
                self.buy = self.STRATEGY.checkBuy(candle)

                if self.buy:
                    self.buyPrice, self.buyTime = self.calcWithFee(candle['close']), candle['timestamp']
                    self.totalFees.append(self.fee* candle['close'])
                    self.quantity = self.principle / self.buyPrice
                    print(f"Buying @ {candle['close']}")
                    if self.type is not SessionType.BACKTEST:
                        typ = "[PAPERTRADE]" if self.type is SessionType.PAPERTRADE else "[LIVETRADE]"
                        logToSlack(f"{typ} Buying for [{self.stratString}]{self.pair.value} at price: {self.buyPrice}", channel=Channel.PAPERTRADER)
                        return True



        else: #is bought

            self.principle = self.calcWithFee(candle['close']) * self.quantity
            self.principleOverTime.append(self.principle)
            if update is True:
                self.STRATEGY.checkBuy(candle)

            self.takeProfit = float(self.buyPrice) * self.takeProfitPercent

            if self.CHECK_STOPLOSS(candle) or self.STRATEGY.checkSell(candle):
                self.sell = True
                self.sellPrice, self.sellTime = self.calcWithFee(float(candle['close'])), candle['timestamp']
                self.totalFees.append(self.fee * float(candle['close']))

            if self.sell:
                self.calcPL()
                if self.type is not SessionType.BACKTEST:
                    logToSlack(f"TRADE COMPLETE\nResults:\n{self.toString()}", channel=Channel.PAPERTRADER)

                else:
                    print(colored("--------------------------\n" + self.toString() + "--------------------------",
                              'green') if self.profitLoss > 0 else colored(
                    "--------------------------\n" + self.toString() + "--------------------------", 'red')) 
                self.profitlosses.append(self.profitLoss)
                self.reset()
                if self.type is SessionType.PAPERTRADE:
                    #write new transaction to database
                    results = self.getResults()["tradeResults"]
                    self.writer.writeTransactionData(results, self.sessionid)


                return False

        self.prevcandle = candle
        return True
    def getTotalTrades(self) -> int:
        """
        @:returns count of total trades
        """
        return len(self.profitlosses)

    def getResults(self) -> dict:
        """
        @:returns results in a dictionary that hold buytime, buyprice, selltime, sellprice, profitloss
        """
        return {
            "pair": self.pair.value,
            "tradeResults": self.results
        }
