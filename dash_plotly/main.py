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

from helper_functions import  get_jsonparsed_data, health_preparer, discount_preparer, growers_preparer, analyst_rating_preparer
from db_helpers import fetch_symbol_metadata, fetch_analyst_rating, fetch_biggest_growers, fetch_best_value, fetch_healthiest_companies
from ui_styles import tabs_styles, dt_style
from callback_wrapper import candlestick_wrapper, scatter_wrapper, radar_wrapper, quarter_earnings_wrapper, annual_earnings_wrapper, insider_trade_wrapper


app = Dash()   #initialising dash app

# METADATA
symbol_metadata_df = fetch_symbol_metadata()

# ANALYST RATING
analyst_rating_df = fetch_analyst_rating()
analyst_rating_metadata_df =  analyst_rating_df.merge(symbol_metadata_df)
del analyst_rating_metadata_df["price"]

# BIGGEST GROWERS
biggest_growers_df = fetch_biggest_growers()
biggest_growers_metadata_df =  biggest_growers_df.merge(symbol_metadata_df)
del biggest_growers_metadata_df["price"]

# BEST VALUE
best_value_df = fetch_best_value()
best_value_metadata_df =  best_value_df.merge(symbol_metadata_df)


# HEALTHIEST COMPANIES 
healthiest_companies_df = fetch_healthiest_companies()
healthiest_companies_metadata_df =  healthiest_companies_df.merge(symbol_metadata_df)
del healthiest_companies_metadata_df["price"]

sectors = list(symbol_metadata_df.sector.unique())
sectors.remove('')

tables = ['Analyst Rating', 'Best Value', 'Biggest Growth', 'Healthiest']
all_options = {
    'Analyst Rating': [ 'Best Value', 'Biggest Growth', 'Healthiest'],
    'Best Value': ['Analyst Rating', 'Biggest Growth', 'Healthiest'],
    'Biggest Growth': ['Analyst Rating', 'Best Value',  'Healthiest'],
    'Healthiest': ['Analyst Rating', 'Best Value', 'Biggest Growth']
}
best_value_all = ['Symbol','DCF','DCFminusPrice','grahamMinusPrice','grahamNumber','yearHigh','yearLow','InsiderPurchased','TransactionCount','Price_BV']
best_value_chosen = ['Symbol','DCFminusPrice','grahamNumber','InsiderPurchased','TransactionCount','Price_BV']
biggest_growers_all = ['Symbol', 'freeCashFlowGrowth', 'revGrowth1Yr', 'revGrowth2Yr','netIncomeGrowth1Yr', 'netIncomeGrowth2Yr', 'debt_repayment','employeeGrowth']
biggest_growers_chosen = ['Symbol', 'freeCashFlowGrowth', 'revGrowth1Yr','netIncomeGrowth1Yr', 'debt_repayment',]
healthiest_all = ['Symbol', 'ROA', 'ROE', 'currentRatio', 'debtEquityRatio', 'ebitda','piotroskiScore', 'netProfitMargin', 'priceToOperatingCashFlowsRatio']
healthiest_chosen = ['Symbol', 'ROA', 'ROE', 'currentRatio', 'debtEquityRatio','piotroskiScore' ]
analyst_rating_all = ['Symbol', 'AnalystRating', 'AnalystResponses', 'RatingRank','ResponsesRank', 'AverageRank']
analyst_rating_chosen = ['Symbol', 'AnalystRating', 'AnalystResponses', 'RatingRank','ResponsesRank', 'AverageRank']

dash_table1 = dash_table.DataTable(
    analyst_rating_df.to_dict('records'),
    [{"name": i, "id": i} for i in analyst_rating_chosen],
    page_size=12, id = "DT_analysts", style_data = dt_style, fill_width=True)
dash_table2 = dash_table.DataTable(
    healthiest_companies_metadata_df.to_dict('records'),
    [{"name": i, "id": i} for i in healthiest_chosen],
    page_size=12, id = "DT_healthiest", style_data = dt_style, fill_width=True)
