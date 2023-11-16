import numpy as np
from scipy.stats import norm
from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.greeks.analytical import delta, gamma, vega, theta, rho

# Function to calculate the option payoff based on option type
def calculate_option_payoff(option_type, stock_price, strike_price):
    if option_type == "Call":
        return max(stock_price - strike_price, 0)
    elif option_type == "Put":
        return max(strike_price - stock_price, 0)

# Function to calculate option price with BS
def blackScholes(risk_free_rate, stock_price, strike_price, time_to_maturity, volatility, option_type):
    "Calculate BS price of call/put"
    d1 = (np.log(stock_price/strike_price) + (risk_free_rate + volatility**2/2)*time_to_maturity)/(volatility*np.sqrt(time_to_maturity))
    d2 = d1 - volatility*np.sqrt(time_to_maturity)
    
    if option_type == "Call":
        price = stock_price*norm.cdf(d1, 0, 1) - strike_price*np.exp(-risk_free_rate*time_to_maturity)*norm.cdf(d2, 0, 1)
    elif option_type == "Put":
        price = strike_price*np.exp(-risk_free_rate*time_to_maturity)*norm.cdf(-d2, 0, 1) - stock_price*norm.cdf(-d1, 0, 1)

    type = option_type[0].lower()

    return (price + bs(type, stock_price, strike_price, time_to_maturity, risk_free_rate, volatility))/2

# Function to calculate option delta with BS
def delta_calc(risk_free_rate, stock_price, strike_price, time_to_maturity, volatility, option_type):
    "Calculate delta of an option"
    d1 = (np.log(stock_price/strike_price) + (risk_free_rate + volatility**2/2)*time_to_maturity)/(volatility*np.sqrt(time_to_maturity))
    
    if option_type == "Call":
        delta_calc = norm.cdf(d1, 0, 1)
    elif option_type == "Put":
        delta_calc = -norm.cdf(-d1, 0, 1)
    
    type = option_type[0].lower()
    
    return (delta_calc + delta(type, stock_price, strike_price, time_to_maturity, risk_free_rate, volatility))/2


# Function to calculate option gamma with BS
def gamma_calc(risk_free_rate, stock_price, strike_price, time_to_maturity, volatility, option_type):
    "Calculate gamma of a option"
    d1 = (np.log(stock_price/strike_price) + (risk_free_rate + volatility**2/2)*time_to_maturity)/(volatility*np.sqrt(time_to_maturity))

    gamma_calc = norm.pdf(d1, 0, 1)/(stock_price*volatility*np.sqrt(time_to_maturity))
    
    type = option_type[0].lower()
    
    return (gamma_calc + gamma(type, stock_price, strike_price, time_to_maturity, risk_free_rate, volatility))/2

def vega_calc(risk_free_rate, stock_price, strike_price, time_to_maturity, volatility, option_type):
    "Calculate BS price of call/put"
    d1 = (np.log(stock_price/strike_price) + (risk_free_rate + volatility**2/2)*time_to_maturity)/(volatility*np.sqrt(time_to_maturity))
    
    vega_calc = stock_price*norm.pdf(d1, 0, 1)*np.sqrt(time_to_maturity)
    
    type = option_type[0].lower()
    
    return (vega_calc*0.01 + vega(type, stock_price, strike_price, time_to_maturity, risk_free_rate, volatility))/2

def theta_calc(risk_free_rate, stock_price, strike_price, time_to_maturity, volatility, option_type):
    "Calculate BS price of call/put"
    d1 = (np.log(stock_price/strike_price) + (risk_free_rate + volatility**2/2)*time_to_maturity)/(volatility*np.sqrt(time_to_maturity))
    d2 = d1 - volatility*np.sqrt(time_to_maturity)
    
    if option_type == "Call":
        theta_calc = -stock_price*norm.pdf(d1, 0, 1)*volatility/(2*np.sqrt(time_to_maturity)) - risk_free_rate*strike_price*np.exp(-risk_free_rate*time_to_maturity)*norm.cdf(d2, 0, 1)
    elif option_type == "Put":
        theta_calc = -stock_price*norm.pdf(d1, 0, 1)*volatility/(2*np.sqrt(time_to_maturity)) + risk_free_rate*strike_price*np.exp(-risk_free_rate*time_to_maturity)*norm.cdf(-d2, 0, 1)
    
    type = option_type[0].lower()

    return (theta_calc/365 + theta(type, stock_price, strike_price, time_to_maturity, risk_free_rate, volatility))/2

def rho_calc(risk_free_rate, stock_price, strike_price, time_to_maturity, volatility, option_type):
    "Calculate BS price of call/put"
    d1 = (np.log(stock_price/strike_price) + (risk_free_rate + volatility**2/2)*time_to_maturity)/(volatility*np.sqrt(time_to_maturity))
    d2 = d1 - volatility*np.sqrt(time_to_maturity)

    if option_type == "Call":
        rho_calc = strike_price*time_to_maturity*np.exp(-risk_free_rate*time_to_maturity)*norm.cdf(d2, 0, 1)
    elif option_type == "Put":
        rho_calc = -strike_price*time_to_maturity*np.exp(-risk_free_rate*time_to_maturity)*norm.cdf(-d2, 0, 1)
    
    type = option_type[0].lower()
    
    return (rho_calc*0.01 + rho(type, stock_price, strike_price, time_to_maturity, risk_free_rate, volatility))/2
