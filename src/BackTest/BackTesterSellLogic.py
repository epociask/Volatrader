"""
Holds backtest sell logic as Instance class
Uses trailing stop loss strategy
"""


class Instance:

    def __init__(self, base):
        # Global variables
        self.pair: str = base
        self.percentStopLoss: float = 0  # PercentSL...input by user : DEFAULT 0
        self.globalHigh: float = 0  # global high ..ie highest value found in session : DEFAULT 0
        self.currentPrice: float = 0  # current price... obtained by CCXT API : DEFAULT 0
        self.lastPrice: float = 0  # last given price... updated in function call : DEFAULT 0
        self.slVal: float = 0  # Value that program will sell upon
        self.sold = False  # boolean to tell whether sell should be made or not
        self.slValFunc = lambda price: float((float(price) * float(".{}".format(100 - self.percentStopLoss))))

    def drive(self) -> (None, Exception):
        """
          Checks if SL should be calculated
        """
        self.slVal = self.slValFunc(float(self.globalHigh))

    def setStopLossPercent(self, p) -> None:
        """"
            Sets percentage stop loss in class
            @param percentage stop loss
        """
        self.percentStopLoss = p


    def reset(self) -> None:
        """
        Resets values after sell is made
        """
        self.globalHigh: float = 0  # global high ..ie highest value found in session : DEFAULT 0
        self.currentPrice: float = 0  # current price... obtained by CCXT API : DEFAULT 0
        self.lastPrice: float = 0  # last given price... updated in function call : DEFAULT 0
        self.slVal: float = 0  # Value that program will sell upon



    def toString(self) -> str:
        """
        toString method
        """
        return str(
            self.pair.value + "\n" + "Current price :" + str(self.currentPrice) + "\n" + "Global high :" + str(
                self.globalHigh) + "\n" + "Stoploss value :" + str(self.slVal) + "\n" + "Stoploss percent :" + str(
                self.percentStopLoss) + "\n")

    def run(self, price) -> bool:
        """
        @:param price
        @:returns True/False based on percentageSL
        """
        #print(self.toString())
        if type(price) != float:
            raise TypeError("Wrong parameter.... expecting float")
        self.currentPrice = price
        self.lastPrice = self.currentPrice
        if self.globalHigh == 0 or self.currentPrice > self.globalHigh:
            self.globalHigh = price
        self.drive()
        return self.checkForSell()

    def checkForSell(self) -> bool:
        """
        @:returns True if sell is to be made // false otherwise
        """
        if self.currentPrice <= self.slVal:
            self.reset()
            return True

        return False
