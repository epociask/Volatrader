import numpy as np
import random
import math
import quandl
quandl.ApiConfig.api_key = "Uc2MWXi4sBSEKd8185Px"

# 252 trading periods over a year

# risk free rate is 3 month US Treasury bill's interest rate used by most US traders (SUGGESTION TO USE IEF INSTEAD)






"NEED NEW UP TO DATE DATA ON EVERYTHING BELOW. THIS SHIT'S NOT UP TO DATE AND THUSLY TRASH"
rfr = quandl.get("USTREASURY/BILLRATES", returns="numpy")
rf = rfr[0]
risk_free_rate = rf[5]
unemployment_list = quandl.get("FRED/NROUST", rows = 1, returns = "numpy")
unemployment_threshold = unemployment_list.mean()
short_term_unemployment = unemployment_list[0]
gdp_list = quandl.get("FED/FU087005086_Q", rows = 1, returns = "numpy")
gdp_threshold = gdp_list.mean()
gross_domestic_product = gdp_list[0]
CPI_list = quandl.get("BLSI/CUSR0000SA0", rows = 1, returns = "numpy")
"NEED NEW UP TO DATE DATA. THIS SHIT'S NOT UP TO DATE AND THUSLY TRASH"








#quandl Rate Limits:
#Authenticated users have a limit of 300 calls per 10 seconds, 2,000 calls per 10 minutes and a limit of 50,000 calls per day.
#Authenticated users of free datasets have a concurrency limit of one; that is, they can make one call at a time and have an additional call in the queue.
#Premium data subscribers have a limit of 5,000 calls per 10 minutes and a limit of 720,000 calls per day.


# Sharpe ratio is a proxy of total portfolio risk often used to compare the change in overall risk-return characteristics when a new asset or asset class is added to a portfolio

def Sharpe_Ratio(return_list): #percentage profit loss
    return (Mean(return_list) - risk_free_rate) / Standard_Deviation(return_list)

# Less than 1: Bad
# 1 – 1.99: Adequate/good
# 2 – 2.99: Very good
# Greater than 3: Excellent

# Limitations
# It assumes that returns are normally distributed (like rolling dices should eventually give a bell curve). However, financial markets are skewed away from the average due to surprising drops and spikes.
# Our Sharpe Ratio can be adjusted lengthening the measurement interval, which would lower the estimate of volatility.
# Also we could choose a period with the best potetential rather than a neutral look-back period

# Standard deviation used to help minimize your risk and still maximize returns. It measures how much the investment returns deviate from the mean of the probability distribution of investments

def Standard_Deviation(return_list):
    return math.sqrt(Variance(return_list))

# Expected return measures the mean or expected value of probability distribution of investment returns. COULD BE GOOD TO IMPLEMENT LATER.
# Doesn't take risk into account and is based largely on historic data

# Variance measures variability from the average. The variance statistic can help determine the risk when purchasing a specific security.

def Variance(return_list):
    average_return = Mean(return_list)
    variance_list = [(x-average_return)**2 for x in return_list]
    return sum(variance_list) / len(variance_list)

# Rolling sharpe ratio provides a continually-updated, albeit rearward-looking, view of current reward-to-risk. Should help us identify strategy decay over time.

def Rolling_Sharpe_Ratio(return_list, period):
    # In order to calculate an annualised rolling Sharpe ratio it is necessary to make two modifications to this formula. The first is to reduce the set of returns to the last trailing number of annualised trading periods (e.g. for daily data this means take the last 252 close-to-close returns)
    # Multiply the value by the square root of the number of annual trading periods. For strategies trading on a daily timeframe the number of periods is equal to 252, the (approximate) number of trading days in the US
    new_return_list = return_list[(len(return_list) - period):len(return_list)]  # truncates list from all profits to the last n profits
    return math.sqrt(period) * Sharpe_Ratio(new_return_list)

# Sortino ratio is based off the Sharpe Ratio and differentiates harmful volatility from total overall volatility by using the asset's standard deviation of negative portfolio returns, called downside deviation, instead of the total standard deviation of portfolio returns.

def Sortino_Ratio(return_list):
    negative_return_list = [x for x in return_list if x < 0]
    if(len(negative_return_list) != 0):
        return (Mean(return_list) - risk_free_rate) / Standard_Deviation(negative_return_list)  # focus on only the negative returns
    raise Exception("No observed downside. Use Sharpe Ratio instead")

# Higher number is better, similar to Sharpe ratio.
# The Sortino ratio improves upon the Sharpe ratio by isolating downside or negative volatility from total volatility by dividing excess return by the downside deviation instead of the total standard deviation of a portfolio or asset.

# Just as the Sortino ratio is modelled after the Sharpe Ratio, I wrote the equivalent using the Rolling Sharpe Ratio as my base and creating the Rolling Sortino Ratio. This probably has been done before, so I will research it, see if its viable, and update this portion.

