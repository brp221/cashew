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
import time

import sys
sys.path.append(r'/Users/bratislavpetkovic/Desktop/cashew/WaveSurfer/')
from helper_functions import *

commodityList = ["AAPL", "MSFT", "NVDA", "TSLA"]
timeFrameList = ["1min","5min","15min","30min","1hour","4hour","daily"]
values = ["BUY", "SCOUTING", "SELL"]
myPositionsDF = pd.DataFrame(columns=["DateBought", "DateSold", "PriceBought", "PriceSold", "Quantity"])
execfile("helper_functions.py")

#--------------------------------------------------------------------------------------------------
def trading_bot_1(time="1hour", symbol="MSFT"):
    print(symbol)
    print(time)
    priceURL = ("https://financialmodelingprep.com/api/v3/historical-chart/"+time+"/"+symbol+"?apikey=ce687b3fe0554890e65d6a5e48f601f9")
    data = pd.DataFrame.from_dict(get_jsonparsed_data(priceURL)).head(80) # 80 is approximately 80/6 = 13. days
    dataR = data[::-1]
    #______________________________GENERATE INDICATORS_______________________________
    dataR['RSI'] = talib.RSI(dataR['close'], timeperiod=14)
    dataR['upper'], dataR['mid'], dataR['lower'] = talib.BBANDS(dataR['close'], nbdevup=2, nbdevdn=2, timeperiod=20)
    dataR['OBV'] = talib.OBV(dataR['close'], dataR['volume'])
    #_____________________DATA PROCESS ( conditions 1 through 3)_____________________
    #       CONDITION 1
    condition_1 = dataR[dataR["mid"]<=dataR["close"]]
    # bb_graph(dataR, condition_1["date"])
    condition_1["condition1"]= True
    #       CONDITION 2
    condition_2 = dataR[dataR["RSI"]>50]
    # rsi_graph(dataR, condition_2["date"])
    condition_2["condition2"]= True
    #       CONDITION 3
    obv_slope = dataR["OBV"].rolling(4, min_periods=2).apply(calc_slope)[4::5]
    obv_slope.name="OBV_slope"
    obv_slope = dataR.merge(obv_slope, left_index=True, right_index=True)
    condition_3 = obv_slope[obv_slope["OBV_slope"] > 0]
    obv_data = dataR[['date','OBV']]
    # obv_graph(obv_data, obv_slope, condition_3["date"])
    condition_3["condition3"]= True
    #       CASH IN CONDITION 
    cashInCondition = dataR[dataR["lower"]>dataR["close"]]
    cashInCondition["cashInCondition"]=True
    #       MY POSITION DF
    verdictDF = dataR.merge(condition_1, how='left')
    verdictDF = verdictDF.merge(condition_2, how='left')
    verdictDF = verdictDF.merge(condition_3, how='left')
    verdictDF = verdictDF.merge(cashInCondition, how='left')
    # print("verdictDF:", verdictDF.head(10))
    verdictDF['condition1'] = verdictDF['condition1'].replace(np.nan, False)
    verdictDF['condition2'] = verdictDF['condition2'].replace(np.nan, False)
    verdictDF['condition3'] = verdictDF['condition3'].replace(np.nan, False)
    verdictDF['cashInCondition'] = verdictDF['cashInCondition'].replace(np.nan, False)
    conditions = [
        (verdictDF["condition1"]==True) & (verdictDF["condition2"]==True) & (verdictDF["condition3"]==True),    # "BUY" Scenario
        (verdictDF["cashInCondition"]==True),                              # "SELL" scenario
        (verdictDF["condition1"]==False) | (verdictDF["condition2"]==False) | (verdictDF["condition3"]==False) # "SCOUTING" scenario
    
    ]
    values = ["BUY", "SELL", "SCOUTING"]
    verdictDF["verdict"]= np.select(conditions, values, "THIS IS MISTAKE")
      
    #_____________________BIG PICTURE GRAPH_____________________
    # big_picture(dataR, obv_slope, condition_1["date"], condition_2["date"],condition_3["date"], stopLossCondition["date"], cashInCondition["date"])
    syzygy = condition_1.merge(condition_2, left_index=False, right_index=False)# syzygy is planetary alignment 
    syzygy = syzygy.merge(condition_3, left_index=False, right_index=False)
    print("syzygy: ", syzygy)
    #_____________________PERSIST RESULTS_______________________
    fileName = ("TESTING/"+symbol+"/"+symbol +"__RSI_BB_OBV.xlsx")
    with pd.ExcelWriter(fileName) as writer:
        syzygy.to_excel(writer, sheet_name=(symbol+" RESULT"), index=False)
        dataR.to_excel(writer, sheet_name=(symbol+" DATA"), index=False)
        verdictDF.to_excel(writer, sheet_name=(symbol+" POSITION"), index=False)
                    
    #_____________________PERSIST POSITION______________________
    #"BUY" and position INITIATED --> ignore? start another positon? append to currentHoldings.csv as a way to reach threshold? 
    #"SELL and position UNINITIATED --> ignore.
    #"BUY" && position UNINITIATED --> position gets initiated by persisting to temp file 
    fileName = ("TESTING/"+symbol+"/"+symbol +"__Current_Holdings.csv")
    if verdictDF["verdict"][verdictDF.index[-1]] == "BUY" :
        print("verdictDF:", verdictDF)
        print("date: ",verdictDF["date"][verdictDF.index[-1]])
        tempDF = pd.DataFrame(data={"date":[verdictDF["date"][verdictDF.index[-1]]],
                                    "close":[verdictDF["close"][verdictDF.index[-1]]],
                                    "quantity":[100]})
        tempDF.to_csv(fileName, index=False)  
    
    #"SELL" && position INITIATED --> position gets finalized ( row in myPositionDF gets computed and stored in MSFT__RSI_BB_OBV.xlsx)
    if verdictDF["verdict"][verdictDF.index[-1]] == "SELL" :        
        holdingsDF = pd.read_csv(fileName)
        print("holdingsDF:", holdingsDF)
        # PERFORM READ
        fileName = ("TESTING/"+symbol+"/"+symbol +"__Historical_Positions.csv")
        try:
            myPositionsDF = pd.read_csv(fileName)
        except FileNotFoundError:
            print("1st timer ?")
            myPositionsDF = pd.DataFrame(columns=["DateBought", "DateSold", "PriceBought", "PriceSold", "Quantity"])
            pass
        # PERFORM OVERWRITE
        myPositionsDF.append({'DateBought' : holdingsDF["date"], 
                             'DateSold' : verdictDF["date"][verdictDF.index[-1]], 
                             'PriceBought' : holdingsDF["close"], 
                             'PriceSold':verdictDF["close"][verdictDF.index[-1]], 
                             'Quantity':100}, ignore_index = True)
        myPositionsDF.to_csv(fileName, index=False)  

