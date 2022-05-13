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
msftR = msft[::-1]
#------------------------------------------------------------------------------------------------------------------------------------------
msftR['RSI'] = talib.RSI(msftR['close'], timeperiod=14)
msftR['upper'], msftR['mid'], msftR['lower'] = talib.BBANDS(msftR['close'], nbdevup=2, nbdevdn=2, timeperiod=20)
msftR['OBV'] = talib.OBV(msftR['close'], msftR['volume'])
#-------------------------------------------------------------------------------------------------------------------------------------------------------
plt.figure(figsize=(10, 10))
fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
ax1.set_ylabel('$')
ax1.plot(msftR['date'],msftR['upper'], label="Up band")
ax1.plot(msftR['date'],msftR['mid'], label='Mid band')
ax1.plot(msftR['date'],msftR['lower'], label='Low band')
ax1.plot(msftR['date'],msftR['close'],color = 'black')
ax2.set_ylabel('RSI')
ax2.plot(msftR['date'],msftR['RSI'], color='blue')
ax2.axhline(y = 70, color = 'r', linestyle = '-')
ax2.axhline(y = 30, color = 'r', linestyle = '-')
ax3.plot(msftR['date'],msftR['OBV'], color='purple')
ax1.set_title('BB and RSI')
plt.show()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
# inspiration: https://tradingstrategyguides.com/best-combination-of-technical-indicators/

# Step #1: Price needs to Break and Close above the middle Bollinger Band
condition_1 = msftR[msftR["mid"]<=msftR["close"]]
bb_graph(msftR, condition_1["date"])

# Step #2: Wait for the RSI indicator to trade above the 50 level if it doesn’t already
condition_2 = msftR[msftR["RSI"]>50]
rsi_graph(msftR, condition_2["date"])

# Step #3: Wait for the OBV indicator to rise. Buy at the market once you see volume confirming the price.
# result = msftR["OBV"].rolling(10, min_periods=2).apply(calc_slope)[4::5]
# result.name="OBV_slope"
# obv_data = msftR[['date','OBV']]
# obv_data = pd.concat([obv_data, result],axis=1)
# obv_graph(obv_data, "bla")
#HOW TO DECIDE IF OBV IS INCREASING OR DECREASING 

# Step #4: Hide your Protective Stop Loss below the lower Bollinger Band
stopLossCondition = msftR[msftR["lower"]>=msftR["close"]]

# Step #5: Take Profit when the price breaks below the lower BB
cashInCondition = msftR[msftR["lower"]>msftR["close"]]
bb_graph(msftR, cashInCondition["date"])

#SEEMS AS THOUGH THE EXIT CONDITION IS ALWAYS THE SAME :):
big_picture(msftR,condition_1["date"], condition_2["date"], stopLossCondition["date"])
#-------------------------------------------------------------------------------------------------------------------------------------------------------