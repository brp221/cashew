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
import sys
sys.path.append(r'/Users/bratislavpetkovic/Desktop/cashew/WaveSurfer/')

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

def calc_slope(x):
    slope = np.polyfit(range(len(x)), x, 1)[0]
    return slope
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt

def bb_graph(df, condition):
    plt.rcParams["figure.figsize"] = [24,16]
    plt.plot(df['date'],df['upper'], label="Up band")
    plt.plot(df['date'],df['mid'], label='Mid band')
    plt.plot(df['date'],df['lower'], label='Low band')
    plt.plot(df['date'],df['close'],color = 'black')
    
    for i in range(0,len(condition)): 
        plt.axvline(condition.iloc[i])
    plt.show()

def rsi_graph(df, condition):
    plt.rcParams["figure.figsize"] = [24,16]
    plt.plot(df['date'],df['RSI'], color='blue')
    for i in range(0,len(condition)): 
        plt.axvline(condition.iloc[i])
    plt.show()

def obv_graph(df, df_slope, condition):
    plt.rcParams["figure.figsize"] = [24,16]
    plt.plot(df['date'],df['OBV'], color='red')
    plt.plot(df_slope['date'],df_slope['OBV_slope'], color='blue')
    for i in range(0,len(condition)): 
        plt.axvline(condition.iloc[i], color="green")
    plt.show()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def big_picture(df, df_slope,condition1, condition2, condition3, stopLossCondition, cashInCondition):
    plt.rcParams["figure.figsize"] = [32,24]
    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
    ax1.plot(df['date'],df['upper'], label="Up band", color='green')
    ax1.plot(df['date'],df['mid'], label='Mid band', color='orange')
    ax1.plot(df['date'],df['lower'], label='Low band', color='red')
    ax1.plot(df['date'],df['close'],color = 'blue')
    for i in range(0,len(condition1)): 
        ax1.axvline(condition1.iloc[i], color="green")
    for i in range(0,len(stopLossCondition)): 
        ax1.axvline(stopLossCondition.iloc[i], color="red")
    for i in range(0,len(cashInCondition)): 
        ax1.axvline(cashInCondition.iloc[i], color="blue")
    
    ax2.plot(df['date'],df['RSI'], color='blue')
    for i in range(0,len(condition2)): 
        ax2.axvline(condition2.iloc[i])
    ax2.axhline(y = 70, color = 'r', linestyle = '-')
    ax2.axhline(y = 30, color = 'r', linestyle = '-')
    
    # ax3.plot(df['date'],df['OBV'], color='purple')
    # ax3.plot(df['date'],df['OBV'], color='purple')
    ax3.plot(df['date'],df['OBV'], color='red')
    ax3.plot(df_slope['date'],df_slope['OBV_slope'], color='blue')
    for i in range(0,len(condition3)): 
        plt.axvline(condition3.iloc[i], color="blue")
    
    ax1.set_title('BB, RSI, OBV Strategy')
    plt.show()



#-------------------------------------------------------------------------------------------------------------------------------------------------------------






#-------------------------------------------------------------------------------------------------------------------------------------------------------------







#-------------------------------------------------------------------------------------------------------------------------------------------------------------









#-------------------------------------------------------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------



