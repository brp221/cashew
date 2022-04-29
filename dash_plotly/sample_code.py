# -*- coding: utf-8 -*-
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

from helperFunctions import get_jsonparsed_data

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.I("Try typing in input 1 & 2, and observe how debounce is impacting the callbacks. Press Enter and/or Tab key in Input 2 to cancel the delay"),
        html.Br(),
        dcc.Input(id="input1", type="text", placeholder="yo", style={'marginRight':'10px'}),
        dcc.Input(id="input2", type="text", placeholder="", debounce=True),
        html.Div(id="output"),
    ]
)


@app.callback(
    Output("output", "children"),
    Input("input1", "value"),
    Input("input2", "value"),
)
def update_output(input1, input2):
    return u'Input 1 {} and Input 2 {}'.format(input1, input2)


# free acquisitions to be colored. Also outline importance of the seller/buyer in scope of company
stockSymbol= "NVDA"
url = ("https://financialmodelingprep.com/api/v4/insider-trading?symbol="+stockSymbol+"&page=0&apikey=ce687b3fe0554890e65d6a5e48f601f9")
insideTradingData = pd.DataFrame.from_dict(get_jsonparsed_data(url))
insideTradingData['securityTransactedTrue'] = insideTradingData.securitiesTransacted
insideTradingData.loc[insideTradingData.acquistionOrDisposition == "D", 'securityTransactedTrue'] = insideTradingData.securitiesTransacted * -1


fig = go.Figure(go.Bar(
            x=list(insideTradingData.securityTransactedTrue),
            y=list(insideTradingData.typeOfOwner),
            orientation='h'))
fig.show()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
import plotly.express as px


analyst_rating_metadata_df.rank_overall_x = analyst_rating_metadata_df.AnalystRating

biggest_growers_metadata_df.rank_1 = biggest_growers_metadata_df.netIncomeGrowth2Yr.rank(pct=True)
biggest_growers_metadata_df.rank_2 = biggest_growers_metadata_df.revGrowth1Yr.rank(pct=True)
biggest_growers_metadata_df.rank_3 = biggest_growers_metadata_df.freeCashFlowGrowth.rank(pct=True)
biggest_growers_metadata_df.rank_4 = biggest_growers_metadata_df.debt_repayment.rank(pct=True, ascending=False)
biggest_growers_metadata_df.rank_overall_y = ((0.25*biggest_growers_metadata_df.rank_1) + (0.25*biggest_growers_metadata_df.rank_2) + 
                                            (0.25*biggest_growers_metadata_df.rank_3) + (0.25*biggest_growers_metadata_df.rank_4))

merged_df = analyst_rating_metadata_df.merge(biggest_growers_metadata_df)

fig = px.scatter(merged_df, x="rank_overall_x", y="rank_overall_y",
	         size="marketCap", color="sector",
                 hover_name="country", log_x=True, size_max=60)
fig.update_layout(
    width=700, height = 700
)
#fig.show()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# TIME SERIES
incomeStatURLquarter = ("https://financialmodelingprep.com/api/v3/income-statement/NVDA?period=quarter&limit=16&apikey=ce687b3fe0554890e65d6a5e48f601f9")
incomeStatDFQuart = pd.DataFrame.from_dict(get_jsonparsed_data(incomeStatURLquarter))
incomeStatDFQuart.index = pd.to_datetime(incomeStatDFQuart.date)


# https://financialmodelingprep.com/api/v3/financial-growth/NVDA?period=quarter&limit=80&apikey=ce687b3fe0554890e65d6a5e48f601f9
# https://financialmodelingprep.com/api/v3/financial-growth/NVDA?period=quarter&limit=80&apikey=ce687b3fe0554890e65d6a5e48f601f9
finGrowthQuartURL = ("https://financialmodelingprep.com/api/v3/financial-growth/NVDA?period=quarter&limit=80&apikey=ce687b3fe0554890e65d6a5e48f601f9")
finGrowthQuart = pd.DataFrame.from_dict(get_jsonparsed_data(finGrowthQuartURL))

x = finGrowthQuart.date
revGrowth = finGrowthQuart.revenueGrowth
netIncGrowth = finGrowthQuart.netIncomeGrowth

# Create traces
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=revGrowth,
                    mode='lines+markers',
                    name='lines+markers'))
fig.add_trace(go.Scatter(x=x, y=netIncGrowth,
                    mode='markers', name='markers'))

fig.show()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------

import dash_bootstrap_components as dbc
from dash import html

