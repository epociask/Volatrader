from termcolor import colored
from BackTesterSellLogic import Instance


'''
Class to hold buying and selling logic 
'''
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
    '''
    @returns # of winning and # of losing trades
    '''
    def getTradeData(self) -> (int, int):
        return str(self.positiveTrades), str(self.NegativeTrades)
    '''
    Adds trade result to results list
    updates winning and losing trade counts
    '''
    def addResult(self) -> None:
        self.results.append({'buytime': self.buyTime, 'buyprice': self.buyPrice, 'selltime': self.sellTime,
                             'sellprice': self.sellPrice, 'profitloss': self.profitLoss})
        if self.profitLoss > 0:
            self.positiveTrades += 1
        else:
            self.NegativeTrades += 1
    '''
    resets after selling 
    '''
    def reset(self) -> None:
        self.addResult()
        self.sellStrat.reset()
        self.buy = False
        self.buyPrice = 0
        self.sellPrice = 0
        self.profitLoss = None
        self.sell = False

    '''
    Calculate profit loss function
    '''
    def calcPL(self) -> None:

        self.profitLoss = (100 - (100 * (self.buyPrice / self.sellPrice))) if self.sellPrice > self.buyPrice else -(
                    100 - (100 * (self.sellPrice / self.buyPrice)))
    '''
    ToString method
    '''
    def toString(self) -> str:

        return "Buy Price {} time: {}\nSell Price {} time: {}\nProfit Loss {}\n".format(self.buyPrice, self.buyTime,
                                                                                        self.sellPrice, self.sellTime,
                                                                                        self.profitLoss)
    '''
    returns total profit-loss percentage after running strategy
    '''
    def getTotalPL(self):

        return sum(self.profitlosses)

    '''
    Uses sell logic instance to see if it's time to sell 
    '''
    def checkForSell(self, data):
        # print("Checking sell:::::::current price", data['candle']['close'])
        if self.sellStrat.run(float(data['candle']['close'])) or self.takeProfit <= float(data['candle']['close']):
            self.sellPrice = float(data['candle']['close'])
            self.sellTime = data['candle']['timestamp']
            return True

        return False

    '''
    main function
    @param data takes in and makes buy/sell, do-nothing decisions accordingly 
    '''
    def update(self, data) -> None:
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

    '''
    @returns count of total trades 
    '''
    def getTotalTrades(self) -> int:
        return len(self.profitlosses)

    '''
    @returns results in a dictionary 
    '''
    def getResults(self) -> dict:
        return {
            "pair": self.pair.value,
            "tradeResults": self.results
        }
