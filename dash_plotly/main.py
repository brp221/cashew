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

from sqlalchemy import column
from sqlalchemy import create_engine
# from sqlalchemy import select
from sqlalchemy import table
# from sqlalchemy import text

import plotly.graph_objects as go
import plotly.express as px


from urllib.request import urlopen
import certifi
import json

# from library.helperFunctions import  get_jsonparsed_data

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)



app = Dash()   #initialising dash app

# CONNECT TO DB
DATABASE_URL = "postgresql://rhrqiookrgcrnz:fcd238d060c40424f6e05b4ca28b9a07126e0a29a76eb1c4f3c83530a044174b@ec2-34-194-73-236.compute-1.amazonaws.com:5432/d4nvq9ol4b3f2k"
engine = create_engine(DATABASE_URL, echo = False)
print(engine.execute("SELECT * FROM \"analyst_rating\" ").fetchone())


# METADATA
symbol_metadata = table("symbol_metadata", column("symbol"), column("companyName"), column("sector"),column("industry"), column("country"), 
                       column("exchangeShortName"), column("price"), column("marketCap"), column("isEtf"))
symbol_metadata_stmt = symbol_metadata.select() #.where(analyst_rating.c.name == 'Bob')
symbol_metadata_df = pd.read_sql_query(symbol_metadata_stmt, engine)
symbol_metadata_df["Symbol"] = symbol_metadata_df["symbol"]
del symbol_metadata_df["symbol"]

# ANALYST RATING
analyst_rating = table("analyst_rating", column("Symbol"), column("AnalystRating"), column("AnalystResponses"),
                       column("RatingRank"), column("ResponsesRank"), column("AverageRank"))
analyst_stmt = analyst_rating.select() #.where(analyst_rating.c.name == 'Bob')
analyst_rating_df = pd.read_sql_query(analyst_stmt, engine)     
analyst_rating_metadata_df =  analyst_rating_df.merge(symbol_metadata_df)

# BIGGEST GROWERS
biggest_growers = table("biggest_growers", column("Symbol"), column("freeCashFlowGrowth"), column("revGrowth1Yr"),
                        column("revGrowth1Yr"), column("netIncomeGrowth1Yr"), column("netIncomeGrowth2Yr"), column("debt_repayment"))
biggest_growers_stmt = biggest_growers.select() #.where(analyst_rating.c.name == 'Bob')
biggest_growers_df = pd.read_sql_query(biggest_growers_stmt, engine) 
biggest_growers_metadata_df =  biggest_growers_df.merge(symbol_metadata_df)


# BEST VALUE
best_value = table("best_value", column("Symbol"), column("price"), column("DCF"), column("DCFminusPrice"),column("grahamMinusPrice"), column("grahamNumber"), 
                       column("yearHigh"), column("yearLow"), column("InsiderPurchased"), column("TransactionCount"), )
best_value_stmt = best_value.select() #.where(analyst_rating.c.name == 'Bob')
best_value_df = pd.read_sql_query(best_value_stmt, engine)
best_value_df["Price_BV"] = best_value_df["price"]
del best_value_df["price"]
best_value_metadata_df =  best_value_df.merge(symbol_metadata_df)


# HEALTHIEST COMPANIES
healthiest_companies = table("healthiest_companies", column("Symbol"), column("ROA"), column("ROE"),column("currentRatio"), column("debtEquityRatio"), 
                       column("ebitda"), column("piotroskiScore"), column("netProfitMargin"), column("priceToOperatingCashFlowsRatio"))
healthiest_companies_stmt = healthiest_companies.select() #.where(analyst_rating.c.name == 'Bob')
healthiest_companies_df = pd.read_sql_query(healthiest_companies_stmt, engine)
healthiest_companies_metadata_df =  healthiest_companies_df.merge(symbol_metadata_df)



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


stockSymbol= "NVDA"
url = ("https://financialmodelingprep.com/api/v4/insider-trading?symbol="+stockSymbol+"&page=0&apikey=ce687b3fe0554890e65d6a5e48f601f9")
insideTradingData = pd.DataFrame.from_dict(get_jsonparsed_data(url))
insideTradingData['securityTransactedTrue'] = insideTradingData.securitiesTransacted
insideTradingData.loc[insideTradingData.acquistionOrDisposition == "D", 'securityTransactedTrue'] = insideTradingData.securitiesTransacted * -1

tabs_styles = {'zIndex': 99, 'display': 'inlineBlock', 'height': '4vh', 'width': '12vw',
               'position': 'fixed', "background": "#323130", 'top': '12.5vh', 'left': '7.5vw',
               'border': 'grey', 'border-radius': '4px'}
tab_selected_style = {
    "background": "blue",
    'text-transform': 'uppercase',
    'color': 'red',
    'font-size': '11px',
    'font-weight': 600,
    'align-items': 'center',
    'justify-content': 'center',
    'width': 450

}