dash_table3 = dash_table.DataTable(
    best_value_df.to_dict('records'),
    [{"name": i, "id": i} for i in best_value_chosen],
    page_size=12, id = "DT_discount",style_data = dt_style,fill_width=True )
dash_table4 = dash_table.DataTable(
    biggest_growers_df.to_dict('records'),
    [{"name": i, "id": i} for i in biggest_growers_chosen],
    page_size=12, id = "DT_growers",style_data = dt_style, fill_width=True )

column_select1 = dcc.Dropdown( list(analyst_rating_df.columns), list(analyst_rating_df.columns),
    multi=True, id = 'AR_columns', style={'display': 'inline-block','marginRight':10,'marginBottom':110, 'width':120, 'height':300 }
    )
column_select2 = dcc.Dropdown( list(healthiest_companies_metadata_df.columns), list(healthiest_companies_metadata_df.columns),
    multi=True, id = 'HC_columns', style={'display': 'inline-block', 'marginBottom':70, 'marginTop':10,'marginRight':10, 'width':180, 'height':350 }
    )
column_select3 = dcc.Dropdown( list(best_value_df.columns), list(best_value_df.columns),
    multi=True, id = 'BV_columns', style={'display': 'inline-block', 'marginBottom':110, 'marginLeft':10, 'width':180, 'height':300 }
    )
column_select4 = dcc.Dropdown( list(biggest_growers_df.columns), list(biggest_growers_df.columns),
    multi=True, id = 'BG_columns', style={'display': 'inline-block', 'marginBottom':70, 'marginTop':10,'marginRight':10, 'width':120, 'height':350 }
    )


table_select_1 = dcc.Dropdown(tables,'Analyst Rating' , id = 'table1',style={'marginBottom':80, 'marginRight':200, 'width':200, 'height':60})
table_select_2 = dcc.Dropdown(tables,'Best Value'  , id = 'table2', style={'marginBottom':300, 'marginRight':200, 'width':200, 'height':60})


stockSymbol= "NVDA"
url = ("https://financialmodelingprep.com/api/v4/insider-trading?symbol="+stockSymbol+"&page=0&apikey=ce687b3fe0554890e65d6a5e48f601f9")
insideTradingData = pd.DataFrame.from_dict(get_jsonparsed_data(url))
insideTradingData['securityTransactedTrue'] = insideTradingData.securitiesTransacted
insideTradingData.loc[insideTradingData.acquistionOrDisposition == "D", 'securityTransactedTrue'] = insideTradingData.securitiesTransacted * -1




