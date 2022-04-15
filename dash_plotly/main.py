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

from sqlalchemy import column
from sqlalchemy import create_engine
# from sqlalchemy import select
from sqlalchemy import table
# from sqlalchemy import text

import plotly.graph_objects as go


from urllib.request import urlopen
import certifi
import json


def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)



app = Dash()   #initialising dash app

# CONNECT TO DB
DATABASE_URL = "postgresql://rhrqiookrgcrnz:fcd238d060c40424f6e05b4ca28b9a07126e0a29a76eb1c4f3c83530a044174b@ec2-34-194-73-236.compute-1.amazonaws.com:5432/d4nvq9ol4b3f2k"
engine = create_engine(DATABASE_URL, echo = False)
print(engine.execute("SELECT * FROM \"analyst_rating\" ").fetchone())

# ANALYST RATING
analyst_rating = table("analyst_rating", column("Symbol"), column("AnalystRating"), column("AnalystResponses"),
                       column("RatingRank"), column("ResponsesRank"), column("AverageRank"))
analyst_stmt = analyst_rating.select() #.where(analyst_rating.c.name == 'Bob')
analyst_rating_df = pd.read_sql_query(analyst_stmt, engine)     

# BIGGEST GROWERS
biggest_growers = table("biggest_growers", column("Symbol"), column("freeCashFlowGrowth"), column("revGrowth1Yr"),
                        column("revGrowth1Yr"), column("netIncomeGrowth1Yr"), column("netIncomeGrowth2Yr"), column("debt_repayment"))
biggest_growers_stmt = biggest_growers.select() #.where(analyst_rating.c.name == 'Bob')
biggest_growers_df = pd.read_sql_query(biggest_growers_stmt, engine) 

# BEST VALUE
best_value = table("best_value", column("Symbol"), column("price"), column("DCF"), column("DCFminusPrice"),column("grahamMinusPrice"), column("grahamNumber"), 
                       column("yearHigh"), column("yearLow"), column("InsiderPurchased"), column("TransactionCount"), )
best_value_stmt = best_value.select() #.where(analyst_rating.c.name == 'Bob')
best_value_df = pd.read_sql_query(best_value_stmt, engine)

# HEALTHIEST COMPANIES
healthiest_companies = table("healthiest_companies", column("Symbol"), column("ROA"), column("ROE"),column("currentRatio"), column("debtEquityRatio"), 
                       column("ebitda"), column("piotroskiScore"), column("netProfitMargin"), column("priceToOperatingCashFlowsRatio"))
healthiest_companies_stmt = healthiest_companies.select() #.where(analyst_rating.c.name == 'Bob')
healthiest_companies_df = pd.read_sql_query(healthiest_companies_stmt, engine)


dash_table1 = dash_table.DataTable(
    analyst_rating_df.to_dict('records'),
    [{"name": i, "id": i} for i in analyst_rating_df.columns],
    page_size=15
    )
dash_table2 = dash_table.DataTable(
    healthiest_companies_df.to_dict('records'),
    [{"name": i, "id": i} for i in healthiest_companies_df.columns],
    page_size=15
    )
dash_table3 = dash_table.DataTable(
    best_value_df.to_dict('records'),
    [{"name": i, "id": i} for i in best_value_df.columns],
    page_size=15,
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
    page_size=15,
    style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        'lineHeight': '15px'
    },
    fill_width=False
    )


app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = "Cashew ™  ", style = {'textAlign':'center',
                                            'marginTop':40,'marginBottom':40}),
    
    dcc.Tabs([
        dcc.Tab(label='TABLES', children=[ 
             html.Div([
                 html.Div([dash_table1], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40}),
                 html.Div([dash_table2], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40}),
             ]),
             html.Div([
                 html.Div([dash_table3], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40}),
                 html.Div([dash_table4], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40}),
             ]),
             dcc.Dropdown( id = 'dropdown',
             options = [
                 {'label':'Google', 'value':'GOOG' },
                 {'label': 'Apple', 'value':'AAPL'},
                 {'label': 'Amazon', 'value':'AMZN'},
                 ],
             value = 'GOOGL'       
             ),
        ]),
        dcc.Tab(label='ANALYSIS', children=[
            html.Div([ 
                dcc.Checklist(
                    id='toggle-rangeslider',
                    options=[{'label': 'Include Rangeslider', 
                              'value': 'slider'}],
                    value=['slider']
                ),
                dcc.Input(id="stockSymbol", type="text", placeholder="NVDA", debounce=True),
                html.Div([html.H4('NVDA CANDLESTICK'),dcc.Graph(id="candleStick")], style={'display': 'inline-block', 'marginLeft':2}),
                html.Div([html.H4('Health Comparison'),dcc.Graph(id="radarChart")], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40}),
                html.Div([html.H4('Income Statements'),dcc.Graph(id="earningsBar")], style={'display': 'inline-block', 'marginLeft':20,'marginBottom':40})
            ])
        ]),
        dcc.Tab(label='CALENDAR', children=[]),
    ])
   
        # dcc.Graph(id = 'line_plot', figure = stock_prices())    
        
    ]
                     )