main_tabs_style = {
    "background": "grey",
    'text-transform': 'uppercase',
    'color': 'white',
    'font-size': '11px',
    'font-weight': 600,
    'align-items': 'center',
    'justify-content': 'center',
    'border-radius': '4px',
    'padding':'6px'
}

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
    merged_df = healthiest_companies_metadata_df.merge(best_value_metadata_df)

    # df = px.data.gapminder()

    fig = px.scatter(merged_df, x="rank_overall_bv", y="rank_overall_hc",
    	         size="marketCap", color="sector",
                     hover_name="Symbol", log_x=True, size_max=60)
    
    fig.update_layout(
        width=700, height = 700
    )
    fig.show()
    return fig


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
        width=800, height = 600
    )

    return fig
    
@app.callback(
    Output("radarChart", "figure"), 
   Input("stockSymbol", "value"))
def display_radar(stockSymbol):
    print(format(stockSymbol))
    print(stockSymbol)
    outlookURL = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol="+stockSymbol+"&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    companyOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL)["rating"])

    # outlookURL2 = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol=MSFT&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    # peerOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL2)["rating"])
    # outlookURL3 = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol=GOOGL&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    # peerOutlook3  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL3)["rating"])

    x =  [companyOutlook.ratingDetailsDCFScore[0], companyOutlook.ratingDetailsROEScore[0], companyOutlook.ratingDetailsROAScore[0], 
                   companyOutlook.ratingDetailsDEScore[0], companyOutlook.ratingDetailsPEScore[0], companyOutlook.ratingDetailsPBScore[0]]
    # x2 =  [peerOutlook.ratingDetailsDCFScore[0], peerOutlook.ratingDetailsROEScore[0], peerOutlook.ratingDetailsROAScore[0], 
    #                peerOutlook.ratingDetailsDEScore[0], peerOutlook.ratingDetailsPEScore[0], peerOutlook.ratingDetailsPBScore[0]]
    # x3 =  [peerOutlook3.ratingDetailsDCFScore[0], peerOutlook3.ratingDetailsROEScore[0], peerOutlook3.ratingDetailsROAScore[0], 
    #                peerOutlook3.ratingDetailsDEScore[0], peerOutlook3.ratingDetailsPEScore[0], peerOutlook3.ratingDetailsPBScore[0]]

    categories = ["DCF", "ROE", "ROA", "D/E", "P/E", "P/B"]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
          r=x,
          theta=categories,
          fill='toself',
          name='Product A'
    ))
    # fig.add_trace(go.Scatterpolar(
    #       r=x2,
    #       theta=categories,
    #       fill='toself',
    #       name='Product B'
    # ))
    # fig.add_trace(go.Scatterpolar(
    #       r=x3,
    #       theta=categories,
    #       fill='toself',
    #       name='Product C'
    # ))

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
    Output("earningsLine", "figure"), 
    Input("stockSymbol", "value"))
def earnings_quarter(stockSymbol):
    # TIME SERIES
    incomeStatURLquarter = ("https://financialmodelingprep.com/api/v3/income-statement/"+stockSymbol+"?period=quarter&limit=16&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    incomeStatDFQuart = pd.DataFrame.from_dict(get_jsonparsed_data(incomeStatURLquarter))

    incomeStatDFQuart.index = pd.to_datetime(incomeStatDFQuart.date)

    # df = px.data.stocks()
    fig = px.line(incomeStatDFQuart, x="date", y=['revenue','ebitda' ,'netIncome'],
                  hover_data={"date": "|%B %d, %Y"},
                  title='custom tick labels')
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")
    fig.show()
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



@app.callback(
    Output("insideTradingBar", "figure"), 
    Input("stockSymbol", "value"),
    Input("transactionCount", "value"),
    # Input("timeFrame", "value"),
    )
def insider_trading(stockSymbol, transactionCount):
    # free acquisitions to be colored. Also outline importance of the seller/buyer in scope of company
    # maybe trim into a couple of diffferent types of people 
    url = ("https://financialmodelingprep.com/api/v4/insider-trading?symbol="+stockSymbol+"&page=0&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    insideTradingData = pd.DataFrame.from_dict(get_jsonparsed_data(url))
    insideTradingData['securityTransactedTrue'] = insideTradingData.securitiesTransacted
    insideTradingData.loc[insideTradingData.acquistionOrDisposition == "D", 'securityTransactedTrue'] = insideTradingData.securitiesTransacted * -1 
    fig = go.Figure(go.Bar(
                x=list(insideTradingData.securityTransactedTrue),
                y=list(insideTradingData.typeOfOwner),
                orientation='h'))
    fig.update_layout( width=600,height=400)
    return fig
app.run_server(debug=True)