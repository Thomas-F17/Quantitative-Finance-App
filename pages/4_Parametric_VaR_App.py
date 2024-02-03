import streamlit as st
from var_cvar import Param_Var_CVaR
from datetime import datetime, timedelta
import pandas as pd

st.title('Parametric VaR and CVaR Calculator for Normal and T -Distributions')

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
confidence = st.slider('Confidence Level (1-X)%', min_value=1, max_value=99, value=95, step=1)

if ticker and start and end and confidence and returns:
    try:
        VaR_norm, VaR_t, CVaR_norm, CVaR_t, StockVolatilityDay, StockVolatilityYear, nu = Param_Var_CVaR(ticker, start, end, confidence, returns)
        format_string = f"{{:.{st.session_state.decimal_places}f}}%"

        results = pd.DataFrame({
            "Metric": ["1-day VaR (Normal Distribution)", "1-day VaR (T-Distribution)", "1-day CVaR (Normal Distribution)", "1-day CVaR (T-Distribution)", "Stock Volatility (1-Day)", "Stock Volatility (Annualised)"],
            "Value (%)": [format_string.format(VaR_norm*100), format_string.format(VaR_t*100), format_string.format(CVaR_norm*100), format_string.format(CVaR_t*100), format_string.format(StockVolatilityDay*100), format_string.format(StockVolatilityYear*100)]
        })
        results = results.set_index('Metric')
        st.table(results)
        st.write(f"Degrees of Freedom (t-distribution): {nu}")

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Slider for number of decimal places
decimal_places = st.slider('Number of Decimal Places', min_value=0, max_value=10, value=2, step=1)

if decimal_places != st.session_state.decimal_places:
    st.session_state.decimal_places = decimal_places
    st.experimental_rerun()

# Explanations
st.markdown("## VaR and CVaR Calculation Formulas")
st.markdown("""
Value at Risk (VaR) and Conditional Value at Risk (CVaR) are calculated using the following formulas:

### VaR Calculation

- **Normal Distribution:**
              
  $VaR_{\\text{norm}} = -\\mu + Z_{\\alpha} \\times \\sigma$
  
  - $\\mu$ is the mean of the returns,
  - $\\sigma$ is the standard deviation of the returns,
  - $Z_{\\alpha}$ is the Z-score corresponding to the confidence level $\\alpha$.


                   
- **t-Distribution:** 
             
  $VaR_{t} = -\\mu + t_{\\alpha, \\nu} \\times \\sigma \\times \\sqrt{\\frac{\\nu - 2}{\\nu}}$
  
  - $t_{\\alpha, \\nu}$ is the t-score corresponding to the confidence level $\\alpha$ and degrees of freedom $\\nu$ (determined by fitting the data).

### CVaR Calculation

- **Normal Distribution:**  
            
  $CVaR_{\\text{norm}} = -\\mu + \\frac{\\phi(Z_{1 - \\alpha})}{1 - \\alpha} \\times \\sigma$
  
  - $\\phi(Z_{1 - \\alpha})$ is the PDF of the normal distribution at $Z_{1 - \\alpha}$.


                 
- **t-Distribution:**  
            
  $CVaR_{t} = -\\mu + \\frac{1}{1 - \\alpha} \\times \\frac{\\nu + t_{1 - \\alpha, \\nu}^2}{\\nu - 1} \\times \\sigma \\times \\sqrt{\\frac{\\nu - 2}{\\nu}} \\times t_{1 - \\alpha, \\nu}$
  
  - $t_{1 - \\alpha, \\nu}$ is the t-score corresponding to the confidence level $1 - \\alpha$ and degrees of freedom $\\nu$ (determined by fitting the data).
""")