@app.callback(
    Output("candleStick", "figure"), 
    Input("stockSymbol", "value"))
def display_candlestick(stockSymbol):
    randomStock = format("NVDA")
    print(format(stockSymbol))
    url = ("https://financialmodelingprep.com/api/v3/historical-price-full/" +stockSymbol + "?apikey=ce687b3fe0554890e65d6a5e48f601f9")
    priceDF = pd.DataFrame.from_dict(get_jsonparsed_data(url)["historical"])
    priceDF["date"] = pd.to_datetime(priceDF["date"])
    fig = go.Figure(data=[go.Candlestick(x=priceDF['date'],
                    open=priceDF['open'],
                    high=priceDF['high'],
                    low=priceDF['low'],
                    close=priceDF['close'])])
    #fig.show()
    fig.update_layout(
        xaxis_rangeslider_visible='slider' in stockSymbol, width=800, height = 600
    )

    return fig
    
@app.callback(
    Output("radarChart", "figure"), 
   Input("stockSymbol", "value"))
def display_radar(stockSymbol):
    print(format(stockSymbol))
    print(stockSymbol)
    outlookURL = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol="+stockSymbol+"&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    aaplOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL)["rating"])

    outlookURL2 = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol=MSFT&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    peerOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL2)["rating"])

    outlookURL3 = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol=GOOGL&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    peerOutlook3  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL3)["rating"])

    x =  [aaplOutlook.ratingDetailsDCFScore[0], aaplOutlook.ratingDetailsROEScore[0], aaplOutlook.ratingDetailsROAScore[0], 
                   aaplOutlook.ratingDetailsDEScore[0], aaplOutlook.ratingDetailsPEScore[0], aaplOutlook.ratingDetailsPBScore[0]]
    x2 =  [peerOutlook.ratingDetailsDCFScore[0], peerOutlook.ratingDetailsROEScore[0], peerOutlook.ratingDetailsROAScore[0], 
                   peerOutlook.ratingDetailsDEScore[0], peerOutlook.ratingDetailsPEScore[0], peerOutlook.ratingDetailsPBScore[0]]
    x3 =  [peerOutlook3.ratingDetailsDCFScore[0], peerOutlook3.ratingDetailsROEScore[0], peerOutlook3.ratingDetailsROAScore[0], 
                   peerOutlook3.ratingDetailsDEScore[0], peerOutlook3.ratingDetailsPEScore[0], peerOutlook3.ratingDetailsPBScore[0]]

    categories = ["DCF", "ROE", "ROA", "D/E", "P/E", "P/B"]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
          r=x,
          theta=categories,
          fill='toself',
          name='Product A'
    ))
    fig.add_trace(go.Scatterpolar(
          r=x2,
          theta=categories,
          fill='toself',
          name='Product B'
    ))
    fig.add_trace(go.Scatterpolar(
          r=x3,
          theta=categories,
          fill='toself',
          name='Product C'
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



@app.callback(
    Output("earningsBar", "figure"), 
    Input("stockSymbol", "value"))
def earnings_bar(stockSymbol):
    print(format(stockSymbol))
    print(stockSymbol)
    url = ("https://financialmodelingprep.com/api/v3/analyst-estimates/"+stockSymbol+"?limit=4&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    estimatedEarningsDF = pd.DataFrame.from_dict(get_jsonparsed_data(url))

    # QUARTER : api/v3/income-statement/AAPL?period=quarter&limit=400&apikey=ce687b3fe0554890e65d6a5e48f601f9
    incomeStatURL = ("https://financialmodelingprep.com/api/v3/income-statement/"+stockSymbol+"?limit=4&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    incomeStatementDF  = pd.DataFrame.from_dict(get_jsonparsed_data(incomeStatURL))

    metrics = ['Revenue', 'Earnings', "EBITDA"]
    years = ['2019', '2020', '2021', '2022']
    x_metric = incomeStatementDF.date
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





app.run_server(debug=True)