import streamlit as st
import yfinance as yf
import os
from datetime import datetime, timedelta
import time
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
import pandas as pd
 
 
current_date = datetime.now()
# current_date = pd.Timestamp(datetime.now()).tz_localize('UTC')
 
st.title("Thematic Investment Analyzer")
 
# List of actual names of NIFTY indices
tickers = [
    'NIFTY 50',
    'NIFTY 100',
    'NIFTY Bank',
    'NIFTY Auto',
    'NIFTY Financial Services',
    'NIFTY FMCG',
    'NIFTY IT',
    'NIFTY Media',
    'NIFTY Metal',
    'NIFTY Pharma',
    'NIFTY PSU Bank',
    'NIFTY Private Bank',
    'NIFTY Realty',
    'NIFTY Energy'
]

# Dictionary mapping ticker symbols to index names
nifty_indices_reverse = {
    'NIFTY 50': '^NSEI',
    'NIFTY 100': '^CNX100',
    'NIFTY Bank': '^NSEBANK',
    'NIFTY Auto': '^CNXAUTO',
    'NIFTY Financial Services': '^CNXFIN',
    'NIFTY FMCG': '^CNXFMCG',
    'NIFTY IT': '^CNXIT',
    'NIFTY Media': '^CNXMEDIA',
    'NIFTY Metal': '^CNXMETAL',
    'NIFTY Pharma': '^CNXPHARMA',
    'NIFTY PSU Bank': '^CNXPSUBANK',
    'NIFTY Private Bank': '^CNXPVTBANK',
    'NIFTY Realty': '^CNXREALTY',
    'NIFTY Energy': '^CNXENERGY'
}

reversed_dict = {value: key for key, value in nifty_indices_reverse.items()}

# @st.cache_data
def fetch_stock_data(tickers):
    result =pd.DataFrame()
    
    for ticker in tickers:
        tickers_indices = nifty_indices_reverse[ticker]
        data = yf.download(tickers_indices, period="5y", interval="1d")
        data.columns = ['_'.join(col) for col in data.columns]
        data['Ticker']=tickers_indices
        
        result = pd.concat([result,data])
    return result
data = fetch_stock_data(tickers)
print(data.columns)
selected_tickers=tickers[0]
st.write("Select indices to compare :")
selected_tickers_indices = st.multiselect(label='',options = tickers,default=tickers[0])
selected_tickers =[]
selected_tickers = [nifty_indices_reverse[ticker] for ticker in selected_tickers_indices]
st.write("Select your time frame :")
time_frame = st.radio(label = '',options= ['5y','3y','1y','6m','3m','1m',"1w"],index= 0, horizontal = True)
period_map  = {
    "5y":(5,0,0),
    "3y": (3,0,0),
    "1y": (1,0,0),
    "6m": (0,6,0),
    "3m": (0,3,0),
    "1m": (0,1,0),
    "1w": (0,0,1)
}
timeframe= period_map[time_frame]
fig,ax = plt.subplots(figsize = (10,6))
start_date = current_date - relativedelta(years = timeframe[0],months = timeframe[1],weeks = timeframe[2])
stock_data = data[(data.index>=start_date) & (data.index<=current_date) & (data['Ticker'].isin(selected_tickers))]
labels_chart =[]
for ticker in selected_tickers:
    string = f"Close_{ticker}"
    stock_data_selected_ticker = stock_data[(stock_data['Ticker'] == ticker) & (stock_data[string] != None) ]
    stock_returns = (stock_data_selected_ticker[string].iloc[-1]-stock_data_selected_ticker[string].iloc[0])/stock_data_selected_ticker[string].iloc[0]
    print(stock_data_selected_ticker)
    st.write(f"{reversed_dict[ticker]} movement for the last {time_frame} :",round(stock_returns*100,2),"%")
    ax.plot(stock_data_selected_ticker.index,stock_data_selected_ticker[string],label= labels_chart)
    # labels_chart.append(reversed_dict[ticker])



ax.set_xlabel('Date')
ax.set_ylabel('Index')
ax.grid(False)
ax.legend(labels_chart)
st.pyplot(fig)