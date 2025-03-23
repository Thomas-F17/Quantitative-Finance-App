import numpy as np
import pandas as pd
import yfinance as yf

def HistVar_CVaR(Ticker, Start, End, confidence, returns):
    """
    Gets stock price data from Yahoo Finance and calculates the historical Value at Risk (VaR) and Conditional Value at Risk (CVaR).

    Parameters
    ----------
    Ticker : str
        The ticker symbol of the stock to analyze (e.g., 'AAPL' for Apple Inc.).
    Start : str
        The start date for fetching data in 'YYYY-MM-DD' format.
    End : str
        The end date for fetching data in 'YYYY-MM-DD' format.
    confidence : float
        The confidence level for VaR and CVaR calculation, expressed as a decimal (e.g., 0.95 for 95% confidence).
    returns : str, optional
        The type of returns to calculate. Can be "simple" for simple returns or "continuously compounded" for log returns. Default is "simple".

    Returns
    -------
    histVar : float
        The historical Value at Risk (VaR) at the specified confidence level.
    histCVar : float
        The historical Conditional Value at Risk (CVaR) at the specified confidence level.
    StockVolatilityDay : float
        The daily stock volatility (standard deviation of the returns).
    StockVolatilityYear : float
        The annualized stock volatility, assuming 252 trading days in a year.

    Notes
    -----
    This is a straightforward method for calculating historical VaR and CVaR for any stock listed on Yahoo Finance with either simple or continously compounded returns.

    Examples
    --------
    >>> HistVar_CVaR("AAPL", "2020-01-01", "2021-01-01", 0.95, returns="simple")
    >>> HistVar_CVaR("GOOG", "2020-01-01", "2021-01-01", 0.95, returns="continuously compounded")
    """

    # Ensure Start and End are in datetime format
    if returns == "simple":
        Start = pd.to_datetime(Start)
        End = pd.to_datetime(End)
    elif returns == "continuously compounded":
        Start = pd.to_datetime(Start) - pd.Timedelta(days=1)
        End = pd.to_datetime(End)

    # Fetch data from Yahoo Finance using yfinance
    Data = yf.download(Ticker, start=Start, end=End, auto_adjust=True)['Close']

    # Calculate daily returns
    if returns == "simple":
        StockReturns = Data.pct_change().dropna()
    elif returns == "continuously compounded":
        StockReturns = np.log(Data / Data.shift(1)).dropna()

    # Historical VaR calculation
    histVar = np.percentile(StockReturns, (1 - confidence) * 100)

    # Historical CVaR calculation

    histCVar = StockReturns[StockReturns <= histVar].mean()

    # Calculate stock volatility (standard deviation of returns)
    StockVolatilityDay = StockReturns.std()

    StockVolatilityYear = StockReturns.std() * np.sqrt(252)

    return float(histVar), float(histCVar), float(StockVolatilityDay), float(StockVolatilityYear)