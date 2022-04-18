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

from sqlalchemy import column
from sqlalchemy import create_engine
# from sqlalchemy import select
from sqlalchemy import table

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

def fetch_symbol_metadata():
    # METADATA
    symbol_metadata = table("symbol_metadata", column("symbol"), column("companyName"), column("sector"),column("industry"), column("country"), 
                           column("exchangeShortName"), column("price"), column("marketCap"), column("isEtf"))
    symbol_metadata_stmt = symbol_metadata.select() #.where(analyst_rating.c.name == 'Bob')
    symbol_metadata_df = pd.read_sql_query(symbol_metadata_stmt, engine)
    symbol_metadata_df["Symbol"] = symbol_metadata_df["symbol"]
    del symbol_metadata_df["symbol"]
    
    
import plotly.graph_objects as go

import pandas as pd
from datetime import datetime


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






#-------------------------------------------------------------------------------------------------------------------------------------------------------------






#-------------------------------------------------------------------------------------------------------------------------------------------------------------







#-------------------------------------------------------------------------------------------------------------------------------------------------------------









#-------------------------------------------------------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------



