#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  3 11:21:35 2022

@author: bratislavpetkovic
"""
from helper_functions import *
import pandas as pd 

def portfolio_generator(df, risk_level, diversification_level, preferred_sectors, investment_amount):
    # 0. DATA MASSAGING AND SETUP
    print("risk_level", risk_level)
    print("diversification_level", diversification_level)
    print("preferred_sectors", preferred_sectors)
    print("investment_amount", investment_amount)
    portfolio_size = [5]
    if(diversification_level=="low"):
        portfolio_size = [4,5,6]
    elif(diversification_level=="medium"):
        portfolio_size = [6,7,9]
    if(diversification_level=="high"):
        portfolio_size = [9,10,11]

    df_new = df.loc[df["sector"].isin(preferred_sectors),]
    
    # 1. JOIN DATA, COMPUTE RANKS AND SORT BY BEST RANK
    # print("rank_overall_ar:", df_new["rank_overall_ar"] )
    # print("rank_overall_hc:", df_new["rank_overall_hc"] )
    df_new["RANK_TOTAL"] = df_new["rank_overall_ar"] + df_new["rank_overall_hc"]
    df_new=df_new.sort_values(by=['RANK_TOTAL'], ascending=False)
    
    # 2. "FISH" OUT THE BEST n=portfolio_size RANKS 
    catchDF = df_new.head(portfolio_size[2])
    print("catchDF:")
    print(catchDF)
    
    #3. GET PRICE FOR EACH SYMBOL
    priceDF = pd.DataFrame(columns = ['symbol', 'price', 'volume'])
    for i in catchDF["Symbol"]:
        url = ("https://financialmodelingprep.com/api/v3/quote-short/"+i+"?apikey=ce687b3fe0554890e65d6a5e48f601f9")
        priceDF = pd.concat([priceDF,pd.DataFrame.from_dict(get_jsonparsed_data(url))])
    priceDF.rename(columns={'symbol': 'Symbol'}, inplace=True)
    print("priceDF:")
    print(priceDF)
    totalDF = catchDF.merge(priceDF)
    print("totalDF:")
    print(totalDF)
    
    #4. ASSIGN WEIGHTS ()
    weights=weights_assigner(portfolio_size[2],investment_amount,totalDF )
    print(weights)
    totalDF["totalDollars"] = weights
    totalDF["quantity"] = totalDF["totalDollars"]/totalDF["price"]
    #5. GET PRICE TARGETS SO THAT CLIENT KNOWS WHEN TO SELL ( give client ability to filter price targets by newsPublisher and timeframe?)
    
    # helper FUNCTION comingSoon
    return totalDF
    
# helper function to join the given tables and then to rank them according to 2-3 categories?
def investment_type(dict_df):
    #COMPUTE RANKS using df preparers
    df_x = analyst_rating_preparer(dict_df["Analyst Rating"])
    df_y = health_preparer(dict_df["Healthiest"])
    df = df_x.merge(df_y)
    
    print("investment_type result: ",df.head())
    return df
    
# helper function to assign weights of wallet to stocks in order of best to worst
def weights_assigner(portfolio_size,investment_amount, totalDF):  
    # Assign weights based on rank or based on price_target minus current price, OR Both?
    # intuitively, best stocks will hold the most weight. Figure out some distribution e.g. 
    # ideally, round the quantities so that client buys whole stocks. 
    # print("portfolio_size==totalDF.size", portfolio_size==len(totalDF))    
    
    #METHOD 1 BY RANK
    total = sum(list(range(1,portfolio_size+1)))
    weights = []
    for i in range(0,portfolio_size+1):
        # pd.concat([weights,i/total ])
        weights.append(i/total)
    weights.reverse()
    weights.pop()
    weights_dollars = [w * investment_amount for w in weights]
    #METHOD 2 BY PRICE TARGETS (ComingSoon)
    #METHOD 3 HYBRID (ComingSoon)
    return weights_dollars
    
    
    
    
    
    
    