for i in commodityList:
    trading_bot_1("1hour", i)


#_____________________BOT NEEDS REST (:{D --> CRON JOB To be run every "time" specified above  
#--------------------------------------------------------------------------------------------------













































# time="1hour"
# symbol=commodityList[1]
# priceURL = ("https://financialmodelingprep.com/api/v3/historical-chart/"+time+"/"+symbol+"?apikey=ce687b3fe0554890e65d6a5e48f601f9")
# url = ("https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?apikey=ce687b3fe0554890e65d6a5e48f601f9")
# data = pd.DataFrame.from_dict(get_jsonparsed_data(priceURL))
# dataR = data[::-1]
# #----------------GENERATE INDICATORS-------------------------------------------------------------------------------------------------------
# dataR['RSI'] = talib.RSI(dataR['close'], timeperiod=14)
# dataR['upper'], dataR['mid'], dataR['lower'] = talib.BBANDS(dataR['close'], nbdevup=2, nbdevdn=2, timeperiod=20)
# dataR['OBV'] = talib.OBV(dataR['close'], dataR['volume'])
#---------------PLOT THE 'BIG PICTURE'--------------------------------------------------------------------------------------------------------------------
# plt.figure(figsize=(10, 10))
# fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
# ax1.set_ylabel('$')
# ax1.plot(dataR['date'],dataR['upper'], label="Up band")
# ax1.plot(dataR['date'],dataR['mid'], label='Mid band')
# ax1.plot(dataR['date'],dataR['lower'], label='Low band')
# ax1.plot(dataR['date'],dataR['close'],color = 'black')
# ax2.set_ylabel('RSI')
# ax2.plot(dataR['date'],dataR['RSI'], color='blue')
# ax2.axhline(y = 70, color = 'r', linestyle = '-')
# ax2.axhline(y = 30, color = 'r', linestyle = '-')
# ax3.plot(dataR['date'],dataR['OBV'], color='purple')
# ax1.set_title('BB and RSI')
# plt.show()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
# # inspiration: https://tradingstrategyguides.com/best-combination-of-technical-indicators/

# #RUN helper_functions.py

# # Step #1: Price needs to Break and Close above the middle Bollinger Band
# condition_1 = dataR[dataR["mid"]<=dataR["close"]]
# bb_graph(dataR, condition_1["date"])

# # Step #2: Wait for the RSI indicator to trade above the 50 level if it doesn’t already
# condition_2 = dataR[dataR["RSI"]>50]
# rsi_graph(dataR, condition_2["date"])

# # Step #3: Wait for the OBV indicator to rise. Buy at the market once you see volume confirming the price.
# obv_slope = dataR["OBV"].rolling(4, min_periods=2).apply(calc_slope)[4::5]
# obv_slope.name="OBV_slope"
# obv_slope = dataR.merge(obv_slope, left_index=True, right_index=True)
# condition_3 = obv_slope[obv_slope["OBV_slope"] > 0]
# obv_data = dataR[['date','OBV']]
# obv_graph(obv_data, obv_slope, condition_3["date"])
# #HOW TO DECIDE IF OBV IS INCREASING OR DECREASING 

# # Step #4: Hide your Protective Stop Loss below the lower Bollinger Band
# stopLossCondition = dataR[dataR["lower"]>=dataR["close"]]

# # Step #5: Take Profit when the price breaks below the lower BB
# cashInCondition = dataR[dataR["lower"]>dataR["close"]]
# bb_graph(dataR, cashInCondition["date"])
# #SEEMS AS THOUGH THE EXIT CONDITION IS ALWAYS THE SAME :): not good 
# #IF CERTAIN PROFIT REALIZED cashInCondition should be above enter position

# big_picture(dataR, obv_slope, condition_1["date"], condition_2["date"],condition_3["date"], stopLossCondition["date"], cashInCondition["date"])
#-------------------------------------------------------------------------------------------------------------------------------------------------------

# KEEP TRACK OF CURRENT PROFIT, BOUGHT AT PRICE, TIMESTAMP  
# to be placed on second page as pivot table (timestamp as the row (index))

# while T / iterate over dataset:
#     every 5, 15, 30 min period fetch data 
#     process data ( compute conditions 1-3 )
#     are conditions suitable:
#         yes: enter trade / or add line to dic counter (when counter gets to 3-5 BUY)
#             record in excel and dict
#         no: sleep(15)
#SELLING IN 2 SCENARIOS 
#STOP LOSS :( set by stopLossCondition OR when the price decreases certain percentage 
#CASH IN   :) set by cashInCondition ( tentative: OR price peaks ?  )