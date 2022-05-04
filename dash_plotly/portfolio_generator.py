#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  3 11:21:35 2022

@author: bratislavpetkovic
"""
from helper_functions import *
#INPUTS:
    #diversification_level : low, medium, high
        # for high include crypto perhaps?
    #investment_style : 1 one of the 4 tables potentially, or 2 of the tables combined w another table sucha s health and/or analyst rating 
    #risk_level : altmanZthreshhold / O-score ---> low,medium,high
        # O-score using https://en.wikipedia.org/wiki/Ohlson_O-score#:~:text=The%20Ohlson%20O%2Dscore%20for,score%20for%20predicting%20financial%20distress. 
    #preferred_sectors: sectors to filter by ( break norm if insufficient)
    #investment_amount: to be a helper function to main generator function. 
        #perhaps factorized 1 means BG 2 means BV , 3 means BG.Join(AR), 4 means BV.Join(HC) ... DEF a helper function or data preparer function
        # used to calculate weight of each company in the stock. 
        # intuitively, best stocks will hold the most weight. Figure out some distribution e.g. 
            # E.G. :out of 8 stocks the weight of 1st stock will be 8/ epsiolon(1 to 8), 
                                        #weight of 2nd stock will be 7/ epsilon(1 to 8),
            # Round to nearest stock if that stock is below a certain threshhold 
    
#ALGO:

    #OUTPUT SHOULD BE A DICTIONARY 4 CARD FORMAT, EACH STOCK NEEDS TO BE BOUGHT NEEDS TO LOCK FANCY & DIVINE 

def portfolio_generator(df, risk_level, diversification_level, preferred_sectors, investment_amount, investment_style):
    # 0. DATA MASSAGING AND data setup
    portfolio_size = [5]
    if(diversification_level=="low"):
        portfolio_size = [4,5,6]
    elif(diversification_level=="medium"):
        portfolio_size = [6,7,9]
    if(diversification_level=="high"):
        portfolio_size = [9,10,11]
        return portfolio_size

    df_new=df[df.sector.isin(preferred_sectors)]#.to_dict('records')
    # print(df_new.head())
    print("rank_overall_ar:", df_new["rank_overall_ar"] )
    print("rank_overall_hc:", df_new["rank_overall_hc"] )
    df_new["RANK_TOTAL"] = df_new["rank_overall_ar"] + df_new["rank_overall_hc"]
    # print(df_new.head())
    df_new=df_new.sort_values(by=['RANK_TOTAL'], ascending=False)
    print("RANK_TOTAL:", df_new["RANK_TOTAL"] )
    print(df_new.head())
    #USE HELPER FUNCTION TO ASSIGN WEIGHS ($$$) 
    # weights_assigner(diversification_level,investment_amount,symbols )
    return df_new
    
# # helper function to join the given tables and then to rank them according to 2-3 categories?
def investment_type(list_df):
    #COMPUTE RANKS using df preparers
    df_x = analyst_rating_preparer(list_df[0])
    df_y = health_preparer(list_df[1])
    df = df_x.merge(df_y)
    
    print(df.head())
    return df
    
# helper function to assign weights of wallet to stocks in order of best to worst
def weights_assigner(diversification_level,investment_amount,symbols):  
    
    #FISH OUT THE BEST RANKS      
    
    
    
    
    
    
    
    