#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 17:16:27 2022

@author: bratislavpetkovic
"""

from dash import Dash, dash_table
from dash import html
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output  

import pandas as pd
import numpy as np

import sys
sys.path.append(r'/Users/bratislavpetkovic/Desktop/cashew/dash_plotly/')

from helperFunctions import  get_jsonparsed_data
from db_helpers import fetch_symbol_metadata, fetch_analyst_rating, fetch_biggest_growers, fetch_best_value, fetch_healthiest_companies
from ui_styles import tabs_styles
from callback_wrapper import candlestick_wrapper, scatter_wrapper, radar_wrapper, quarter_earnings_wrapper, annual_earnings_wrapper, insider_trade_wrapper


app = Dash()   #initialising dash app

# METADATA
symbol_metadata_df = fetch_symbol_metadata()

# ANALYST RATING
analyst_rating_df = fetch_analyst_rating()
analyst_rating_metadata_df =  analyst_rating_df.merge(symbol_metadata_df)

# BIGGEST GROWERS
biggest_growers_df = fetch_biggest_growers()
biggest_growers_metadata_df =  biggest_growers_df.merge(symbol_metadata_df)


# BEST VALUE
best_value_df = fetch_best_value()
best_value_metadata_df =  best_value_df.merge(symbol_metadata_df)


# HEALTHIEST COMPANIES
healthiest_companies_df = fetch_healthiest_companies()
healthiest_companies_metadata_df =  healthiest_companies_df.merge(symbol_metadata_df)



dash_table1 = dash_table.DataTable(
    analyst_rating_df.to_dict('records'),
    [{"name": i, "id": i} for i in analyst_rating_df.columns],
    page_size=15, id = "DT_analysts"
    )
dash_table2 = dash_table.DataTable(
    healthiest_companies_metadata_df.to_dict('records'),
    [{"name": i, "id": i} for i in ['Symbol', 'ROA', 'currentRatio','piotroskiScore','netProfitMargin','sector']],
    page_size=15, id = "DT_healthiest"
    )
dash_table3 = dash_table.DataTable(
    best_value_df.to_dict('records'),
    [{"name": i, "id": i} for i in best_value_df.columns],
    page_size=15, id = "DT_discount",
    style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        'lineHeight': '15px'
    },
    fill_width=False
    )
dash_table4 = dash_table.DataTable(
    biggest_growers_df.to_dict('records'),
    [{"name": i, "id": i} for i in biggest_growers_df.columns],
    page_size=15, id = "DT_growers",
    style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        'lineHeight': '15px'
    },
    fill_width=False
    )


stockSymbol= "NVDA"
url = ("https://financialmodelingprep.com/api/v4/insider-trading?symbol="+stockSymbol+"&page=0&apikey=ce687b3fe0554890e65d6a5e48f601f9")
insideTradingData = pd.DataFrame.from_dict(get_jsonparsed_data(url))
insideTradingData['securityTransactedTrue'] = insideTradingData.securitiesTransacted
insideTradingData.loc[insideTradingData.acquistionOrDisposition == "D", 'securityTransactedTrue'] = insideTradingData.securitiesTransacted * -1



app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = "Cashew ™  ", style = {'textAlign':'center',
                                            'marginTop':40,'marginBottom':40}),
    
    dcc.Tabs([
        dcc.Tab(label='TABLES', children=[ 
            dcc.Dropdown( list(symbol_metadata_df.sector.unique()), list(symbol_metadata_df.sector.unique()),
                multi=True, id = 'sectorSelect'
                ),
             html.Div([
                 html.Div([dash_table1], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40}),
                 html.Div([dash_table2], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40}),
             ]),
             html.Div([
                 html.Div([dash_table3], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40}),
                 html.Div([dash_table4], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40}),
             ]),
             html.Div([dcc.Graph(id="scatterPlot")], style={'display': 'inline-block'}),

        ]),
        dcc.Tab(label='ANALYSIS', children=[
            html.Div([ 
                dcc.Input(id="stockSymbol", type="text", placeholder="symbol",value="NVDA", debounce=True),
                html.Div([html.H4('CANDLESTICK'),dcc.Graph(id="candleStick")], style={'display': 'inline-block'}),
                html.Div([html.H4('Health Comparison'),dcc.Graph(id="radarChart")], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40}),
                
                dcc.Tabs([
                    dcc.Tab(label='ANNUAL', children=[ html.Div([dcc.Graph(id="earningsBar")],  style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40})]),
                    dcc.Tab(label='QUARTER',children=[ html.Div([dcc.Graph(id="earningsLine")], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40})])
                    ],  style=tabs_styles),
            ]),
            html.Div([ 
                html.Div([dcc.Slider(0, 20, 5,value=10,id='transactionCount')], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40}),        
                html.Div([html.H4('InsideTrading'),dcc.Graph(id="insideTradingBar")], style={'display': 'inline-block'}),
            ])
        ]),
        dcc.Tab(label='CALENDAR', children=[]),
    ])
   
])        
# @app.callback(
#     Output("scatterPlot", "figure"),
#     Input("sectorSelect", "value")))
# def update_DT_health():
    
    
@app.callback(
    Output("scatterPlot", "figure"),
    Input("sectorSelect", "value"))
def scatter_plot(sectorSelect):
    healthiest_companies_metadata_df["rank_ROA"] =  healthiest_companies_metadata_df["ROA"].rank(pct=True)
    healthiest_companies_metadata_df["rank_ROE"] =  healthiest_companies_metadata_df["ROE"].rank(pct=True)
    healthiest_companies_metadata_df["rank_piotroski"] =  healthiest_companies_metadata_df["piotroskiScore"].rank(pct=True)
    healthiest_companies_metadata_df["rank_DE"] =  healthiest_companies_metadata_df["debtEquityRatio"].rank(method="max", pct=True)
    healthiest_companies_metadata_df["rank_overall_hc"] = ((0.25* healthiest_companies_metadata_df["rank_ROA"]) + (0.25* healthiest_companies_metadata_df["rank_ROE"]) 
                                                        + (0.25* healthiest_companies_metadata_df["rank_piotroski"]) + (0.25* healthiest_companies_metadata_df["rank_DE"]))

    best_value_metadata_df["DCF_Discount"] = (best_value_metadata_df["DCFminusPrice"]) / (best_value_metadata_df["Price_BV"])
    best_value_metadata_df["yearly_discount"] = (best_value_metadata_df["yearHigh"] - best_value_metadata_df["price"]) / best_value_metadata_df["price"] 
    best_value_metadata_df["percToFloor"] = (best_value_metadata_df["price"] - best_value_metadata_df["yearLow"]) / best_value_metadata_df["price"] 
    best_value_metadata_df["InsiderPurchased/TransCount"] = best_value_metadata_df["InsiderPurchased"] / best_value_metadata_df["TransactionCount"]
    best_value_metadata_df['InsiderPurchased/TransCount'] = best_value_metadata_df['InsiderPurchased/TransCount'].replace(np.nan, 0)

    best_value_metadata_df["rank_1"] =  best_value_metadata_df["DCF_Discount"].rank(pct=True)
    best_value_metadata_df["rank_2"] =  best_value_metadata_df["yearly_discount"].rank(pct=True)
    best_value_metadata_df["rank_3"] =  best_value_metadata_df["InsiderPurchased/TransCount"].rank(pct=True)
    best_value_metadata_df["rank_overall_bv"] = ((0.333* best_value_metadata_df["rank_1"]) + (0.333* best_value_metadata_df["rank_2"]) 
                                                        + (0.333* best_value_metadata_df["rank_3"]) )
    
    return scatter_wrapper(healthiest_companies_metadata_df,best_value_metadata_df)


@app.callback(
    Output("candleStick", "figure"), 
    Input("stockSymbol", "value"))
def display_candlestick(stockSymbol):
    return candlestick_wrapper(stockSymbol)
    
@app.callback(
    Output("radarChart", "figure"), 
   Input("stockSymbol", "value"))
def display_radar(stockSymbol):
    return radar_wrapper(stockSymbol)


@app.callback(
    Output("earningsLine", "figure"), 
    Input("stockSymbol", "value"))
def earnings_quarter(stockSymbol):
    return quarter_earnings_wrapper(stockSymbol)


@app.callback(
    Output("earningsBar", "figure"), 
    Input("stockSymbol", "value"))
def earnings_bar(stockSymbol):
    return annual_earnings_wrapper(stockSymbol)



@app.callback(
    Output("insideTradingBar", "figure"), 
    Input("stockSymbol", "value"),
    Input("transactionCount", "value"),
    # Input("timeFrame", "value"),
    )
def insider_trading(stockSymbol, transactionCount):
    return insider_trade_wrapper(stockSymbol)
    
    
app.run_server(debug=True)