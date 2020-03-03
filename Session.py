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
        self.sellStrat = Instance(self.pair)
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

    def buyStrat(self, candle):
        if not self.sell:
            print("Buying")
            self.buyPrice = float(candle['close'])
            self.buyTime = candle['timestamp']
            return True

        return False

    # returns total profit-loss percentage after running strategy
    def getTotalPL(self):

        return sum(self.profitlosses)

    def checkForSell(self, candle):
        if self.sellStrat.run(float(candle['close'])) or self.takeProfit <= float(candle['close']):
            print("Checking sell")
            self.sellPrice = float(candle['close'])
            self.sellTime = candle['timestamp']
            return True

        return False

    def update(self, candle):

        if not self.buy:
            self.buy = self.buyStrat(candle)
            self.takeProfit = float(self.buyPrice) * 1.08
            print("Take profit price: ", self.takeProfit)

        else:
            self.sell = self.checkForSell(candle)

            if self.sell:
                self.calcPL()
                print(self.toString())
                self.profitlosses.append(self.profitLoss)
                self.reset()

