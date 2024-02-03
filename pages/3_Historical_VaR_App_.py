import streamlit as st
from hist_var import HistVar_CVaR
from datetime import datetime, timedelta
import pandas as pd

st.title('Historical VaR and CVaR Calculator')

if 'decimal_places' not in st.session_state:
    st.session_state.decimal_places = 2

# Set default ticker to 'AAPL'
default_ticker = 'AAPL'
ticker = st.text_input('Ticker', value=default_ticker)

# Set default dates
default_start_date = datetime.now() - timedelta(days=5*365) # 5 years ago from today
default_end_date = datetime.now()

start = st.date_input('Start Date', value=default_start_date, format="DD/MM/YYYY")
end = st.date_input('End Date', value=default_end_date, format="DD/MM/YYYY")

# Choose Return Calc Type
returns = st.radio(
    "Return Calculation Type:",
    ["simple", "continously compounded"],
    index=None,
)

# Set confidence level
confidence = st.slider('Confidence Level (1-X)', min_value=0.01, max_value=0.99, value=0.95, step=0.01)

if ticker and start and end and confidence and returns:
    try:
        histVar, histCVar, StockVolatilityDay, StockVolatilityYear = HistVar_CVaR(ticker, start, end, confidence, returns)
        format_string = f"{{:.{st.session_state.decimal_places}f}}%"

        results = pd.DataFrame({
            "Metric": ["Historical VaR", "Historical CVaR", "Stock Volatility (Day)", "Stock Volatility (Year)"],
            "Value (%)": [format_string.format(histVar*-100), format_string.format(histCVar*-100), format_string.format(StockVolatilityDay*100), format_string.format(StockVolatilityYear*100)]
        })
        results = results.set_index('Metric')
        st.table(results)

    except Exception as e:
        st.error(f"An error occurred: {e}")


# Slider for number of decimal places
decimal_places = st.slider('Number of Decimal Places', min_value=0, max_value=10, value=2, step=1)

if decimal_places != st.session_state.decimal_places:
    st.session_state.decimal_places = decimal_places
    st.experimental_rerun()
    