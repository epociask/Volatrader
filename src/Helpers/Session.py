import time
from termcolor import colored
from BackTest.BackTesterSellLogic import Instance
from Helpers.Enums import *
from Helpers.Logger import logDebugToFile, logToSlack, Channel
from Helpers.HelpfulOperators import getCurrentBinancePrice

class Session:
    """
    Class to hold buying and selling logic and execute each accordingly to price updates
    """

    def __init__(self, pair, buyStrategy, takeProfitPercent, percentSL, stratString: str, sessionType: Enum):
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
        self.buyStrat = buyStrategy
        self.takeProfitPercent = float(f"1.{takeProfitPercent}")
        self.results = []
        self.positiveTrades = 0
        self.NegativeTrades = 0
        self.type = sessionType
        self.prevData = None

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
        return str(self.positiveTrades), str(self.NegativeTrades)

    def addResult(self) -> None:
        """
        Adds trade result to results list
        updates winning and losing trade counts
        @:returns None
        """

        self.results.append({'buytime': self.buyTime, 'buyprice': self.buyPrice, 'selltime': self.sellTime,
                             'sellprice': self.sellPrice, 'profitloss': self.profitLoss})
        if self.profitLoss > 0:
            self.positiveTrades += 1
        else:
            self.NegativeTrades += 1

    def reset(self) -> None:
        """
        reset function to reset class members after selling
        """
        logToFile(f"Resetting for {self.pair}")
        self.addResult()
        self.sellStrat.reset()
        self.buy = False
        self.buyPrice = 0
        self.sellPrice = 0
        self.profitLoss = None
        self.sell = False

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

        return "Buy Price {} time: {}\nSell Price {} time: {}\nProfit Loss {}\n".format(self.buyPrice, self.buyTime,
                                                                                        self.sellPrice, self.sellTime,
                                                                                        self.profitLoss)

    def getTotalPL(self):
        """
        @:returns total profit-loss percentage after running strategy
        """

        return sum(self.profitlosses)

    def checkForBackTestSell(self, data):
        """
        Uses sell logic instance to see if it's time to sell
        @:returns boolean
        """
        logDebugToFile("Checking sell")
        if self.sellStrat.run(float(data['candle']['close'])) or self.takeProfit <= float(data['candle']['close']):
            self.sellPrice = float(data['candle']['close'])
            self.sellTime = data['candle']['timestamp']
            return True

        return False


    def update(self, data, update=False) -> bool:
        """
        main function
        @:param data
        takes in @:param data and makes buy/sell or do-nothing decisions accordingly
        @:returns None
        """
        if not self.buy:    #not bought 

            if self.prevData is None or self.prevData != data:
                logDebugToFile(f"Checking buy condition for {self.pair}")
                self.buy = self.buyStrat.update(data)
                
                if self.buy:
                    self.buyPrice, self.buyTime = data['candle']['close'], data['candle']['timestamp']

                    if self.type is not SessionType.BACKTEST:
                        typ = "[PAPERTRADE]" if self.type is SessionType.PAPERTRADE else "[LIVETRADE]"
                        logToSlack(f"{typ} Buying for [{self.stratString}]{self.pair.value} at price: {self.buyPrice}", channel=Channel.PAPERTRADER)
                        return False
                


        else: #is bought 

            if update is True:
                self.buyStrat.update(data)

            else:
                self.takeProfit = float(self.buyPrice) * self.takeProfitPercent
                self.sell = self.checkForBackTestSell(data)
            if self.sell:
                self.calcPL()
                logToSlack(colored("--------------------------\n" + self.toString() + "--------------------------",
                              'green') if self.profitLoss > 0 else colored(
                    "--------------------------\n" + self.toString() + "--------------------------", 'red')) if self.type != SessionType.BACKTEST else print(colored("--------------------------\n" + self.toString() + "--------------------------",
                              'green') if self.profitLoss > 0 else colored(
                    "--------------------------\n" + self.toString() + "--------------------------", 'red'))
                self.profitlosses.append(self.profitLoss)
                self.reset()

        self.prevData = data
        return True
    def getTotalTrades(self) -> int:
        """
        @:returns count of total trades
        """
        return len(self.profitlosses)

    def getResults(self) -> dict:
        """
        @:returns results in a dictionary
        """

        return {
            "pair": self.pair.value,
            "tradeResults": self.results
        }
