#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 18:09:15 2022

@author: bratislavpetkovic
"""
# For Python 3.0 and later
from urllib.request import urlopen
import certifi
import json

import plotly.graph_objects as go

import pandas as pd
from datetime import datetime

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------


randomStock = "NVDA"
url = ("https://financialmodelingprep.com/api/v3/historical-price-full/" +randomStock + "?apikey=ce687b3fe0554890e65d6a5e48f601f9")
priceDF = pd.DataFrame.from_dict(get_jsonparsed_data(url)["historical"])

priceDF["date"] = pd.to_datetime(priceDF["date"])

fig = go.Figure(data=[go.Candlestick(x=priceDF['date'],
                open=priceDF['open'],
                high=priceDF['high'],
                low=priceDF['low'],
                close=priceDF['close'])])

# fig.show()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv') # replace with your own data source
fig = go.Figure(go.Candlestick(
    x=df['Date'],
    open=df['AAPL.Open'],
    high=df['AAPL.High'],
    low=df['AAPL.Low'],
    close=df['AAPL.Close']
))




#-------------------------------------------------------------------------------------------------------------------------------------------------------------
outlookURL = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol=AAPL&apikey=ce687b3fe0554890e65d6a5e48f601f9")
aaplOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL)["rating"])

outlookURL2 = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol=MSFT&apikey=ce687b3fe0554890e65d6a5e48f601f9")
peerOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL2)["rating"])

outlookURL3 = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol=GOOGL&apikey=ce687b3fe0554890e65d6a5e48f601f9")
peerOutlook3  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL3)["rating"])

x =  [aaplOutlook.ratingDetailsDCFScore[0], aaplOutlook.ratingDetailsROEScore[0], aaplOutlook.ratingDetailsROAScore[0], 
               aaplOutlook.ratingDetailsDEScore[0], aaplOutlook.ratingDetailsPEScore[0], aaplOutlook.ratingDetailsPBScore[0]]
x2 =  [peerOutlook.ratingDetailsDCFScore[0], peerOutlook.ratingDetailsROEScore[0], peerOutlook.ratingDetailsROAScore[0], 
               peerOutlook.ratingDetailsDEScore[0], peerOutlook.ratingDetailsPEScore[0], peerOutlook.ratingDetailsPBScore[0]]
x3 =  [peerOutlook3.ratingDetailsDCFScore[0], peerOutlook3.ratingDetailsROEScore[0], peerOutlook3.ratingDetailsROAScore[0], 
               peerOutlook3.ratingDetailsDEScore[0], peerOutlook3.ratingDetailsPEScore[0], peerOutlook3.ratingDetailsPBScore[0]]

categories = ["DCF", "ROE", "ROA", "D/E", "P/E", "P/B"]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
      r=x,
      theta=categories,
      fill='toself',
      name='Product A'
))
fig.add_trace(go.Scatterpolar(
      r=x2,
      theta=categories,
      fill='toself',
      name='Product B'
))
fig.add_trace(go.Scatterpolar(
      r=x3,
      theta=categories,
      fill='toself',
      name='Product C'
))

fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 5]
    )),
  showlegend=False
)

fig.show()





#-------------------------------------------------------------------------------------------------------------------------------------------------------------






#-------------------------------------------------------------------------------------------------------------------------------------------------------------







#-------------------------------------------------------------------------------------------------------------------------------------------------------------









#-------------------------------------------------------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------



