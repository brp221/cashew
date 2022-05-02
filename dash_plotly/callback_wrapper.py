#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 21:48:30 2022

@author: bratislavpetkovic
"""
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

import sys
sys.path.append(r'/Users/bratislavpetkovic/Desktop/cashew/dash_plotly/')
from helper_functions import  get_jsonparsed_data

import fmpsdk

apikey = "ce687b3fe0554890e65d6a5e48f601f9"

def candlestick_wrapper(symbol, indicators):
    # incorporate control for time frame: daily, 1min 5min ... 
    print("Candlestick wrapper:"+symbol+"\n")
    url = ("https://financialmodelingprep.com/api/v3/historical-price-full/" +symbol + "?apikey=ce687b3fe0554890e65d6a5e48f601f9")
    priceDF = pd.DataFrame.from_dict(get_jsonparsed_data(url)["historical"])
    priceDF["date"] = pd.to_datetime(priceDF["date"])
    
    figureData = [go.Candlestick(x=priceDF['date'],open=priceDF['open'],high=priceDF['high'],low=priceDF['low'],close=priceDF['close'])]
    for i in indicators:
        df = pd.DataFrame.from_dict(fmpsdk.technical_indicators("ce687b3fe0554890e65d6a5e48f601f9",symbol,"daily",i))
        if(len(df)>0): 
            df["date"] = pd.to_datetime(df["date"])
            # print(i,"--> ",df.iloc[0])
            line = go.Scatter(x=df["date"], y=df[i],  mode='lines',name=i)
            figureData.append(line)
    fig = go.Figure(data=figureData)
  
    fig.update_layout(
        width=1000, height = 750
    )
    return fig

def scatter_wrapper( table1, table2):
    print("Scatter wrapper\n")
    if('rank_overall_x' in table1.columns):
        del table1['rank_overall_x']
    if('rank_overall_y' in table2.columns):
        del table2['rank_overall_y']
    merged_df = table1.merge(table2)
    fig = px.scatter(merged_df, x="rank_overall_x", y="rank_overall_y",
    	         size="marketCap", color="sector",
                     hover_name="Symbol", log_x=True, size_max=60)
    
    # fig.update_layout(
    #     width=1100, height = 700 
    # )
    #fig.show()
    return fig
    
def radar_wrapper(symbol, peerSymbol):
    print("Radar symbol:"+symbol)
    print("Radar peerSymbol:"+peerSymbol)
    outlookURL = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol="+symbol+"&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    companyOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL)["rating"])
    outlookURL2 = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol="+peerSymbol+"&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    peerOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL2)["rating"])
    x =  [companyOutlook.ratingDetailsDCFScore[0], companyOutlook.ratingDetailsROEScore[0], companyOutlook.ratingDetailsROAScore[0], 
                   companyOutlook.ratingDetailsDEScore[0], companyOutlook.ratingDetailsPEScore[0], companyOutlook.ratingDetailsPBScore[0]]
    x2 =  [peerOutlook.ratingDetailsDCFScore[0], peerOutlook.ratingDetailsROEScore[0], peerOutlook.ratingDetailsROAScore[0], 
                    peerOutlook.ratingDetailsDEScore[0], peerOutlook.ratingDetailsPEScore[0], peerOutlook.ratingDetailsPBScore[0]]
    categories = ["DCF", "ROE", "ROA", "D/E", "P/E", "P/B"]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
          r=x,
          theta=categories,
          line_color = '#7851a9',
          marker_color = "#7851a9", 
          fill='toself',
          name=symbol
    ))
    fig.add_trace(go.Scatterpolar(
          r=x2,
          theta=categories,
          line_color = 'black',
          marker_color="#5e8078",
          fill='toself',
          name=peerSymbol
    ))
    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 5]
        )),
      legend=dict(yanchor="top",y=1.4,xanchor="left",x=0.25), width=330,height=330
      # showlegend=True#, width=300,height=300
    )

    return fig

def quarter_earnings_wrapper(symbol):
    print("Quarter Earnings wrapper:"+symbol)
    # TIME SERIES
    incomeStatURLquarter = ("https://financialmodelingprep.com/api/v3/income-statement/"+symbol+"?period=quarter&limit=16&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    incomeStatDFQuart = pd.DataFrame.from_dict(get_jsonparsed_data(incomeStatURLquarter))
    
    x1 = incomeStatDFQuart.date
    y1 = incomeStatDFQuart.netIncome
    
    x2 = incomeStatDFQuart.date
    y2 = incomeStatDFQuart.revenue
    
       
    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1,
                        mode='lines+markers',
                        name='Revenue'))
    fig.add_trace(go.Scatter(x=x2, y=y2,
                         mode='lines+markers',
                         name='NetIncome'))
    fig.update_layout( 
        width=500,height=420,
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1)
    )
    return fig
    
def annual_earnings_wrapper(symbol):
    print("Annual Earnings wrapper:"+symbol)
    # url = ("https://financialmodelingprep.com/api/v3/analyst-estimates/"+symbol+"?limit=4&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    # estimatedEarningsDF = pd.DataFrame.from_dict(get_jsonparsed_data(url))

    # QUARTER : api/v3/income-statement/AAPL?period=quarter&limit=400&apikey=ce687b3fe0554890e65d6a5e48f601f9
    incomeStatURL = ("https://financialmodelingprep.com/api/v3/income-statement/"+symbol+"?limit=4&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    incomeStatementDF  = pd.DataFrame.from_dict(get_jsonparsed_data(incomeStatURL))
    years = ['2019', '2020', '2021', '2022']
    revenue = list(incomeStatementDF.revenue)
    revenue.reverse()
    netIncome = list(incomeStatementDF.netIncome)
    netIncome.reverse() 
    ebitda = list(incomeStatementDF.ebitda)
    ebitda.reverse()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years,
        y=revenue,
        name='Revenue',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=years,
        y=netIncome,
        name='Net Income',
        marker_color='lightsalmon'
    )),
    fig.add_trace(go.Bar(
        x=years,
        y=ebitda,
        name='EBITDA',
        marker_color='purple'
    ))
    
    fig.update_layout(barmode='group', xaxis_tickangle=-45,legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))#, width=450,height=400)
    #fig.show()
    return fig
    
   
def insider_trade_wrapper(symbol):
    print("Insider Trading wrapper:"+symbol)
    # free acquisitions to be colored. Also outline importance of the seller/buyer in scope of company
    # maybe trim into a couple of diffferent types of people (e.g. CEO, director, common employeee ...)
    url = ("https://financialmodelingprep.com/api/v4/insider-trading?symbol="+symbol+"&page=0&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    insideTradingData = pd.DataFrame.from_dict(get_jsonparsed_data(url))
    insideTradingData['securityTransactedTrue'] = insideTradingData.securitiesTransacted
    insideTradingData.loc[insideTradingData.acquistionOrDisposition == "D", 'securityTransactedTrue'] = insideTradingData.securitiesTransacted * -1 
    conditionlist = [
        (insideTradingData['typeOfOwner'].str.contains("10 percent owner")),
        (insideTradingData['typeOfOwner'].str.contains("director")) ,
        (insideTradingData['typeOfOwner'].str.contains("officer")) & (~insideTradingData['typeOfOwner'].str.contains("director")),
        (insideTradingData['typeOfOwner'].str.contains("other"))]
    choicelist = [ '10 % owner','director', 'officer', 'other']
    insideTradingData['employeeType'] = np.select(conditionlist, choicelist, default='Unknown')
    barData = insideTradingData.groupby(['employeeType','acquistionOrDisposition'])['securityTransactedTrue'].sum().reset_index()
    fig = px.bar(barData, y='securityTransactedTrue', x='employeeType',color='acquistionOrDisposition', text='securityTransactedTrue')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return fig
    
    
def growth_metric_wrapper(symbol):
    finGrowthQuartURL = ("https://financialmodelingprep.com/api/v3/financial-growth/"+symbol+"?period=quarter&limit=60&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    finGrowthQuart = pd.DataFrame.from_dict(get_jsonparsed_data(finGrowthQuartURL))
    x = finGrowthQuart.date
    revGrowth = finGrowthQuart.revenueGrowth
    netIncGrowth = finGrowthQuart.netIncomeGrowth

    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=revGrowth,
                        mode='lines+markers',
                        name='RevenueGrowth'))
    fig.add_trace(go.Scatter(x=x, y=netIncGrowth,
                         mode='lines+markers',
                         name='NetIncomeGrowth'))
    fig.update_layout( legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))#width=650,height=450)

    return fig

def growth_future_wrapper(symbol):
    #/api/v3/analyst-estimates/AAPL?period=quarter&limit=30
    #/api/v3/analyst-estimates/"+symbol+"?limit=4&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    earningsEstimatesURL = ("https://financialmodelingprep.com/api/v3/analyst-estimates/"+symbol+"?period=quarter&limit=16&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    estimatedEarnings= pd.DataFrame.from_dict(get_jsonparsed_data(earningsEstimatesURL))
    actualEarningsURL = ("https://financialmodelingprep.com/api/v3/income-statement/"+symbol+"?period=quarter&limit=16&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    actualEarnings= pd.DataFrame.from_dict(get_jsonparsed_data(actualEarningsURL))
    
    x1 = estimatedEarnings.date
    y1 = estimatedEarnings.estimatedRevenueAvg.astype(int)
    
    x2 = actualEarnings.date
    y2 = actualEarnings.revenue
    
    
    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1,
                        mode='lines+markers',
                        name='RevenueEstimate'))
    fig.add_trace(go.Scatter(x=x2, y=y2,
                         mode='lines+markers',
                         name='RevenueActual'))
    fig.update_layout( legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))#width=650,height=450)

    return fig


# def test_wrapper(symbol, indicators):
#     figureData=[]
#     print(indicators)
#     print(len(indicators))
#     for i in indicators:
#         df = pd.DataFrame.from_dict(fmpsdk.technical_indicators("ce687b3fe0554890e65d6a5e48f601f9",symbol,"daily",i))
#         if(len(df)>0): 
#             print(df.columns)
#             df["date"] = pd.to_datetime(df["date"])
#             print(i,"--> ",df.iloc[0])
#             print("\n\n")
#             line = go.Scatter(x=df["date"], y=df[i],  mode='lines',name=i)
#             figureData.append(line)
#     fig = go.Figure(data=figureData)
  
#     fig.update_layout(
#         width=1000, height = 750
#     )
#     return fig 

    


# def debt_wrapper(symbol):
#     #debt paid off yearly vs increasing debt. 