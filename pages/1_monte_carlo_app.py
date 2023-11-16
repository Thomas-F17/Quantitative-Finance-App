import streamlit as st
from monte_carlo_simulation import monte_carlo_option_pricing
import plotly.express as px
import pandas as pd

# set layout to wide
st.set_page_config(layout="wide")

st.title("Option Pricing through Monte Carlo Simulation")
st.write("This app performs Monte Carlo simulation for option pricing and plots the simulated price paths.")

col1, col2 = st.columns([0.3, 0.7], gap = 'large')
with col1:
    st.write("## Input Parameters")
    option_type = st.selectbox("Option Type", ("Call", "Put"))  # "Call" or "Put"  
    stock_price = st.number_input("Stock Price", value=100)
    strike_price = st.number_input("Strike Price", value=100)
    volatility = st.number_input("Volatility", value=0.2)  # Annualized volatility (e.g., 20%)
    risk_free_rate = st.number_input("Risk-free Rate", value=0.05)  # Annual risk-free interest rate (e.g., 5%)
    time_to_maturity = st.number_input("Time to Maturity", value=1)  # Time to maturity in years
    num_simulations = st.number_input("Number of Simulations", value=10)

with col2:
    st.write("## Output")
    # Calculate the option price using Monte Carlo simulation and obtain price paths
    option_price, price_paths = monte_carlo_option_pricing(option_type, stock_price, strike_price, volatility, risk_free_rate, time_to_maturity, num_simulations)

    st.metric("The estimated option price is: ", f"{option_price:.2f}")

    # Combine the simulated price paths into a single DataFrame
    df = pd.DataFrame(price_paths).T
    # Rename columns
    df.columns = [f"Path {i+1}" for i in range(num_simulations)]

    # Create an interactive plot using Plotly Express
    fig = px.line(df, labels={"index": "Time Steps", "value": "Stock Price"}, title="Simulated Price Paths")

    st.plotly_chart(fig, use_container_width=True)