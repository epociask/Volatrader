import time
from termcolor import colored
from Trader.SellLogic import Instance
from Helpers.Constants.Enums import *
from Helpers.Logger import logDebugToFile, logToSlack, Channel
from Helpers.API.MarketFunctions  import getCurrentBinancePrice
import ccxt
from Helpers.TimeHelpers import convertNumericTimeToString

class TradeSession:
    """
    Class to hold buying and selling logic and execute each accordingly to price updates
    """

    def __init__(self, pair, buyStrategy, takeProfitPercent, percentSL, stratString: str, sessionType: Enum, principle= 1000):
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
        self.prevData = None
        self.fee = .1/100
        self.calcWithFee = lambda price: price * float(1 - self.fee)
        self.totalFees = []
        self.principle = principle
        self.principleOverTime = []

    
    def getTotalFees(self):
        return sum(self.totalFees)


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

        self.results.append({'buytime': convertNumericTimeToString(self.buyTime), 'buyprice': self.buyPrice, 'selltime': convertNumericTimeToString(self.sellTime),
                             'sellprice': self.sellPrice, 'profitloss': self.profitLoss})
        if self.profitLoss > 0:
            self.positiveTrades += 1
        else:
            self.NegativeTrades += 1

    def reset(self) -> None:
        """
        reset function to reset class members after selling
        """
        logDebugToFile(f"Resetting for {self.pair}")

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

        return "Buy Price {} time: {}\nSell Price {} time: {}\nProfit Loss {}\n".format(self.buyPrice, self.buyTime,
                                                                                        self.sellPrice, self.sellTime,
                                                                                        self.profitLoss)

    def getTotalPL(self):
        """
        @:returns total profit-loss percentage after running strategy
        """

        return sum(self.profitlosses)

    def CHECK_STOPLOSS(self, data):
        """
        Uses sell logic instance to see if it's time to sell
        @:returns boolean
        """
        logDebugToFile("Checking sell")
        if self.sellStrat.run(float(data['candle']['close'])) or self.takeProfit <= float(data['candle']['close']):
    
            return True

        return False


    def update(self, data, update=True) -> bool:
        """
        main function
        @:param data
        takes in @:param data and makes buy/sell or do-nothing decisions accordingly
        @:returns None
        """
        if not self.buy:    #not bought 
            
            self.principleOverTime.append(self.principle)

            if self.prevData is None or self.prevData != data:
                logDebugToFile(f"Checking buy condition for {self.pair} w/ {data}")
                self.buy = self.STRATEGY.checkBuy(data)
                
                if self.buy:
                    self.buyPrice, self.buyTime = self.calcWithFee(data['candle']['close']), data['candle']['timestamp']
                    self.totalFees.append(self.fee* data['candle']['close'])
                    self.quantity = self.principle / self.buyPrice 

                    if self.type is not SessionType.BACKTEST:
                        print(f"Buying @ {data['candle']['close']}")
                        typ = "[PAPERTRADE]" if self.type is SessionType.PAPERTRADE else "[LIVETRADE]"
                        logToSlack(f"{typ} Buying for [{self.stratString}]{self.pair.value} at price: {self.buyPrice}", channel=Channel.PAPERTRADER)

                        return True
                


        else: #is bought 

            self.principle = data['candle']['close'] * self.quantity
            self.principleOverTime.append(self.principle)
            if update is True:
                self.STRATEGY.checkBuy(data)

            if update is True and self.type is SessionType.BACKTEST:
                self.takeProfit = float(self.buyPrice) * self.takeProfitPercent

                if self.CHECK_STOPLOSS(data) or self.STRATEGY.checkSell(data):
                    self.sell = True 
                    self.sellPrice = self.calcWithFee(float(data['candle']['close']))
                    self.sellTime = data['candle']['timestamp']
            if self.sell:
                self.calcPL()
                logToSlack(colored("--------------------------\n" + self.toString() + "--------------------------",
                              'green') if self.profitLoss > 0 else colored(
                    "--------------------------\n" + self.toString() + "--------------------------", 'red')) if self.type != SessionType.BACKTEST else print(colored("--------------------------\n" + self.toString() + "--------------------------",
                              'green') if self.profitLoss > 0 else colored(
                    "--------------------------\n" + self.toString() + "--------------------------", 'red'))
                self.profitlosses.append(self.profitLoss)
                self.reset()
                return False

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
