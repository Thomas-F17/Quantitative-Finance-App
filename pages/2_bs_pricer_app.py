import streamlit as st
from bs_pricer import blackScholes,delta_calc,gamma_calc,vega_calc,theta_calc,rho_calc

# set layout to wide
st.set_page_config(layout="wide")

st.title("Option Pricing through Black-Scholes Merton")
st.write("This app calculates option price and greeks based on the Black-Scholes Merton model.")

col1, col2 = st.columns([0.3, 0.7], gap = 'large')
with col1:
    st.write("## Input Parameters")
    option_type = st.selectbox("Option Type", ("Call", "Put"))  # "Call" or "Put"  
    stock_price = st.number_input("Stock Price", value=100)
    strike_price = st.number_input("Strike Price", value=100)
    volatility = st.number_input("Volatility (annualised)", value=0.2)  # Annualized volatility (e.g., 20%)
    risk_free_rate = st.number_input("Risk-free Rate (annualised)", value=0.05)  # Annual risk-free interest rate (e.g., 5%)
    time_to_maturity = st.number_input("Time to Maturity (in years)", value=1)  # Time to maturity in years

with col2:
    st.write("## Output")
    # Calculate the option price using Monte Carlo simulation and obtain price paths
    bs_p = blackScholes(risk_free_rate, stock_price, strike_price, time_to_maturity, volatility, option_type)
    bs_d = delta_calc(risk_free_rate, stock_price, strike_price, time_to_maturity, volatility, option_type)
    bs_g = gamma_calc(risk_free_rate, stock_price, strike_price, time_to_maturity, volatility, option_type)
    bs_v = vega_calc(risk_free_rate, stock_price, strike_price, time_to_maturity, volatility, option_type)
    bs_t = theta_calc(risk_free_rate, stock_price, strike_price, time_to_maturity, volatility, option_type)
    bs_r = rho_calc(risk_free_rate, stock_price, strike_price, time_to_maturity, volatility, option_type)

    st.metric("The estimated option price is: ", f"{bs_p:.3f}")
    st.metric("The estimated option delta is: ", f"{bs_d:.3f}")
    st.metric("The estimated option gamma is: ", f"{bs_g:.3f}")
    st.metric("The estimated option vega is: ", f"{bs_v:.3f}")
    st.metric("The estimated option theta is: ", f"{bs_t:.3f}")
    st.metric("The estimated option rho is: ", f"{bs_r:.3f}")

