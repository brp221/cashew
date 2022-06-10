
"""Mon May  9 16:03:46 2022"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import fmpsdk
import talib 
import matplotlib.pyplot as plt
import time
import os
import sys
sys.path.append(r'/Users/bratislavpetkovic/Desktop/cashew/WaveSurfer/')
from helper_functions import *

commodityList = ["AAPL", "AMZN","MSFT", "BABA", "NVDA", "TSLA", "GOOGL", "RBLX", "DKNG"]
timeFrameList = ["1min","5min","15min","30min","1hour","4hour","daily"]

directory = "/Users/bratislavpetkovic/Desktop/cashew/WaveSurfer/RSI_BB_OBV/"
with open((directory+"helper_functions.py")) as infile:
    exec(infile.read())
#--------------------------------------------------------------------------------------------------

def trading_bot_1(time="1hour", symbol="MSFT"):
    print("#--------------------------------------------------------------------------------------------------")
    print(symbol)
    print(time)
    priceURL = ("https://financialmodelingprep.com/api/v3/historical-chart/"+time+"/"+symbol+"?apikey=ce687b3fe0554890e65d6a5e48f601f9")
    data = pd.DataFrame.from_dict(get_jsonparsed_data(priceURL)).head(60) # 80 is approximately 80/6 = 13. days for 1 hour
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
    # print("syzygy: ", syzygy)
    #_____________________PERSIST RESULTS_______________________
    testing_dir = (directory+"TESTING/"+symbol+"/")
    storageFile = (testing_dir+"/"+symbol +"__RSI_BB_OBV.xlsx")
    if not os.path.exists(testing_dir):      # Create a new directory because it does not exist 
      os.makedirs(testing_dir)
    with pd.ExcelWriter(storageFile) as writer:
        syzygy.to_excel(writer, sheet_name=(symbol+" BUY POINTS"), index=False)
        verdictDF.to_excel(writer, sheet_name=(symbol+" ALL POINTS"), index=False)
                    
    #_____________________PERSIST POSITION______________________
    holdingsFile = (testing_dir+symbol +"__Current_Holdings.csv")
    print("file: ", holdingsFile)
    try:
      holdingsDF = pd.read_csv(holdingsFile) # exception gets thrown, jump to except block
      currentProfit =  (data["close"][0]  - holdingsDF["close"][0]) * holdingsDF["quantity"][0]
      print("currentProfit: ", currentProfit )
      quantitySelected = int( (400 / verdictDF["close"][verdictDF.index[-1]]) * -1 // 1 * -1) #$ to get to 400 $ per commodity 
      print("quantitySelected: ", quantitySelected )    
      if verdictDF["verdict"][verdictDF.index[-1]] == "BUY" :
          print("BUY, position initiated")
          holdingsDF.loc[len(holdingsDF)] = [verdictDF["date"][verdictDF.index[-1]],verdictDF["close"][verdictDF.index[-1]],quantitySelected]
          holdingsDF.to_csv(holdingsFile, index=False)   
          
      if verdictDF["verdict"][verdictDF.index[-1]] == "SELL" or currentProfit > 800:   # or currentProfit <-300:          
          # at this point, it has been established that the holdings file exists bc it is a parent requisite/dependancy 
          sell_reasoning = "ALGO" if verdictDF["verdict"][verdictDF.index[-1]] == "SELL" else "STOP-LOSS"
          print("SELL")
          os.remove(holdingsFile)
          closedPositionsFile = (testing_dir+symbol +"__Historical_Positions.csv")
          print("closedPositionsFile: ", closedPositionsFile)
          try:
              myPositionsDF = pd.read_csv(closedPositionsFile)
              myPositionsDF.loc[len(myPositionsDF)] = [holdingsDF["date"][0],
                                                       verdictDF["date"][verdictDF.index[-1]],
                                                       holdingsDF["close"][0],
                                                       verdictDF["close"][verdictDF.index[-1]],
                                                       holdingsDF["quantity"][0],
                                                       sell_reasoning]
              print("NON_VIRGIN position closed and persisted ")
              myPositionsDF.to_csv(closedPositionsFile, index=True) 
          except FileNotFoundError:
              myPositionsDF = pd.DataFrame(data={'DateBought' :holdingsDF["date"][0], 
                                                 'DateSold' : verdictDF["date"][verdictDF.index[-1]], 
                                                 'PriceBought' : holdingsDF["close"][0], 
                                                 'PriceSold':verdictDF["close"][verdictDF.index[-1]], 
                                                 'Quantity':holdingsDF["quantity"][0],
                                                 'sell-reason': sell_reasoning})
              print("VIRGIN position closed and persisted ")
              myPositionsDF.to_csv(closedPositionsFile, index=True) 
              
    except FileNotFoundError:
      quantitySelected = int( (400 / verdictDF["close"][verdictDF.index[-1]]) * -1 // 1 * -1) #$ to get to 400 $ per commodity 
      print("quantitySelected: ", quantitySelected)
      if verdictDF["verdict"][verdictDF.index[-1]] == "BUY" :
          print("date: ",verdictDF["date"][verdictDF.index[-1]])
          print(verdictDF["date"][verdictDF.index[-1]])
          print("BUY, position UNinitiated")
          holdingsDF = pd.DataFrame(data={"date":[verdictDF["date"][verdictDF.index[-1]]],
                                      "close":[verdictDF["close"][verdictDF.index[-1]]],
                                      "quantity":[quantitySelected]})
          
          holdingsDF.to_csv(holdingsFile, index=False)   
    print("#--------------------------------------------------------------------------------------------------")
#--------------------------------------------------------------------------------------------------

for i in commodityList:
    trading_bot_1("5min", i)


#_____________________BOT NEEDS REST (:{D --> CRON JOB To be run every "time" specified above  
#--------------------------------------------------------------------------------------------------




# bot can be improved (or made more precise ) by specifying the extent to which the conditions are True
# maybe even setting threshholds 







































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