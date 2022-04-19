#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 21:48:30 2022

@author: bratislavpetkovic
"""
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px

import sys
sys.path.append(r'/Users/bratislavpetkovic/Desktop/cashew/dash_plotly/')
from helper_functions import  get_jsonparsed_data

def candlestick_wrapper(symbol):
    print("Candlestick wrapper:"+symbol+"\n")
    url = ("https://financialmodelingprep.com/api/v3/historical-price-full/" +symbol + "?apikey=ce687b3fe0554890e65d6a5e48f601f9")
    priceDF = pd.DataFrame.from_dict(get_jsonparsed_data(url)["historical"])
    priceDF["date"] = pd.to_datetime(priceDF["date"])
    fig = go.Figure(data=[go.Candlestick(x=priceDF['date'],
                    open=priceDF['open'],
                    high=priceDF['high'],
                    low=priceDF['low'],
                    close=priceDF['close'])])
    fig.update_layout(
        width=800, height = 600
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
    
    fig.update_layout(
        width=1100, height = 700
    )
    #fig.show()
    return fig
    
def radar_wrapper(symbol):
    print("Radar wrapper:"+symbol)
    outlookURL = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol="+symbol+"&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    companyOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL)["rating"])
    # outlookURL2 = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol=MSFT&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    # peerOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL2)["rating"])
    x =  [companyOutlook.ratingDetailsDCFScore[0], companyOutlook.ratingDetailsROEScore[0], companyOutlook.ratingDetailsROAScore[0], 
                   companyOutlook.ratingDetailsDEScore[0], companyOutlook.ratingDetailsPEScore[0], companyOutlook.ratingDetailsPBScore[0]]
    # x2 =  [peerOutlook.ratingDetailsDCFScore[0], peerOutlook.ratingDetailsROEScore[0], peerOutlook.ratingDetailsROAScore[0], 
    #                peerOutlook.ratingDetailsDEScore[0], peerOutlook.ratingDetailsPEScore[0], peerOutlook.ratingDetailsPBScore[0]]
    categories = ["DCF", "ROE", "ROA", "D/E", "P/E", "P/B"]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
          r=x,
          theta=categories,
          fill='toself',
          name='Product A'
    ))
    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 5]
        )),
      showlegend=False, width=400,height=400
    )

    return fig

def quarter_earnings_wrapper(symbol):
    print("Quarter Earnings wrapper:"+symbol)
    # TIME SERIES
    incomeStatURLquarter = ("https://financialmodelingprep.com/api/v3/income-statement/"+symbol+"?period=quarter&limit=16&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    incomeStatDFQuart = pd.DataFrame.from_dict(get_jsonparsed_data(incomeStatURLquarter))

    incomeStatDFQuart.index = pd.to_datetime(incomeStatDFQuart.date)

    # df = px.data.stocks()
    fig = px.line(incomeStatDFQuart, x="date", y=['revenue','ebitda' ,'netIncome'],
                  hover_data={"date": "|%B %d, %Y"},
                  title='custom tick labels')
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y") 
    #fig.show()
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
    
    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45, width=450,height=600)
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
    fig = go.Figure(go.Bar(
                x=list(insideTradingData.securityTransactedTrue),
                y=list(insideTradingData.typeOfOwner),
                orientation='h'))
    fig.update_layout( width=600,height=400)
    return fig
    
    
    