import numpy as np
import pandas as pd
import yfinance as yf

def HistVar_CVaR(Ticker, Start, End, confidence):
    """Get data from yahoo finance and calculate historical VaR and CVaR"""

    # Ensure Start and End are in datetime format
    Start = pd.to_datetime(Start)
    End = pd.to_datetime(End)

    # Fetch data from Yahoo Finance using yfinance
    Data = yf.download(Ticker, start=Start, end=End)
    Data = Data['Close']

    # Calculate daily returns
    StockReturns = Data.pct_change().dropna()

    # Historical VaR calculation
    histVar = np.percentile(StockReturns, (1 - confidence) * 100)

    # Historical CVaR calculation

    histCVar = StockReturns[StockReturns <= histVar].mean()

    # Calculate stock volatility (standard deviation of returns)
    StockVolatilityDay = StockReturns.std()

    StockVolatilityYear = StockReturns.std() * np.sqrt(252)

    return histVar, histCVar, StockVolatilityDay, StockVolatilityYear