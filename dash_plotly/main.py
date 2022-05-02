#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 17:16:27 2022

@author: bratislavpetkovic
"""

from dash import Dash, dash_table, html, dcc
import dash_bootstrap_components as dbc
from random import *

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np

import sys
sys.path.append(r'/Users/bratislavpetkovic/Desktop/cashew/dash_plotly/')

from helper_functions import  get_jsonparsed_data, health_preparer, discount_preparer, growers_preparer, analyst_rating_preparer
from db_helpers import fetch_symbol_metadata, fetch_analyst_rating, fetch_biggest_growers, fetch_best_value, fetch_healthiest_companies
from ui_styles import dt_style, analyst_dt_style, tab_style, main_tabs_styles, tab_selected_style, discount_dt_style, healthiest_dt_style, growers_dt_style, earnings_tabs_styles
from callback_wrapper import *
from select_options import * 
from components_wrapper import *

symbol_metadata_df = fetch_symbol_metadata() # METADATA

analyst_rating_df = fetch_analyst_rating() # ANALYST RATING
analyst_rating_metadata_df =  analyst_rating_df.merge(symbol_metadata_df) 
del analyst_rating_metadata_df["price"]

biggest_growers_df = fetch_biggest_growers() # BIGGEST GROWERS
biggest_growers_metadata_df =  biggest_growers_df.merge(symbol_metadata_df)
del biggest_growers_metadata_df["price"]

best_value_df = fetch_best_value()          # BEST VALUE
best_value_metadata_df =  best_value_df.merge(symbol_metadata_df)

healthiest_companies_df = fetch_healthiest_companies()  # HEALTHIEST COMPANIES 
healthiest_companies_metadata_df =  healthiest_companies_df.merge(symbol_metadata_df)
del healthiest_companies_metadata_df["price"]

sectors = list(symbol_metadata_df.sector.unique())
sectors.remove('')
# tables = ['Analyst Rating', 'Best Value', 'Biggest Growth', 'Healthiest']

# TABLES
analystTable = create_table("DT_analysts", analyst_rating_metadata_df, analyst_rating_chosen, dt_style, analyst_dt_style)
healthiestTable = create_table("DT_healthiest", healthiest_companies_metadata_df, healthiest_chosen, dt_style, healthiest_dt_style)
discountTable = create_table("DT_discount", best_value_metadata_df, best_value_chosen, dt_style, discount_dt_style)
growersTable = create_table("DT_growers", biggest_growers_metadata_df, biggest_growers_chosen, dt_style, growers_dt_style)

# table_select_1 = dcc.Dropdown(tables,'Analyst Rating' , id = 'table1',style={'marginBottom':80, 'marginRight':200, 'width':200, 'height':60})
# table_select_2 = dcc.Dropdown(tables,'Best Value'  , id = 'table2', style={'marginBottom':300, 'marginRight':200, 'width':200, 'height':60})
table1Choice = dbc.RadioItems(options=tableOptions,value=tables[0],id="table1",inline=True)
table2Choice = dbc.RadioItems(options=tableOptions,value=tables[1],id="table2",inline=True)
        

#CHECKLISTS
analystChecklist = create_checklist("analystChecklist", analyst_rating_metadata_df.columns, analyst_rating_chosen, {'display': 'inline-block', 'marginLeft':-40,'width':400})
healthiestChecklist = create_checklist("healthiestChecklist", healthiest_companies_metadata_df.columns, healthiest_chosen, {'display': 'inline-block', 'marginLeft':-40,'width':400})
discountChecklist = create_checklist("discountChecklist", best_value_metadata_df.columns, best_value_chosen, {'display': 'inline-block', 'marginLeft':-40,'width':200})
growersChecklist = create_checklist("growersChecklist", biggest_growers_metadata_df.columns, biggest_growers_chosen, {'display': 'inline-block', 'marginLeft':-40,'width':200})
indicatorChecklist = create_checklist("indicatorChecklist", indicators_all, indicators_chosen, {'display': 'inline-block', 'marginLeft':-40,'width':400})
# timeframeChecklist = create_radio("timeframeChecklist", indicators_all, indicators_chosen, {'display': 'inline-block','fontSize':10})

#DROPDOWN
sectorSelect = create_dropdown("sectorSelect", sectors, sectors,{'display': 'inline-block', 'marginLeft':-20, 'marginTop':8,'marginRight':100, 'height':80  })
tableSelect =  create_single_dropdown("tableSelect", tables, 'Healthiest',{'display': 'inline-block', 'marginLeft':-20, 'marginTop':8,'height':40, 'width':200 })

#SEARCH
randSymbol = symbol_metadata_df.Symbol[randint(1,100)]
symbolSector = symbol_metadata_df[symbol_metadata_df["Symbol"]==randSymbol]["sector"].values[0]
peerSymbolChosen = symbol_metadata_df[symbol_metadata_df["sector"]==symbolSector]["Symbol"].values[0]
searchSymbol = dbc.Input(id="stockSymbol", placeholder="symbol", type="text", value=randSymbol,size="sm", style={"width": 100, "height": 30})
peerSymbol = dbc.Input(id="peerSymbol", placeholder="symbol", type="text", value=peerSymbolChosen, size="sm", style={"width": 100, "height": 30})

#LAYOUT SHORTCUTS 
table_filters=dbc.Row([dbc.Col(tableSelect, width=2),dbc.Col(sectorSelect, width=10)])
healthiest_content=dbc.Row([dbc.Col(healthiestChecklist, width=2),dbc.Col(healthiestTable, width=10)])
analyst_content=dbc.Row([dbc.Col(analystChecklist, width=3),dbc.Col(analystTable, width=9)])
discount_content=dbc.Row([dbc.Col(discountChecklist, width=3),dbc.Col(discountTable, width=9)])
growers_content=dbc.Row([dbc.Col(growersChecklist, width=2),dbc.Col(growersTable, width=10)])

#PAGE CONTENT SHORTCUTS
tablesPage = [table_filters,healthiest_content]
researchPage = [
    dbc.Row([
        dbc.Col(dbc.Label("Choose X-axis"),width=3),
        dbc.Col(table1Choice, width=6),
        ]),
    dbc.Row([
        dbc.Col(dbc.Label("Choose Y-axis"),width=3),
        dbc.Col(table2Choice, width=6),
        ]),
    dbc.Row([
            dbc.Col(dcc.Graph(id="scatterPlot",config={'displayModeBar': False}), width=12),            
        ])
    ]
analysisPage = [
    # dbc.Row([dbc.Col(searchSymbol, width=4)]),
    dbc.Row([
        dbc.Col([searchSymbol,dcc.Graph(id="estimateGrowthChart")], width=5),
        #dbc.Col(dcc.Graph(id="growthChart"), width=4),
        dbc.Col(dcc.Graph(id="insideTradingBar"), width=5),
        ]),
    dbc.Row([
        # dbc.Col(peerSymbol, width=1),
        dbc.Col([peerSymbol,dcc.Graph(id="radarChart")], width=6),
        #dbc.Col(dcc.Graph(id="candleStick"), width=4),
        dbc.Col(dcc.Graph(id="earningsLine"), width=6),
        ])
    ]
candlestickPage = [
    dbc.Row([
        dbc.Col(dcc.Graph(id="candleStick"), width=10),
        dbc.Col(indicatorChecklist, width=2),
        ]),
    # dbc.Row([
    #     dbc.Col(dcc.Graph(id="test"), width=10)
    #     ])
    ]

#APP 
app = Dash(
    external_stylesheets = [dbc.themes.VAPOR], #LUX, #MORPH, #PULSE, #VAPOR, # ZEPHYR, #SLATE, #Spacelab, #Yeti
    suppress_callback_exceptions=True) 
app.layout = dbc.Container(
[   
    navbar,
    dbc.Tabs(
        [
            dbc.Tab(tablesPage,label="DATA", tab_id="Tables"),
            dbc.Tab(researchPage,label="RESEARCH", tab_id="Research"),
            dbc.Tab(analysisPage,label="PROFILE", tab_id="Analysis"),
            dbc.Tab(candlestickPage,label="PRICE", tab_id="Candlestick"),
        ],id="tabs", active_tab="Tables",
    ),
    # html.Div(id="tab-content", className="p-4", children=tablesPage),
])

@app.callback(
    Output("tabs", "children"),
    Output("tableSelect", "value"),
    Input("tableSelect", "value"))
def update_tables_page(value):
    print("selectedTable:", value)
    tablesPageSelected = [table_filters]
    if(value=='Analyst Rating'):
        tablesPageSelected.append(analyst_content)
    elif(value=='Healthiest'):
        tablesPageSelected.append(healthiest_content)
    elif(value=='Best Value'):
        tablesPageSelected.append(discount_content)
    elif(value=='Biggest Growth'):
        tablesPageSelected.append(growers_content)
    allTabsChildren = [
        dbc.Tab(tablesPageSelected,label="DATA", tab_id="Tables"),
        dbc.Tab(researchPage,label="RESEARCH", tab_id="Research"),
        dbc.Tab(analysisPage,label="PROFILE", tab_id="Analysis"),
        dbc.Tab(candlestickPage,label="PRICE", tab_id="Candlestick"),
    ]
    return allTabsChildren, value

#     tableContent=[]
#     if(tableSelected=='Analyst Rating'):
#         tableContent=dbc.Row([dbc.Col(analystChecklist, width=2),dbc.Col(analystTable, width=10)])
#     elif(tableSelected=="Best Value"):
#         tableContent=dbc.Row([dbc.Col(discountChecklist, width=2),dbc.Col(discountTable, width=10)])
#     elif(tableSelected=="Biggest Growth"):
#         tableContent=dbc.Row([dbc.Col(growersChecklist, width=2),dbc.Col(growersTable, width=10)])
#     elif(tableSelected=="Healthiest"):
#         tableContent=dbc.Row([dbc.Col(healthiestChecklist, width=2),dbc.Col(healthiestTable, width=10)])
#     tablesPage = [dbc.Row([dbc.Col(tableSelect, width=2),dbc.Col(sectorSelect, width=10)]),tableContent]
#     return tablesPage
@app.callback(
    Output("table1", "options"),
    Input("table2", "value"))
def scatter_table1_update(table2Choice):
    table1Options = [x for x in tableOptions if not (x['value']==table2Choice)]
    return table1Options

@app.callback(
    Output("table2", "options"),
    Input("table1", "value"))
def scatter_table2_update(table1Choice):
    table2Options = [x for x in tableOptions if not (x['value']==table1Choice)]
    return table2Options

@app.callback(
    Output("estimateGrowthChart", "figure"), 
    Input("stockSymbol", "value"))
def growth_future(stockSymbol):
    return growth_future_wrapper(stockSymbol)

@app.callback(
    Output("growthChart", "figure"), 
    Input("stockSymbol", "value"))
def growth_metric(stockSymbol):
    return growth_metric_wrapper(stockSymbol)

@app.callback(
    Output("DT_analysts", "data"), 
    Input("sectorSelect", "value"))
def DT_analysts_update(sectorSelect):
    print("updating DT_analysts")
    return analyst_rating_metadata_df[analyst_rating_metadata_df.sector.isin(sectorSelect)].to_dict('records')

@app.callback(
    Output("DT_healthiest", "data"), 
    Input("sectorSelect", "value"))
def DT_healthiest_update(sectorSelect):
    print("updating DT_healthiest")
    return healthiest_companies_metadata_df[healthiest_companies_metadata_df.sector.isin(sectorSelect)].to_dict('records')

@app.callback(
    Output("DT_discount", "data"), 
    Input("sectorSelect", "value"))
def DT_discount_update(sectorSelect):
    print("updating DT_discount")
    return best_value_metadata_df[best_value_metadata_df.sector.isin(sectorSelect)].to_dict('records')

@app.callback(
    Output("DT_growers", "data"), 
    Input("sectorSelect", "value"))
def DT_growers_update(sectorSelect):
    print("updating DT_growers")
    return biggest_growers_metadata_df[biggest_growers_metadata_df.sector.isin(sectorSelect)].to_dict('records')


@app.callback( 
    Output("DT_analysts", "columns"),
    [Input('analystChecklist', 'value')],
    [State('DT_analysts', 'columns')])
def columns_table1(value, columns):
    if value is None or columns is None:
        raise PreventUpdate      
    columns = [{"name": i, "id": i, 'hideable': False} for i in value]
    return columns

@app.callback( 
    Output("DT_healthiest", "columns"),
    [Input('healthiestChecklist', 'value')],
    [State('DT_healthiest', 'columns')])
def columns_table2(value, columns):
    if value is None or columns is None:
        raise PreventUpdate      
    columns = [{"name": i, "id": i, 'hideable': False} for i in value]
    return columns

@app.callback( 
    Output("DT_discount", "columns"),
    [Input('discountChecklist', 'value')],
    [State('DT_discount', 'columns')])
def columns_table3(value, columns):
    if value is None or columns is None:
        raise PreventUpdate      
    columns = [{"name": i, "id": i, 'hideable': False} for i in value]
    return columns

@app.callback( 
    Output("DT_growers", "columns"),
    [Input('growersChecklist', 'value')],
    [State('DT_growers', 'columns')])
def columns_table4(value, columns):
    if value is None or columns is None:
        raise PreventUpdate      
    columns = [{"name": i, "id": i, 'hideable': False} for i in value]
    return columns


@app.callback(
    Output("scatterPlot", "figure"),
    Input("table1", "value"),
    Input("table2", "value"),
    )
def scatter_plot(table1, table2):
    # print("table1:"+table1)
    # print("table2:"+table2)
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
        
    return scatter_wrapper(df_y,df_x)


@app.callback(
    Output("candleStick", "figure"), 
    [Input("stockSymbol", "value"),Input("indicatorChecklist", "value")])
def display_candlestick(stockSymbol,indicators):
    return candlestick_wrapper(stockSymbol, indicators)
    
# @app.callback(
#     Output("test", "figure"), 
#     [Input("stockSymbol", "value"),Input("indicatorChecklist", "value")])
# def test(stockSymbol,indicators):
#     return test_wrapper(stockSymbol, indicators)
    


@app.callback(
    Output("radarChart", "figure"), 
    Input("stockSymbol", "value"),
    Input("peerSymbol", "value"))
def display_radar(stockSymbol, peerSymbol):
    return radar_wrapper(stockSymbol, peerSymbol)


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
    # Input("transactionCount", "value"),
    # Input("timeFrame", "value"),
    )
def insider_trading(stockSymbol):
    return insider_trade_wrapper(stockSymbol)
    
    
app.run_server(debug=True)