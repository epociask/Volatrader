from Trader.TradeSession import TradeSession 
import numpy as np 

class Math():
    def __init__(self, session):
        self.portfolio_return = session.getTakeProfitPercent()/100
        self.risk_free_rate = 0 #3 month US Treasury bill's interest rate used by most US traders (SUGGESTION TO USE IEF INSTEAD)
        self.stock_return_dict = session.getResults()
        self.length = session.getTotalTrades()

    # Sharpe ratio is a proxy of total portfolio risk often used to compare the change in overall risk-return characteristics when a new asset or asset class is added to a portfolio
    def Sharpe_Ratio(self):
        standard_deviation = self.Standard_Deviation()
        return((self.portfolio_return - self.risk_free_rate)/standard_deviation)
    #Less than 1: Bad
    #1 – 1.99: Adequate/good
    #2 – 2.99: Very good
    #Greater than 3: Excellent

    #Limitations
    # It assumes that returns are normally distributed (like rolling dices should eventually give a bell curve). However, financial markets are skewed away from the average due to surprising drops and spikes.
    # Our Sharpe Ratio can be adjusted lengthening the measurement interval, which would lower the estimate of volatility.
    # Also we could choose a period with the best potetential rather than a neutral look-back period

    #Standard deviation used to help minimize your risk and still maximize returns. It measures how much the investment returns deviate from the mean of the probability distribution of investments
    def Standard_Deviation(self):
        standard_deviation = np.sqrt(self.Variance())
        return standard_deviation

    # def Standard_Deviation(self, return_list):
    #     standard_deviation = np.sqrt(Variance(return_list))
    #     return standard_deviation

    #Expected return measures the mean or expected value of probability distribution of investment returns. COULD BE GOOD TO IMPLEMENT LATER.
    #Doesn't take risk into account and is based largely on historic data

    #Variance measures variability from the average. The variance statistic can help determine the risk when purchasing a specific security.
    def Variance(self):
        return_dict = self.stock_return_dict["tradeResults"]
        return_list = return_dict["profitloss"]
        average_return = 0
        variance = 0
        for i in range(return_list):
            average_return += return_list[i]
        average_return = average_return/self.length
        for i in range(return_list):
            variance += (return_list[i] - average_return)**2
        variance = variance/self.length
        return variance

        # def Variance(self, return_list):
        #     average_return = 0
        #     variance = 0
        #     for i in range(return_list):
        #         average_return += return_list[i]
        #     average_return = average_return/len(return_list)
        #     for i in range(return_list):
        #         variance += (return_list[i] - average_return)**2
        #     variance = variance/len(return_list)
        #     return variance

    #Rolling sharpe ratio provides a continually-updated, albeit rearward-looking, view of current reward-to-risk. Should help us identify strategy decay over time.
    def Rolling_Sharpe_Ratio(self):
        #In order to calculate an annualised rolling Sharpe ratio it is necessary to make two modifications to this formula. The first is to reduce the set of returns to the last trailing number of annualised trading periods (e.g. for daily data this means take the last 252 close-to-close returns)
        #Multiply the value by the square root of the number of annual trading periods. For strategies trading on a daily timeframe the number of periods is equal to 252, the (approximate) number of trading days in the US
        trading_period = np.sqrt(252) #252 trading periods over a year
        sharpe_ratio = Sharpe_Ratio()
        return(trading_period * sharpe_ratio)
    
    def Rolling_Sharpe_Ratio(self, period):
        trading_period = np.sqrt(period)
        sharpe_ratio = Sharpe_Ratio()
        return(trading_period * sharpe_ratio)

    #Sortino ratio is based off the Sharpe Ratio and differentiates harmful volatility from total overall volatility by using the asset's standard deviation of negative portfolio returns, called downside deviation, instead of the total standard deviation of portfolio returns.
    def Sortino_Ratio(self):
        negative_return_list = []
        return_dict = self.stock_return_dict["tradeResults"]
        return_list = return_dict["profitloss"]
        for i in range(return_list):
            if(return_list[i] < 0):
                negative_return_list.append(self.stock_return_dict[i])
        downside_deviation = Standard_Deviation(negative_return_list) #focus on only the negative returns
        return((self.portfolio_return - self.risk_free_rate)/downside_deviation)
    
    def Sortino_Ratio(self, return_list):
        negative_return_list = []
        for i in range(return_list):
            if(return_list[i] < 0):
                negative_return_list.append(return_list[i])
        downside_deviation = Standard_Deviation(negative_return_list) #focus on only the negative returns
        return((self.portfolio_return - self.risk_free_rate)/downside_deviation)
    
    #Higher number is better, similar to Sharpe ratio.
    #The Sortino ratio improves upon the Sharpe ratio by isolating downside or negative volatility from total volatility by dividing excess return by the downside deviation instead of the total standard deviation of a portfolio or asset.

    #Just as the Sortino ratio is modelled after the Sharpe Ratio, I wrote the equivalent using the Rolling Sharpe Ratio as my base and creating the Rolling Sortino Ratio. This probably has been done before, so I will research it, see if its viable, and update this portion. 
    def Rolling_Sortino_Ratio(self):
        trading_period = np.sqrt(252) #252 trading periods over a year
        sortino_ratio = Sortino_Ratio()
        return(trading_period * sortino_ratio)
    
    def Rolling_Sortino_Ratio(self, period):
        trading_period = np.sqrt(period)
        sortino_ratio = Sortino_Ratio()
        return(trading_period * sortino_ratio)


    #Treynor ratio is based off the Sharpe Ratio and compares the risk of our portfolio to the risk of the market. Should allow us to determine reward-to-volatility ratio.
    def Treynor_Ratio(self, market_return_list):
        beta = Beta(self.stock_return_list, market_return_list)
        return((self.portfolio_return - self.risk_free_return)/beta)
    #A main weakness of the Treynor ratio is its backward-looking nature. Investments are likely to perform and behave differently in the future than they did in the past. The accuracy of the Treynor ratio is highly dependent on the use of appropriate benchmarks to measure beta.
    #When comparing similar investments, the higher Treynor ratio is better, all else equal, but there is no definition of how much better it is than the other investments.

    #Beta is a measure of the volitility of a portfolio compared to the market
    def Beta(self, market_return_list):
        covariance = "Covariance(self.stock_return_list, market_return_list)"
        return(covariance/Variance(market_return_list))
    #Using beta to evaluate a stock will also need to evaluate it from other perspectives—such as fundamental or technical factors—before assuming it will add or remove risk from a portfolio.

    #Covariance. AKA FUCK THIS ILL DO THIS SHIT LATER
    def Covariance(self, return_list, return_list2):
        covariance
        return covariance