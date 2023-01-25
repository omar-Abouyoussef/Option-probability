import pandas as pd
import numpy as np
import yfinance as yf
from scipy.stats import norm
import datetime as dt
import plotly.express as px
import streamlit as st


##################
def get_strike_price(df, prob):
    returns = df['Close'].pct_change()
    mean = np.mean(returns)
    std = np.std(returns)

    #inverse cdf of normal distribution
    upper = norm.ppf(prob, loc = mean, scale = std)
    lower = norm.ppf(1-prob, loc = mean, scale = std)
    call_strike_price = df['Close'][-1]*(1+upper)
    put_strike_price = df['Close'][-1]*(1+lower)

    return returns, call_strike_price, put_strike_price
#################
####################



st.set_page_config(page_title="Option Probability Lab")
st.title('Option Probability Lab')
st.sidebar.header("Option probability calculator")

#User input
st.text_input(label = "Ticker: ",
                value = '^VIX',
                key="ticker")
ticker = st.session_state.ticker

st.date_input(label = "Start Date: ",
                value = (dt.date.today() - dt.timedelta(days = 252)),
                key="start_date")
start_date = st.session_state.start_date

st.date_input(label = "End Date: ",
                        value = dt.date.today(),
                key="end_date")
end_date = st.session_state.end_date

st.text_input(label = "Interval:\n1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo ",
                value='1d',
                key="interval")
interval = st.session_state.interval

prob = st.number_input(label = 'Desired Probability: ',
                        min_value=0.0,
                        max_value=1.0,
                        value = 0.95,
                        step = 0.01,
                        key='prob')
prob = st.session_state.prob



df = yf.download(tickers=ticker,start=start_date, end=end_date, interval=interval)

returns, call_strike_price, put_strike_price = get_strike_price(df, prob)

cdf = norm.cdf(np.sort(returns), loc = np.mean(returns), scale = np.std(returns))    
fig = px.line(x = np.sort(returns)*100, y = np.sort(cdf)*100, title = "Cumulative Distribution of Returns", labels={'x':'Change %', 'y':'Probability %'})
st.plotly_chart(fig)
st.write(f"Short call option with strike price: {call_strike_price.round(1)}\n")
st.write(f"Short put option with strike price: {put_strike_price.round(1)}")
