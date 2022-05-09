#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  9 16:03:46 2022

@author: bratislavpetkovic
"""

import pandas as pd
import fmpsdk
import talib 
import matplotlib.pyplot as plt
import sys
sys.path.append(r'/Users/bratislavpetkovic/Desktop/cashew/WaveSurfer/')
from helper_functions import *

commodityList = ["AAPL", "MSFT", "NVDA", "TSLA"]
timeFrameList = ["1min","5min","15min","30min","1hour","4hour","daily"]

time="1hour"
symbol="AMZN"
priceURL = ("https://financialmodelingprep.com/api/v3/historical-chart/"+time+"/"+symbol+"?apikey=ce687b3fe0554890e65d6a5e48f601f9")
url = ("https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?apikey=ce687b3fe0554890e65d6a5e48f601f9")
msft = pd.DataFrame.from_dict(get_jsonparsed_data(priceURL))


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
#------------------------------------------------------------------------------------------------------------------------------------------
upper, mid, lower = talib.BBANDS(msft['close'], nbdevup=2, nbdevdn=2, timeperiod=20)
plt.plot(upper, label="Upper band")
plt.plot(mid, label='Middle band')
plt.plot(lower, label='Lower band')
plt.plot(msft['close'], label="Close")
plt.title('Bollinger Bands')
plt.legend()
plt.show()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.set_ylabel('$')
ax1.plot(upper, label="Upper band")
ax1.plot(mid, label='Middle band')
ax1.plot(lower, label='Lower band')
ax1.plot(msft['close'],color = 'black')
ax2.set_ylabel('RSI')
ax2.plot(msft['RSI'], color='blue')
ax2.axhline(y = 70, color = 'r', linestyle = '-')
ax2.axhline(y = 30, color = 'r', linestyle = '-')
ax1.set_title('BB and RSI')
plt.show()