def Rolling_Sortino_Ratio(return_list, period):
    new_return_list = return_list[(len(return_list) - period):len(return_list)]
    return math.sqrt(period) * Sortino_Ratio(new_return_list)

# Treynor ratio is based off the Sharpe Ratio and compares the risk of our portfolio to the risk of the market. Should allow us to determine reward-to-volatility ratio.
def Treynor_Ratio(stock_return_list, market_return_list, period):
    new_return_list = stock_return_list[(len(stock_return_list) - period):len(stock_return_list)]
    new_market_list = market_return_list[(len(market_return_list) - period):len(market_return_list)]
    return (Mean(new_return_list) - risk_free_rate) / Beta(new_return_list, new_market_list)

#For negative values of Beta, the Ratio does not give meaningful values.
#When comparing two portfolios, the Ratio does not indicate the significance of the difference of the values, as they are ordinal. For example, a Treynor Ratio of 0.5 is better than one of 0.25, but not necessarily twice as good.
#The numerator is the excess return to the risk-free rate. The denominator is the Beta of the portfolio, or, in other words, a measure of its systematic risk.

# A main weakness of the Treynor ratio is its backward-looking nature. Investments are likely to perform and behave differently in the future than they did in the past. The accuracy of the Treynor ratio is highly dependent on the use of appropriate benchmarks to measure beta.
# When comparing similar investments, the higher Treynor ratio is better, all else equal, but there is no definition of how much better it is than the other investments.


# Beta is a measure of the volitility of a portfolio compared to the market
def Beta(stock_return_list, market_return_list):
    return Covariance(stock_return_list, market_return_list) / Variance(market_return_list)

# Using beta to evaluate a stock will also need to evaluate it from other perspectives—such as fundamental or technical factors—before assuming it will add or remove risk from a portfolio.

# Covariance.
def Covariance(return_list, return_list2):
    xm = Mean(return_list)
    ym = Mean(return_list2)
    covariance = 0
    n = len(return_list)
    for i in range(n):
        covariance += (return_list[i] - xm) * (return_list2[i] - ym)
    return  covariance/(n - 1)
    # https://www.investopedia.com/terms/c/covariance.asp

# For investors, high kurtosis of the return distribution implies that the investor will experience occasional extreme returns (either positive or negative), more extreme than the usual + or - three standard deviations from the mean that is predicted by the normal distribution of returns. This phenomenon is known as kurtosis risk.
def Kurtosis(return_list):
    average = Mean(return_list)
    x1_list = [(x-average)**2 for x in return_list]
    x2_list = [(x-average)**4 for x in return_list]
    x1 = sum(x1_list) / len(x1_list)
    x2 = sum(x2_list) / len(x2_list)
    return (x2 / (x1 ** 2)) - 3

# NEED MORE INFO ON WHICH FORMULA IS MORE ACCURATE
def Kurtosis2(return_list):
    length = len(return_list)
    average = Mean(return_list)
    x1_list = [(x-average)**2 for x in return_list]
    x2_list = [(x-average)**4 for x in return_list]
    x1 = sum(x1_list) / (length - 1)
    x2 = sum(x2_list) / length
    return ((length * (length + 1)) / ((length - 1)*(length - 2)*(length - 3)))*(x2 / (x1 ** 2)) - (3*((length - 1) ** 2 / (length - 2)*(length - 3)))

# kurtosis = (0 +- 3 * standard deviation). Normal risk
# kurtosis > (0 + 3 * standard deviation). High risk
# kurtosis < (0 - 3 * standard deviation). Less risk

#2 quarters of negative GDP growth is a Recession. BUY companies offering lower prices, vices such as alcohol (but not gambling!), and entertainment such as video games and netflix. Wait till Recession ends and put shit ton of money into the market and enjoy the upswing of recovery.
def isRecession():
    if (gdp_list[0] < 0 & gdp_list[1] < 0):
        return True
    else:
        return False

#Looks at GDP, unemployment, and inflation to determine strength of the economy 
def Economic_Strength():
    total = 0
    score = 100/3
    if(gross_domestic_product > 0):
        total += gross_domestic_product * score/2.5 #2-3% growth for a healthy economy
    if(short_term_unemployment >= 4 & short_term_unemployment <= 6):
        total += score #between 4% - 6% for a healthy economy
    """elif(short_term_unemployment < 4):
        total += score - (score/2 * (4-short_term_unemployment))""" #too little unemployment leads to inflation but that is covered now in CPI
    elif(short_term_unemployment > 6):
        total += score - (score/2 * (short_term_unemployment-6))
    CPI_growth = Percentage_Growth(CPI_list[0],CPI_list[1])
    if (CPI_growth < 3.5):
        total += score - (score/2 * (CPI_growth - 3.5)) # < 3.5% for a healthy economy
    elif(CPI_growth > 0):
        total += score
    return total
  

def Percentage_Growth(original, next_int):
    return (original - next_int)/(original*100)

