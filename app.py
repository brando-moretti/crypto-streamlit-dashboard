import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 1. Basic page configuration
st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("📊 Real-Time Cryptocurrency Dashboard")
st.markdown("Data extracted via the public CoinGecko API.")

# 2. Function to fetch data (with cache to avoid overloading the API)
@st.cache_data(ttl=60) # Data updates every 60 seconds
def get_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    # Parameters to request the top 5 cryptos in Euro, including data from the last 7 days
    parameters = {
        "vs_currency": "eur",
        "order": "market_cap_desc",
        "per_page": 5,
        "page": 1,
        "sparkline": "true" 
    }
    response = requests.get(url, params=parameters)
    return response.json()

# Execute the API call
json_data = get_data()

# 3. REAL-TIME UPDATED COUNTERS (Metrics)
st.subheader("Current Values (Top 3)")
metric_columns = st.columns(3)

# Create a counter for the top 3 cryptocurrencies
for i in range(3):
    crypto = json_data[i]
    metric_columns[i].metric(
        label=crypto['name'],
        value=f"{crypto['current_price']} €",
        delta=f"{crypto['price_change_percentage_24h']:.2f}%" # 24h percentage change
    )

st.divider()

# Create two columns to place the charts side-by-side
left_column, right_column = st.columns(2)

# 4. PIE CHART
with left_column:
    st.subheader("Market Dominance (Top 5)")
    # Transform JSON data into a Pandas DataFrame for easier handling
    market_df = pd.DataFrame(json_data)[['name', 'market_cap']]
    
    # Use Plotly for an interactive pie chart
    pie_chart = px.pie(
        market_df, 
        values='market_cap', 
        names='name', 
        hole=0.4 # Creates a donut chart, very elegant
    )
    st.plotly_chart(pie_chart, use_container_width=True)

# 5. TREND LINES
with right_column:
    st.subheader("Price Trend (Last 7 Days)")
    # Extract the 7-day price array for the first crypto (Bitcoin)
    crypto_name = json_data[0]['name']
    historical_prices = json_data[0]['sparkline_in_7d']['price']
    
    trend_df = pd.DataFrame(historical_prices, columns=[f'{crypto_name} Price (EUR)'])
    
    # Use Streamlit's native line chart
    st.line_chart(trend_df)