app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = "Cashew ™  ", style = {'textAlign':'center',
                                            'marginTop':10,'marginBottom':10}),
    
    dcc.Tabs([
        dcc.Tab(label='TABLES', children=[ 
            dcc.Dropdown( sectors, list(symbol_metadata_df.sector.unique()),
                multi=True, id = 'sectorSelect', style={'display': 'inline-block', 'marginLeft':100,'marginBottom':8, 'marginTop':8,'marginRight':100, 'width':1450, 'height':40 }
                ),
             html.Div([
                 html.Div([column_select1], style={'display': 'inline-block', 'marginLeft':2,'marginBottom':10}),
                 html.Div([dash_table1], style={'display': 'inline-block', 'marginLeft':2,'marginBottom':10}),
                 html.Div([dash_table3], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':10}),
                 html.Div([column_select3], style={'display': 'inline-block', 'marginLeft':2,'marginBottom':10}),
             ]),
             html.Div([
                 html.Div([column_select4], style={'display': 'inline-block', 'marginLeft':2,'marginBottom':10}),
                 html.Div([dash_table4], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':10}),
                 html.Div([dash_table2], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':10}),
                 html.Div([column_select2], style={'display': 'inline-block', 'marginLeft':2,'marginBottom':10}),
             ])
        ]),
        dcc.Tab(label='RESEARCH', children=[
                html.Div([
                    html.Div([dcc.Graph(id="scatterPlot")], style={'display': 'inline-block'}),
                    html.Div([
                        dcc.RadioItems(list(all_options.keys()),'Biggest Growth',id='table1',),
                        dcc.RadioItems(id='table2',value='Best Value')
                    ], style={'display': 'inline-block', 'marginLeft':60}),
                ]),
            ]),
        dcc.Tab(label='ANALYSIS', children=[
            html.Div([ 
                dcc.Input(id="stockSymbol", type="text", placeholder="symbol",value="NVDA", debounce=True),
                html.Div([html.H4('CANDLESTICK'),dcc.Graph(id="candleStick")], style={'display': 'inline-block', 'marginLeft':5,}),
                html.Div([html.H4('Health Comparison'),dcc.Graph(id="radarChart")], style={'display': 'inline-block'}),
                html.Div([html.H4('Earnings'),
                          dcc.Tabs([
                              dcc.Tab(label='ANNUAL', children=[ html.Div([dcc.Graph(id="earningsBar")],  style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40})]),
                              dcc.Tab(label='QUARTER',children=[ html.Div([dcc.Graph(id="earningsLine")], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40})])
                              ]),
                          ], style={'display': 'inline-block', 'width':300}),
                
            ]),
            html.Div([ 
                html.Div([dcc.Slider(0, 20, 5,value=10,id='transactionCount')], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40, 'width':250}),        
                html.Div([html.H4('InsideTrading'),dcc.Graph(id="insideTradingBar")], style={'display': 'inline-block','width':250}),
            ])
        ]),
        dcc.Tab(label='CALENDAR', children=[]),
    ])
   
])        

@app.callback(
    Output("table2", "options"),
    Input("table1", "value"))
def update_table2(selected_table1):
    return [{'label': i, 'value': i} for i in all_options[selected_table1]]

@app.callback(
    Output("table1", "options"),
    Input("table2", "value"))
def update_table1(selected_table2):
    return [{'label': i, 'value': i} for i in all_options[selected_table2]]

@app.callback(
    Output("scatterPlot", "figure"),
    Input("table1", "value"),
    Input("table2", "value"),
    )
def scatter_plot(table1, table2):
    print("table1:"+table1)
    print("table2:"+table2)
    df_x = pd.DataFrame()
    df_y = pd.DataFrame()

    if table1 == 'Analyst Rating' :
        df_x = analyst_rating_preparer(analyst_rating_metadata_df)
        df_x["rank_overall_x"] = df_x.rank_overall_ar
        
    elif table1 == 'Best Value' :
        df_x = discount_preparer(best_value_metadata_df)
        df_x["rank_overall_x"] = df_x.rank_overall_bv  
       
    elif table1 == 'Biggest Growth' :
        df_x = growers_preparer(biggest_growers_metadata_df)
        df_x["rank_overall_x"] = df_x.rank_overall_bg
        
    elif table1 == 'Healthiest' :
        df_x = health_preparer(healthiest_companies_metadata_df)
        df_x["rank_overall_x"] = df_x.rank_overall_hc
        
    else:
        print("error occured")
    
    if table2 == 'Analyst Rating' :
        df_y = analyst_rating_preparer(analyst_rating_metadata_df)
        df_y["rank_overall_y"] = df_y.rank_overall_ar
        
    elif table2 == 'Best Value' :
        df_y = discount_preparer(best_value_metadata_df)
        df_y["rank_overall_y"] = df_y.rank_overall_bv
        
    elif table2 == 'Biggest Growth' :
        df_y = growers_preparer(biggest_growers_metadata_df)
        df_y["rank_overall_y"] = df_y.rank_overall_bg
        
    elif table2 == 'Healthiest' :
        df_y = health_preparer(healthiest_companies_metadata_df)
        df_y["rank_overall_y"] = df_y.rank_overall_hc
        
        
    else:
        print("error occured")
        
    print("df_y : ", len(df_y))
    print("df_x : ", len(df_x))
    return scatter_wrapper(df_y,df_x)


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