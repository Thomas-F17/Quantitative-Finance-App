import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm, t

def Param_Var_CVaR(Ticker, Start, End, confidence, returns):
    """
    Calculates Parametric Value at Risk (VaR) and Conditional Value at Risk (CVaR) for a given stock.

    Parameters
    ----------
    Ticker : str
        The ticker symbol of the stock to analyze (e.g., 'GOOG' for Google).
    Start : str
        The start date for the data in 'YYYY-MM-DD' format.
    End : str
        The end date for the data in 'YYYY-MM-DD' format.
    confidence : float
        The confidence level for VaR and CVaR calculation, expressed as a percentage (e.g., 99 for 99%).

    Returns
    -------
    VaR_norm : float
        The 1-day Value at Risk using the normal distribution.
    VaR_t : float
        The 1-day Value at Risk using the t-distribution.
    CVaR_norm : float
        The 1-day Conditional Value at Risk using the normal distribution.
    CVaR_t : float
        The 1-day Conditional Value at Risk using the t-distribution.
    StockVolatilityDay : float
        The daily stock volatility (standard deviation of returns).
    StockVolatilityYear : float
        The annualized stock volatility.
    nu : float
        The degrees of freedom for the t-distribution.

    Notes
    -----
    This function calculates the parametric VaR and CVaR using both the normal and t-distributions. The t-distribution
    parameters are estimated from the stock's historical returns for the chosen period. VaR and CVaR provide an estimate of the maximum loss expected over a specified time frame with a
    certain confidence level. The t-distribution is often used for small sample sizes or when the data is skewed.
    see for more information: 
    https://quantatrisk.com/2016/12/08/conditional-value-at-risk-student-t/
    https://quantatrisk.com/2015/12/02/student-t-linear-value-at-risk/
"""
    
    # Convert confidence from percentage to decimal
    confidence_decimal = confidence / 100

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

    StockStd = StockReturns.std()
    mu = StockReturns.mean()

    # Finding the degrees of freedom from the return distribution and rounding
    tfit = t.fit(StockReturns)
    nu, mu_t, std_t = tfit
    nu = np.round(nu)

    # Parametric VaR using normal distribution
    VaR_norm = norm.ppf(confidence_decimal) * StockStd - mu

    # Parametric VaR using t-distribution
    VaR_t = t.ppf(confidence_decimal, nu) * StockStd * np.sqrt((nu - 2) / nu) - mu

    # Parametric CVaR using normal distribution
    CVaR_norm = (norm.pdf(norm.ppf(1 - confidence_decimal)) / (1 - confidence_decimal)) * StockStd - mu

    # Parametric CVaR using t-distribution
    x = t.ppf(1 - confidence_decimal, nu)
    CVaR_t = (-1 / (1 - confidence_decimal)) * (1 - nu) ** (-1) * (nu - 2 + x ** 2) * t.pdf(x, nu) * StockStd - mu

    # Calculate stock volatility (standard deviation of returns)
    StockVolatilityDay = StockStd
    StockVolatilityYear = StockStd * np.sqrt(252)

    return VaR_norm, VaR_t, CVaR_norm, CVaR_t, StockVolatilityDay, StockVolatilityYear, nu
