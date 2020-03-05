from Instance import Instance

#Base template for how to write a strat
class Session:

    def __init__(self, pair):
        self.pair = pair
        self.sellStrat = Instance(pair)
        self.sellStrat.setStopLossPercent(1)
        self.profitlosses = []
        self.buy = False
        self.buyPrice = 0
        self.takeProfit = 0
        self.sellPrice = 0
        self.ProfitLoss = None
        self.sell = False

    def reset(self):
        self.sellStrat.reset()
        self.buy = False
        self.buyPrice = 0
        self.sellPrice = 0
        self.ProfitLoss = None
        self.sell = False

    def calcPL(self):

        self.profitLoss = (100 - (100 * (self.buyPrice / self.sellPrice))) if self.sellPrice > self.buyPrice else -(100 - (100 * (self.sellPrice / self.buyPrice)))

    # ToString method
    def toString(self):

        return "Buy Price {} time: {}\nSell Price {} time: {}\nProfit Loss {}\n".format(self.buyPrice, self.buyTime,
                                                                                        self.sellPrice, self.sellTime,
                                                                                        self.profitLoss)

    def buyStrat(self, data):
        print("Checking buy start")
        print(data['threeoutside']['value'])
        if data['threeoutside']['value'] != '0':
            print("Buying")
            self.buyPrice = float(data['candle']['close'])
            self.buyTime = data['candle']['timestamp']
            self.takeProfit = float(self.buyPrice) * 1.02

            return True

        return False

    # returns total profit-loss percentage after running strategy
    def getTotalPL(self):

        return sum(self.profitlosses)

    def checkForSell(self, data):
        print("Checking sell:::::::current price", data['candle']['close'])
        if self.sellStrat.run(float(data['candle']['close'])) or self.takeProfit <= float(data['candle']['close']):
            self.sellPrice = float(data['candle']['close'])
            self.sellTime = data['candle']['timestamp']
            return True

        return False

    def update(self, data):
        print("Checking for ", data)

        if not self.buy:
            self.buy = self.buyStrat(data)
            print("Take profit price: ", self.takeProfit)

        else:
            self.sell = self.checkForSell(data)

            if self.sell:
                self.calcPL()
                print(self.toString())
                self.profitlosses.append(self.profitLoss)
                self.reset()

