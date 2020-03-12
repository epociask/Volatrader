import ccxt
from src.authent import getPortfolio
from src.authent import getCurrentPrice
from src.authent import sell


class Instance:

    def __init__(self, base, quantity):
        # Global variables
        self.pair: str = base + "/USDT" if base != 'BTC' else 'BTC/USDT'
        print(self.pair)
        self.quantity: float = 0
        self.percentStopLoss: float = 0  # PercentSL...input by user : DEFAULT 0
        self.globalHigh: float = 0  # global high ..ie highest value found in session : DEFAULT 0
        self.currentPrice: float = 0  # current price... obtained by CCXT API : DEFAULT 0
        self.lastPrice: float = 0  # last given price... updated in function call : DEFAULT 0
        self.slVal: float = 0  # Value that program will sell upon
        self.shouldSell = False  # boolean to tell whether sell should be made or not
        self.slValFunc = lambda price: float((  price * float(".{}".format(100 - self.percentStopLoss))))


    def drive(self) -> (None, Exception):
        print(type(self.globalHigh))
        print(type(self.currentPrice))
        print(type(self.slVal))
        if self.currentPrice > self.globalHigh or self.slVal == 0:
            self.slVal = self.slValFunc(self.globalHigh)

    def setStopLossPercent(self, p):
        self.percentStopLoss = p

    def toString(self):
        return str(
            self.pair + "\n" + "Current price :" + str(self.currentPrice) + "\n" + "Global high :" + str(
                self.globalHigh) + "\n" + "Stoploss value :" + str(self.slVal) + "\n" + "Stoploss percent :" + str(
                self.percentStopLoss) + "\n")

    def run(self, price):
        if type(price) != float:
            raise TypeError("Wrong parameter.... expecting float")
        self.currentPrice = price
        self.lastPrice = self.currentPrice
        if self.globalHigh == 0 or self.currentPrice > self.globalHigh:
            print("setting global high")
            self.globalHigh = price
        self.shouldSell = self.checkForSell()
        self.drive()

    # @returns True if sell is to be made // false otherwise
    def checkForSell(self) -> bool:
        return True if self.currentPrice <= self.slVal else False


class Session:

    def __init__(self, exchange: ccxt.Exchange):
        self.API = exchange  # CCXT wrapper to access remote  data and perform remote operations
        self.portfolio = getPortfolio(self.API)
        self.instances = []

    def initializeSession(self) -> None:

        for crypto in self.portfolio:
            temp = Instance(crypto, self.portfolio[crypto])
            temp.setStopLossPercent(int(input("What percent stop loss would you like on {}?  \n".format(crypto))))
            self.instances.append(temp)

    def run(self):
        for instance in self.instances:

            try:
                price = getCurrentPrice(instance.pair, self.API)
                print(price)
                instance.setCurrentPrice(price)
            except Exception as e:
                print("Error", e)
            if instance.shouldSell:
                sell(instance.pair, self.API, self.portfolio)


            print(instance.toString())
