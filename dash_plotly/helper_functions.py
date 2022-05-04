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
import numpy as np

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


import plotly.graph_objects as go

import pandas as pd
from datetime import datetime
import sys
sys.path.append(r'/Users/bratislavpetkovic/Desktop/cashew/dash_plotly/')


#-------------------------------------------------------------------------------------------------------------------------------------------------------------

#EVENTUALLY HAVE THE PREPARERS HAVE A CLIENT CUSTOMIZABLE RANKING PROCESS
def health_preparer(df):
    df["rank_ROA"] =  df["ROA"].rank(pct=True)
    df["rank_ROE"] =  df["ROE"].rank(pct=True)
    df["rank_piotroski"] =  df["piotroskiScore"].rank(pct=True)
    df["rank_DE"] =  df["debtEquityRatio"].rank(ascending=False, pct=True)
    df["rank_overall_hc"] = ((0.25* df["rank_ROA"]) + (0.25* df["rank_ROE"]) + (0.25* df["rank_piotroski"]) + (0.25* df["rank_DE"]))
    print("rank_overall_hc : ", df["rank_overall_hc"])
    return df

def discount_preparer(df):
    df["DCF_Discount"] = (df["DCFminusPrice"]) / (df["Price_BV"])
    df["yearly_discount"] = (df["yearHigh"] - df["price"]) / df["price"] 
    df["percToFloor"] = (df["price"] - df["yearLow"]) / df["price"] 
    df["InsiderPurchased/TransCount"] = df["InsiderPurchased"] / df["TransactionCount"]
    df['InsiderPurchased/TransCount'] = df['InsiderPurchased/TransCount'].replace(np.nan, 0)

    df["rank_1_bv"] =  df["DCF_Discount"].rank(pct=True)
    df["rank_2_bv"] =  df["yearly_discount"].rank(pct=True)
    df["rank_3_bv"] =  df["InsiderPurchased/TransCount"].rank(pct=True)
    df["rank_overall_bv"] = ((0.40* df["rank_1_bv"]) + (0.40* df["rank_2_bv"]) + (0.20* df["rank_3_bv"]) )
    # print("discount_preparer : ", len(df))
    return df

def growers_preparer(df):
    df["rank_1_bg"] = df.netIncomeGrowth2Yr.rank(pct=True)
    df["rank_2_bg"] = df.revGrowth1Yr.rank(pct=True)
    df["rank_3_bg"] = df.freeCashFlowGrowth.rank(pct=True)
    df["rank_4_bg"] = df.debt_repayment.rank(pct=True, ascending=False)
    df["rank_overall_bg"] = ((0.25*df.rank_1_bg) + (0.25*df.rank_2_bg) + (0.25*df.rank_3_bg) + (0.25*df.rank_4_bg))
    # print("growers_preparer : ", len(df))
    return df

def analyst_rating_preparer(df):
    df["rank_overall_ar"] =  df["AnalystRating"].rank(pct=True)
    print("rank_overall_ar:",df["rank_overall_ar"])
    return df


#-------------------------------------------------------------------------------------------------------------------------------------------------------------





#-------------------------------------------------------------------------------------------------------------------------------------------------------------






#-------------------------------------------------------------------------------------------------------------------------------------------------------------






#-------------------------------------------------------------------------------------------------------------------------------------------------------------







#-------------------------------------------------------------------------------------------------------------------------------------------------------------









#-------------------------------------------------------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------



