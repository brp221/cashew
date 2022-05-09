#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trade Bot Draft 1 - "WaveSurfer"

@author: bratislavpetkovic
"""

import pandas as pd
import fmpsdk

import sys
sys.path.append(r'/Users/bratislavpetkovic/Desktop/cashew/WaveSurfer/')
from helper_functions import *

commodityList = ["AAPL", "MSFT", "NVDA", "TSLA"]
timeFrameList = ["1min","5min","15min","30min","1hour","4hour","daily"]
indicators = ["sma","ema","wma","dema","tema","williams","rsa","adx","standardDeviation"]

for i in timeFrameList:
    df = pd.DataFrame.from_dict(fmpsdk.technical_indicators("ce687b3fe0554890e65d6a5e48f601f9",commodityList[0],i,indicators[6]))
    if(len(df)>0): 
        df["date"] = pd.to_datetime(df["date"])
        # print(i,"--> ",df.iloc[0])
        print(i)
        print(df.head())
        print("\n\n")

#brew install ta-lib
import talib 
import matplotlib.pyplot as plt
time="1hour"
symbol="MSFT"
priceURL = ("https://financialmodelingprep.com/api/v3/historical-chart/"+time+"/"+symbol+"?apikey=ce687b3fe0554890e65d6a5e48f601f9")
url = ("https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?apikey=ce687b3fe0554890e65d6a5e48f601f9")
msft = pd.DataFrame.from_dict(get_jsonparsed_data(priceURL))
#------------------------------------------------------------------------------
msft['SMA20'] = talib.SMA(msft['close'], timeperiod=20)
msft['SMA50'] = talib.SMA(msft['close'], timeperiod=50)
plt.plot(msft['close'], color='black', label='Daily Close Price')
plt.plot(msft['SMA20'], color='green', label='SMA 20')
plt.plot(msft['SMA50'], color='red', label='SMA 50')
plt.legend()
plt.title('Simple Moving Averages')
plt.show()
#------------------------------------------------------------------------------
msft['EMA20'] = talib.EMA(msft['close'], timeperiod=20)
msft['EMA50'] = talib.EMA(msft['close'], timeperiod=50)
plt.plot(msft['close'], color='black', label='Daily Close Price')
plt.plot(msft['EMA20'], color='green', label='EMA 20')
plt.plot(msft['EMA50'], color='red', label='EMA 50')
plt.legend()
plt.title('Exponential Moving Avg')
plt.show()
#------------------------------------------------------------------------------
msft['ADX'] = talib.ADX(msft['high'], msft['low'], msft['close'], timeperiod=14)
fig, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.set_ylabel('Price')
ax1.plot(msft['close'], color='black')
ax2.set_ylabel('ADX')
ax2.plot(msft['ADX'], color='blue')
ax1.set_title('Daily Close Price and ADX')
ax2.axhline(y = 50, color = 'r', linestyle = '-')
ax2.axhline(y = 25, color = 'r', linestyle = '-')
plt.show()
#------------------------------------------------------------------------------
macd, macdsig = talib.MACD(msft['close'], fastperiod=12, slowperiod=26, signalperiod=9)
fig, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.set_ylabel('Price')
ax1.plot(msft['close'], color='black')
ax2.set_ylabel('MACD')
ax2.plot(macdsig, color='green', label='Signal Line')
ax2.plot(macd, color='red', label='MACD')
ax1.set_title('Daily Close Price and MACD')
plt.legend()
plt.show()

#------------------------------------------------------------------------------
msft['RSI'] = talib.RSI(msft['close'], timeperiod=14)
fig, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.set_ylabel('Price')
ax1.plot(msft['close'],color = 'black')
ax2.set_ylabel('RSI')
ax2.plot(msft['RSI'], color='blue')
ax2.axhline(y = 70, color = 'r', linestyle = '-')
ax2.axhline(y = 30, color = 'r', linestyle = '-')
ax1.set_title('Daily Close Price and RSI')
plt.show()
#------------------------------------------------------------------------------
upper, mid, lower = talib.BBANDS(msft['close'], nbdevup=2, nbdevdn=2, timeperiod=20)
plt.plot(upper, label="Upper band")
plt.plot(mid, label='Middle band')
plt.plot(lower, label='Lower band')
plt.plot(msft['close'], label="Close")
plt.title('Bollinger Bands')
plt.legend()
plt.show()
#------------------------------------------------------------------------------