row = html.Div(
    [
        dbc.Row(dbc.Col(html.Div("A single, half-width column"), width=6)),
        dbc.Row(
            dbc.Col(html.Div("An automatically sized column"), width="auto")
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"), width=3),
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns"), width=3),
            ]
        ),
    ]
)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
dcc.Tabs([
    dcc.Tab(label='TABLES', children=[ 
        dcc.Dropdown( sectors, list(symbol_metadata_df.sector.unique()),
            multi=True, id = 'sectorSelect', style={'display': 'inline-block', 'marginLeft':100,'marginBottom':8, 'marginTop':8,'marginRight':100, 'width':1450, 'height':40 }),
        table_select,
         html.Div([
             html.Div([dash_table1], id='dash_table1',style={'display': 'inline-block', 'marginLeft':10,'marginRight':10, 'marginBottom':2}),
             html.Div([analyst_checklist],id='analyst_checklist' ,style={'display': 'inline-block',"height":600, "width":200, 'marginLeft':20, 'marginRight':10,'marginBottom':200}),
             
             html.Div([dash_table3],id='dash_table2',style={'display': 'hidden', 'marginLeft':20,'marginBottom':2}),
             html.Div([discount_checklist],id='discount_checklist',style={'display': 'hidden', 'marginRight':20, 'marginBottom':200}),
             
             html.Div([dash_table4], style={'display': 'hidden', 'marginLeft':45,'marginBottom':2}),
             html.Div([growers_checklist], style={'display': 'hidden', 'marginLeft':20, 'marginBottom':2}),

             html.Div([dash_table2], style={'display': 'hidden', 'marginLeft':20,'marginBottom':2}),
             html.Div([haelthiest_checklist], style={'display': 'hidden', 'marginLeft':45,'marginBottom':10}),
         ]),
    ], style = tab_style, selected_style = tab_selected_style),
    dcc.Tab(label='RESEARCH', children=[
            html.Div([
                html.Div([dcc.Graph(id="scatterPlot")], style={'display': 'inline-block'}),
                html.Div([
                    dcc.RadioItems(list(all_options.keys()),'Biggest Growth',id='table1',),
                    dcc.RadioItems(id='table2',value='Best Value')
                ], style={'display': 'inline-block', 'marginLeft':60}),
            ]),
        ], style = tab_style, selected_style = tab_selected_style),
    dcc.Tab(label='ANALYSIS', children=[
        html.Div([ 
            html.Div([   
                        # html.Div([  dcc.Input(id="stockSymbol", type="text", placeholder="symbol",value="NVDA", debounce=True   )])  , #style={'display': 'inline-block', 'marginLeft':10}),   
                        # html.Div([  dcc.Graph(id="candleStick", style={'display': 'inline-block', 'marginLeft':0, 'marginTop':0})      ]),
                        dcc.Input(id="stockSymbol", type="text", placeholder="symbol",value="NVDA", debounce=True,style={'display': 'inline-block', 'marginLeft':0, 'marginTop':0}   ),
                        dcc.Graph(id="candleStick", style={'display': 'inline-block', 'marginLeft':0, 'marginTop':0}) ,
                        dcc.Input(id="peerSymbol", type="text", placeholder="compare to", value="TSM", debounce=True,
                                  style={'display': 'inline-block', 'marginLeft':10}), 
                        dcc.Graph(id="radarChart")
                    ], style={'display': 'inline-block', 'marginLeft':1,'marginRight':1,'marginBottom':10, 'marginTop':10}),
            
            # html.Div([
            #           dcc.Input(id="peerSymbol", type="text", placeholder="compare to", value="TSM", debounce=True,
            #                     style={'display': 'inline-block', 'marginLeft':10}), 
            #           dcc.Graph(id="radarChart")], style={'display': 'inline-block', 'marginLeft':0,'marginBottom':200, 'marginTop':0}),
            html.Div([
                    dcc.Tabs([
                      dcc.Tab(label='ANNUAL', children=[ html.Div([dcc.Graph(id="earningsBar")],  style={'display': 'inline-block', 'marginLeft':10, 'marginTop':10})]),
                      dcc.Tab(label='QUARTER',children=[ html.Div([dcc.Graph(id="earningsLine")], style={'display': 'inline-block', 'marginLeft':10, 'marginTop':10})])
                      ])#, style = earnings_tabs_styles),
                ], style={'display': 'inline-block', 'marginLeft':1,'marginRight':1,'marginBottom':10, 'marginTop':10}),
            
            
                    ], style={'display': 'inline-block', 'marginLeft':1,'marginRight':1,'marginBottom':300, 'marginTop':10}),
            
        html.Div([ 
            html.Div([dcc.Slider(0, 20, 5,value=10,id='transactionCount')], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40, 'width':250}),        
            html.Div([html.H4('InsideTrading'),dcc.Graph(id="insideTradingBar")], style={'display': 'inline-block','width':250}),
            dcc.Graph(id="growthChart"),
            dcc.Graph(id="estimateGrowthChart")
        ])
    ], style = tab_style, selected_style = tab_selected_style),
    dcc.Tab(label='CALENDAR', children=[], style = tab_style, selected_style = tab_selected_style),
],style=main_tabs_styles )