# Average Returns. It can help measure the past performance of a security or the performance of a portfolio.
def Mean(return_list):
    # Average Return = Sum of Returns/Number of Returns
    return sum(return_list)/len(return_list)

#The simple average of returns is an easy calculation, but it is not very accurate. For more accurate returns calculations, analysts and investors also use frequently the geometric mean or money-weighted return.


#WIP
'''
class Market_Animal:
    def __init__(self):
        unemployment_list = quandl.get("FRED/NROUST", rows = 1, returns = "numpy")
        self.unemployment_threshold = unemployment_list.mean()
        self.short_term_unemployment = unemployment_list[0]
        gdp_list = quandl.get("FRED/GDPC1", rows = 1, returns = "numpy")
        self.gdp_threshold = gdp_list.mean()
        self.gross_domestic_product = gdp_list[0]
        self.data_set = [gross_domestic_product, short_term_unemployment]
    
    def getGDP(self):
        return self.gross_domestic_product
    
    def getGDPThreshold(self):
        return self.short_term_unemployment
    
    def getUnemployment(self):
        return self.gross_domestic_product
    
    def getUnemploymentThreshold(self):
        return self.unemployment_threshold

    def Bear_Bull(self):
        if(self.gross_domestic_product >= self.gdp_threshold & self.short_term_unemployment < self.unemployment_threshold):
            return "bullish"
        elif (self.gross_domestic_product < self.gdp_threshold & self.short_term_unemployment >= self.unemployment_threshold):
            return "bearish"
        else:
            return "unknown"
    
    #Fear and greed indicator: https://www.investopedia.com/terms/f/fear-and-greed-index.asp
    def Chicken_Pig(self): 
        return

    #Usually higher in bear markets
    def Volatility(self):
        return
'''






# Monte Carlo Simulation are used to model the probability of different outcomes in a process that cannot easily be predicted due to the intervention of random variables. It is a technique used to understand the impact of risk and uncertainty in prediction and forecasting models.
def Monte_Carlo(return_list):
    # Periodic Daily Return=ln( Previous Day’s Price/Day’s Price)
    # Drift=Average Daily Return − Variance/2
    # Random Value=σ×NORMSINV(RAND())
    # Next Day’s Price=Today’s Price×e**(Drift+Random Value)
    current_price = return_list[len(return_list) - 1]
    previous_price = return_list[len(return_list) - 2]
    periodic_return = math.log(current_price/previous_price)
    drift = Mean(return_list) - Variance(return_list) / 2
    random_value = Standard_Deviation(return_list) * ICND(random.randrange(0, 1))
    return current_price*math.exp(drift+random_value)
#Examines of the properties of estimators.

# Repeat this calculation the desired number of times (each repetition represents one day) to obtain a simulation of future price movement. By generating an arbitrary number of simulations, you can assess the probability that a security's price will follow given trajectory.
# The most likely return is at the middle of the curve, meaning there is an equal chance that the actual return will be higher or lower than that value. The probability that the actual return will be within one standard deviation of the most probable ("expected") rate is 68%; that it will be within two standard deviations is 95%; and that it will be within three standard deviations is 99.7%. Still, there is no guarantee that the most expected outcome will occur, or that actual movements will not exceed the wildest projections.
# Crucially, Monte Carlo simulations ignore everything that is not built into the price movement (macro trends, company leadership, hype, cyclical factors); in other words, they assume perfectly efficient markets. For example, the fact that Time Warner lowered its guidance for the year on November 4 is not reflected here, except in the price movement for that day, the last value in the data; if that fact were accounted for, the bulk of simulations would probably not predict a modest rise in price.

# I think this should be used in conjunction with fibonnaci arcs to get a better picture of the more "correct" predictions.

#Inverse Cumulative Normal Distribution(ICND)
def ICND(random_num):
    return random_num




#IDEAS


# Capital Asset Pricing Model (CAPM). The formula for calculating the expected return of an asset given its risk.
def CAPM(stock_return_list, market_return_list, expected_market_return):
    beta = Beta(stock_return_list, market_return_list)
    market_risk_premium = (expected_market_return) #Market_Risk_Premium()
    return risk_free_rate + (beta * market_risk_premium)

# Market risk premium can be calculated by subtracting the risk-free rate from the expected equity market return, providing a quantitative measure of the extra return demanded by market participants for increased risk. NEED MORE INFO.
def Market_Risk_Premium(expected_return):
    return expected_return - risk_free_rate

#Price-to-Earnings (P/E) Ratio
def Price_Earnings_Ratio(market_value, earnings, total_shares):
    return (market_value/total_shares)/(earnings/total_shares)
    #P/E ratio by dividing a company's market value per share by its earnings per share.

#Gives the growth or decline of a strategy over a given period of time. Remember strategies "decay" over time meaning they become less viable as others use new/different strategies.
def Expected_Value(average_returns, probability):
    return #integral(0, infinity)(x*f(x)*d(x))