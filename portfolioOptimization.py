# Optimizing a portfolio of 20 NASDAQ stocks
# Finding the 5 least correlated stocks
# Assuming a 20 % weight per stock in a portfolio

import math
from itertools import combinations
import numpy as np
import pandas as pd
import yfinance as yf
# Importing the Yahoo Finance library to access stock data

symbols=("AAPL", "MSFT", "AMZN", "FB", "GOOGL", "GOOG", "TSLA", "NVDA", "PYPL",
"ADBE", "NFLX", "INTC", "CSCO", "CMCSA", "PEP", "COST", "TMUS", "AMGN", "AVGO",
"QCOM")
# Initializing a tuple with the top 20 stocks of the NASDAQ 100
# The stocks are ranked by their weights in the index

allPrices=pd.DataFrame()
# allPrices = the data frame that will store all the price data we need

for i in symbols:
    stock=yf.download(i, period="2y", interval="1mo").dropna()
    # Clean out missing values from the accessed data
    allPrices[i]=stock["Close"]
    # Store the closing price of each stock
# allPrices now has all prices across all required dates for all stocks

portfoliosObj=combinations(symbols, 5)
# Creating an object with all possible 5-length combinations of our 20 stocks
# Each tuple element in the object is a possible 5-stock portfolio
# There are 15504 possible portfolios in this case
portfolios=tuple(portfoliosObj)
# Converting the object to a tuple for iterative ease

weights=np.array([[0.2], [0.2], [0.2], [0.2], [0.2]])
# weights = standard weights array for each portfolio
# Every stock in a portfolio gets a 20 % weight

stanDevs=np.empty(15504)
# stanDevs = array that will contain the standard deviations of each possible
# portfolio

for i in range(len(portfolios)):

    currentPrices=pd.DataFrame()
    # The data frame to store the prices of the current portfolio's stocks

    for j in portfolios[i]:
        currentPrices[j]=allPrices[j]
    # Import the 5 relevant columns from allPrices

    currentPricesArray=currentPrices.to_numpy()
    # Storing the prices in a numpy matrix for mathematical operations
    meanPrice=currentPricesArray.mean(axis=0)
    # Array containing the mean price for each stock for the two-year period
    demeanedPrices=currentPricesArray-meanPrice
    # Matrix containing demeaned stock prices to establish a common price base

    priceCount=demeanedPrices.shape[0]
    # priceCount = the number of prices retrieved for each stock
    # Equal to the number of rows in both the prices and demeanedPrices matrices

    covariance=(np.dot(np.transpose(demeanedPrices), demeanedPrices))/priceCount
    # covariance = the covariance matrix for the current portfolio
    # The covariance of two stocks is representative of the degree of
    # correlation between the pair of stocks
    # All such covariances in the portfolio are represented in the matrix
    portfVariance=np.dot(weights.T, np.dot(covariance, weights))
    # portfVariance = variance of the entire portfolio
    portfStanDev=math.sqrt(portfVariance)
    # portfStanDev = standard deviation of the entire portfolio
    # This is the final variable that condenses the correlation among all
    # stocks in a portfolio into one value
    # The lesser a portfolio's standard deviation, the less correlated its
    # stocks are

    stanDevs[i]=portfStanDev
    # Updating the current portfolio's standard deviation in the predefined
    # array

# The standard deviations array is now complete
minStanDev=stanDevs.min()
# minStanDev = the minimum standard deviation possible for any portfolio
findMin=np.where(stanDevs==minStanDev)
# findMin = a tuple of an array storing the index that contains the minimum
# standard deviation
indexMin=findMin[0][0]
# Extracting the numerical value of the located index
# The corresponding optimal portfolio will thus be at the same index in the
# portfolios tuple
optimalPortfolio=portfolios[indexMin]
# We finally have the most diverse portfolio out of all possible options

print("The 5 least correlated stocks among the top 20 NASDAQ stocks are:")
for i in optimalPortfolio:
    print(i)
# Print the ticker symbols of the stocks to wrap up
