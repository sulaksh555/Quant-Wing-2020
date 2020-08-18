# Implementation of the moving average crossover trading strategy
# Apple Inc shares for a 2-year period have been used for backtesting

import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import yfinance as yf
# Importing the Yahoo Finance library to access stock data

apple=yf.download("AAPL", period="2y")
strategyData=pd.DataFrame(apple["Close"])
# strategyData = data frame containing all important data about the strategy
# The first parameter of relevance is the daily closing price of the stock

strategyData["Position"]=0.0
# A column to keep a track of long and hold positions at each date

strategyData["SMA"]=strategyData["Close"].rolling(window=50, min_periods=1).mean()
# Set up the Short Moving Average of the stock with a 50-day period

strategyData["LMA"]=strategyData["Close"].rolling(window=200, min_periods=1).mean()
# Set up the Long Moving Average of the stock with a 200-day period

strategyData["Position"][50:]=np.where(strategyData["SMA"][50:]>
strategyData["LMA"][50:], 1.0, 0.0)
# Identify the trading position on each active day
# 1.0 corresponds to a long position with respect to the stock
# 0.0 corresponds to a hold position with respect to the stock
# Establish a long position in the stock whenever the SMA is greater than the LMA
# Consider indices 50 onwards so that the SMA has rolled over its entire window
# This ensures that the SMA and the LMA will not be taken over the same period
# The two MAs will hence have different periods and possess different values

strategyData["Signal"]=strategyData["Position"].diff()
# Use the trade positions data to identify when signals occur
# A positive difference between two days is a buy signal
# A negative difference between two days is a sell signal
# A zero difference between two days is a signal to hold onto the stock

# The framework for the strategy has now been set up
# We shall now backtest the strategy to see how it performs with past data

starter=500000.0
# Let the initial value of our portfolio be $ 500000
# This is entirely in the form of cash to begin with
# Some of the cash will later be used to buy company stock
# The remaining cash reserves will act as an unchanging asset

strategyData["Shares held"]=strategyData["Position"]*500.0
# Adding a column to denote the number of shares we have a long position in
# Every buy signal triggers an order to purchase 500 underlying shares

strategyData["Stock owned"]=strategyData["Close"]*strategyData["Shares held"]
# Adding a column to denote the monetary value of company stock we hold
# Dollar value of owned stock = dollar price per share * number of shares owned

strategyData["Cash expended"]=strategyData["Signal"]*strategyData["Close"]*500.0
# This column shows the amount of cash we spent on buying stock
# Positive buy signals lead to positive cash expenditures
# Negative sell signals lead to negative cash expenditures or us regaining cash

strategyData["Cash reserves"]=starter-strategyData["Cash expended"].cumsum()
# This marks how much unchanging cash we have left at each date

strategyData["Total assets"]=strategyData["Stock owned"]+strategyData["Cash reserves"]
# Our portfolio is made up of owned company stock and preserved cash
# The total value of our portfolio is the sum of these two assets

currentAssets=strategyData["Total assets"][-1]
# The present-day value of our overall portfolio

currentProfit=currentAssets-starter
# The net profit our strategy has given us so far

currentReturns=currentProfit/starter*100.0
# The current percentage return we are netting through the strategy

print("Using the strategy gives us present-day returns of", currentReturns,
"% on an initial investment of $", starter)
# Display current returns for the strategy

# Finally, plotting our total assets versus time visualizes the profitability
# of our trading strategy
# This is shown below

register_matplotlib_converters()

xData=np.array(strategyData.index)
yData=np.array(strategyData["Total assets"])
plt.plot(xData, yData)
plt.xlabel("Time")
plt.ylabel("Portfolio value")
plt.title("Trading strategy profitability")
plt.show()

# Display the portfolio value graph to complete the backtesting
