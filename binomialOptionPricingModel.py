# Simulation of the binomial model for pricing stock options
# Implemented for a European-style call option

import math

def findPrice(stockPrice, volatility, expiryTime, intRate, strike, stepCount):
    # stockPrice = current price of the underlying stock
    # volatility = measure of randomness of the stock's price
    # expiryTime = time period in years within which the option can be exercised
    # intRate = risk-free rate of interest on the stock
    # strike = strike price for the option contract
    # stepCount = number of times the stock changes value
    levelCount=stepCount+1
    # levelCount = number of levels in the stock value tree
    # One starting value plus one level added per step
    timeStep=expiryTime/stepCount
    # timeStep = length of interval after which the stock changes value
    upFact=1+volatility*math.sqrt(timeStep)
    # upFact = factor by which the stock will appreciate on growth
    downFact=1-volatility*math.sqrt(timeStep)
    # downFact = factor by which the stock will depreciate on decline
    rfProb=0.5+(intRate*math.sqrt(timeStep))/(2*volatility)
    # rfProb = risk-free probability of the stock's value rising
    stocks=list()
    # stocks = 2D list to contain the stock price tree
    for i in range(levelCount):
        stocks.append([])
        # Every element in stocks is one level of the stock price tree
    options=list()
    # options = 2D list to contain the options value tree
    for i in range(levelCount):
        options.append([])
    stocks[0].append(stockPrice)
    # Update the known starting stock price
    for i in range(levelCount-1):
        for j in stocks[i]:
            stocks[i+1].append(j*upFact)
            stocks[i+1].append(j*downFact)
    # Update the stock tree with all possible stock values
    for i in stocks[levelCount-1]:
        # Access all stock prices at expiry
        # Find the intrinsic values of the option for each
        options[levelCount-1].append(optionVal(i, strike))
    discFact=math.exp(-1*intRate*timeStep)
    # discFact = the discount factor used to backdate from a future value
    # to a present value
    for i in range(levelCount-1, 0, -1):
        # Backtrack from the option values at expiry to update preceding values
        for j in range(0, len(stocks[i]), 2):
            options[i-1].append(discFact*(rfProb*options[i][j]+
            (1-rfProb)*options[i][j+1]))
    # The option values tree is now complete
    price=options[0][0]
    # The first value in the options tree is the stock option's price
    return price

def optionVal(stockPrice, strike):
    # A function to calculate the intrinsic value of an option at any node
    if(stockPrice>strike):
        return stockPrice-strike
    return 0.0

stockPrice=float(input("Enter the current price of the stock: "))
volatility=float(input("Enter the volatility: "))
expiryTime=float(input("Enter the expiration period of the option in years: "))
intRate=float(input("Enter the risk-free rate of interest: "))
strike=float(input("Enter the strike price for the option: "))
stepCount=int(input("Enter the number of times the stock changes value till expiry: "))

# All inputs acquired

price=findPrice(stockPrice, volatility, expiryTime, intRate, strike, stepCount)
print("The price of the stock option is", price)

# Final price printed
