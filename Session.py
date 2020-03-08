from termcolor import colored
from Instance import Instance


# Base template for how to write a strat
class Session:

    def __init__(self, pair, buyStrategy, takeProfitPercent, percentSL):
        self.pair = pair
        self.sellStrat = Instance(pair)
        self.sellStrat.setStopLossPercent(percentSL)
        self.profitlosses = []
        self.buy = False
        self.buyPrice = 0
        self.takeProfit = 0
        self.sellPrice = 0
        self.profitLoss = None
        self.sell = False
        self.buyStrat = buyStrategy
        self.takeProfitPercent = float(f"1.{takeProfitPercent}")
        self.results = []
        self.positiveTrades = 0
        self.NegativeTrades = 0

    def getTradeData(self):
        return str(self.positiveTrades), str(self.NegativeTrades)

    def addResult(self):
        self.results.append({'buytime': self.buyTime, 'buyprice': self.buyPrice, 'selltime': self.sellTime,
                             'sellprice': self.sellPrice, 'profitloss': self.profitLoss})
        if self.profitLoss > 0:
            self.positiveTrades += 1
        else:
            self.NegativeTrades += 1

    def reset(self):
        self.addResult()
        self.sellStrat.reset()
        self.buy = False
        self.buyPrice = 0
        self.sellPrice = 0
        self.profitLoss = None
        self.sell = False

    def calcPL(self):

        self.profitLoss = (100 - (100 * (self.buyPrice / self.sellPrice))) if self.sellPrice > self.buyPrice else -(
                    100 - (100 * (self.sellPrice / self.buyPrice)))

    # ToString method
    def toString(self):

        return "Buy Price {} time: {}\nSell Price {} time: {}\nProfit Loss {}\n".format(self.buyPrice, self.buyTime,
                                                                                        self.sellPrice, self.sellTime,
                                                                                        self.profitLoss)

    # returns total profit-loss percentage after running strategy
    def getTotalPL(self):

        return sum(self.profitlosses)

    def checkForSell(self, data):
        # print("Checking sell:::::::current price", data['candle']['close'])
        if self.sellStrat.run(float(data['candle']['close'])) or self.takeProfit <= float(data['candle']['close']):
            self.sellPrice = float(data['candle']['close'])
            self.sellTime = data['candle']['timestamp']
            return True

        return False

    def update(self, data):
        # print("Checking for ", data)

        if not self.buy:
            self.buy, self.buyTime, self.buyPrice = self.buyStrat(data)


        else:
            self.takeProfit = float(self.buyPrice) * self.takeProfitPercent
            self.sell = self.checkForSell(data)

            if self.sell:
                self.calcPL()
                print(colored("--------------------------\n" + self.toString() + "--------------------------",
                              'green') if self.profitLoss > 0 else colored(
                    "--------------------------\n" + self.toString() + "--------------------------", 'red'))
                self.profitlosses.append(self.profitLoss)
                self.reset()

    def getTotalTrades(self):
        return len(self.profitlosses)

    def getResults(self):
        return {
            "pair": self.pair.value,
            "tradeResults": self.results
        }
