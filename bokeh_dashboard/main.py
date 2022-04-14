#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 19:54:28 2022

@author: bratislavpetkovic
"""

# myapp.py

from os.path import dirname, join
from csv import writer
import datetime
#from random import randint
# from functools import reduce

from bokeh.layouts import column, row, widgetbox,layout
from bokeh.plotting import figure, curdoc, output_file, show
from bokeh.layouts import column, row, gridplot
from bokeh.models import ColumnDataSource, LabelSet, Div, TextInput, CustomJS,MultiChoice, RangeSlider, Button, FactorRange, DataTable, TableColumn, Column
#from bokeh.transform import factor_cmap, factor_mark
from bokeh.models.widgets import Tabs, Panel, MultiSelect, Paragraph, Select
from bokeh.transform import factor_cmap, dodge
from bokeh.palettes import Spectral6, Set3, Plasma6

import pandas as pd
from pandas.core.frame import DataFrame
from math import pi

import numpy as np
from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text

# from helperLibrary.library import *

import plotly.graph_objects as go
import plotly.offline as pyo


import os
from dotenv import load_dotenv
import fmpsdk
load_dotenv()
apikey=os.environ.get("apikey")



# ___________________________________________________________________________________________________________________________________
#                                  HELPER FUNCTIONS
# For Python 3.0 and later
from urllib.request import urlopen
import certifi
import json
def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

def column_formatter(df):
    columns=[]
    for i in df.columns:
        columns.append(TableColumn(field=i, title=i))
    return columns





# ___________________________________________________________________________________________________________________________________
#                                   CHARTS + VISUALIZATIONS
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

#       <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   DATA TABLE  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
analystRatingDTsource = ColumnDataSource(analyst_rating_df)
biggestGrowersDTsource = ColumnDataSource(biggest_growers_df)
bestValueDTsource = ColumnDataSource(best_value_df)
healthiestCompsDTsource = ColumnDataSource(healthiest_companies_df)


analystRatingColumns=column_formatter(analyst_rating_df)
analystRatingDT = DataTable(source=analystRatingDTsource, columns=analystRatingColumns, autosize_mode="fit_columns", background="#4e85b1", width=770, height=400)

biggestGrowersColumns=column_formatter(biggest_growers_df)
biggestGrowersDT = DataTable(source=biggestGrowersDTsource, columns=biggestGrowersColumns, autosize_mode="force_fit", background="blue", width=770, height=400)

bestValueColumns=column_formatter(best_value_df)
bestValueDT = DataTable(source=bestValueDTsource, columns=bestValueColumns, autosize_mode="force_fit", background="green", width=770, height=400)

# output_file("healthiestCompsDT") fit_viewport
healthiestCompColumns=column_formatter(healthiest_companies_df)
healthiestCompsDT = DataTable(source=healthiestCompsDTsource, columns=healthiestCompColumns, autosize_mode="force_fit",  width=770, height=400)
show(healthiestCompsDT)

#       <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   CANDLESTICK CHART  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
randomStock = "NVDA"
url = ("https://financialmodelingprep.com/api/v3/historical-price-full/" +randomStock + "?apikey=ce687b3fe0554890e65d6a5e48f601f9")
priceDF = pd.DataFrame.from_dict(get_jsonparsed_data(url)["historical"])

priceDF["date"] = pd.to_datetime(priceDF["date"])

inc = priceDF.close > priceDF.open
dec = priceDF.open > priceDF.close
w = 12*60*60*1000 # half day in ms

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

candlestick = figure(x_axis_type="datetime", tools=TOOLS, width=750,height=400, title = randomStock + " Price")
candlestick.xaxis.major_label_orientation = pi/4
candlestick.grid.grid_line_alpha=0.3
#hovertool
candlestick.segment(priceDF.date, priceDF.high, priceDF.date, priceDF.low, color="black")
candlestick.vbar(priceDF.date[inc], w, priceDF.open[inc], priceDF.close[inc], fill_color="#3bc461", line_color="black")
candlestick.vbar(priceDF.date[dec], w, priceDF.open[dec], priceDF.close[dec], fill_color="#F2583E", line_color="black")
#show(candlestick)

#       <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   VBAR  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
url = ("https://financialmodelingprep.com/api/v3/analyst-estimates/NVDA?limit=4&apikey=ce687b3fe0554890e65d6a5e48f601f9")
estimatedEarningsDF = pd.DataFrame.from_dict(get_jsonparsed_data(url))

# QUARTER : api/v3/income-statement/AAPL?period=quarter&limit=400&apikey=ce687b3fe0554890e65d6a5e48f601f9
incomeStatURL = ("https://financialmodelingprep.com/api/v3/income-statement/NVDA?limit=4&apikey=ce687b3fe0554890e65d6a5e48f601f9")
incomeStatementDF  = pd.DataFrame.from_dict(get_jsonparsed_data(incomeStatURL))

metrics = ['Revenue', 'Earnings', "EBITDA"]
years = ['2019', '2020', '2021', '2022']

data = {'metrics' : metrics,
        '2019'   : [incomeStatementDF.revenue[3],incomeStatementDF.netIncome[3], incomeStatementDF.ebitda[3]],
        '2020'   : [incomeStatementDF.revenue[2],incomeStatementDF.netIncome[2], incomeStatementDF.ebitda[2]],
        '2021'   : [incomeStatementDF.revenue[1],incomeStatementDF.netIncome[1], incomeStatementDF.ebitda[1]],
        '2022'   : [incomeStatementDF.revenue[0],incomeStatementDF.netIncome[0], incomeStatementDF.ebitda[0]]}

x = [ (metric, year) for metric in metrics for year in years ]
counts = sum(zip(data['2019'], data['2020'], data['2021'], data['2022']), ()) # like an hstack

source = ColumnDataSource(data=dict(x=x, counts=counts))
earningsBar = figure(x_range=FactorRange(*x), height=250, title="Fruit counts by year",
           toolbar_location=None, tools="")
earningsBar.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
       fill_color=factor_cmap('x', palette=Plasma6, factors=years, start=1, end=2))
earningsBar.y_range.start = 0
earningsBar.x_range.range_padding = 0.1
earningsBar.xaxis.major_label_orientation = 1
earningsBar.xgrid.grid_line_color = None

#       <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   LINEGRAPH EARNINGS  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

url = ("https://financialmodelingprep.com/api/v3/analyst-estimates/NVDA?limit=4&apikey=ce687b3fe0554890e65d6a5e48f601f9")
estimatedEarningsDF = pd.DataFrame.from_dict(get_jsonparsed_data(url))

# QUARTER : api/v3/income-statement/AAPL?period=quarter&limit=400&apikey=ce687b3fe0554890e65d6a5e48f601f9
incomeStatURL = ("https://financialmodelingprep.com/api/v3/income-statement/NVDA?limit=4&apikey=ce687b3fe0554890e65d6a5e48f601f9")
incomeStatementDF  = pd.DataFrame.from_dict(get_jsonparsed_data(incomeStatURL))

incomeStatURLquarter = ("https://financialmodelingprep.com/api/v3/income-statement/NVDA?period=quarter&limit=16&apikey=ce687b3fe0554890e65d6a5e48f601f9")
incomeStatDFQuart = pd.DataFrame.from_dict(get_jsonparsed_data(incomeStatURLquarter))

incomeStatementDF.index = pd.to_datetime(incomeStatementDF.date)
incomeStatDFQuart.index = pd.to_datetime(incomeStatDFQuart.date)
# incomeStatementDF.year = ["2022","2021", "2020", "2019"]

TOOLS = 'save,pan,box_zoom,reset,wheel_zoom, hover'
lineGraph = figure(title="Year-wise total number of crimes",x_axis_type="datetime",  y_axis_type="linear", plot_height = 400,
           tools = TOOLS, plot_width = 800)
lineGraph.xaxis.axis_label = 'Year'
lineGraph.yaxis.axis_label = 'Metrics'
lineGraph.line(incomeStatDFQuart.index ,incomeStatDFQuart.revenue , line_color="#0C0786", line_width = 3)
lineGraph.line(incomeStatDFQuart.index ,incomeStatDFQuart.netIncome , line_color="#B02A8F", line_width = 3)
lineGraph.line(incomeStatDFQuart.index ,incomeStatDFQuart.ebitda , line_color="#FCA635", line_width = 3)

show(lineGraph)
# # p.line('date', 'netIncome', source=source)
# p.add_tools(HoverTool(('year', '@x'),
# ('revenue', '@y'),
# ('netIncome', '@y')))

# show the tooltip
# p.add_tools(HoverTool(
#     tooltips='<font face="Arial" size="3">WYear: @x{0.0}, Revenue/Income is @y{0.00}</font>',
#     mode='vline'
# ))


#       <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   INSIDER TRADING CHART  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#       <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<    COMPANY HEALTH vs (PEERS)  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
outlookURL = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol=AAPL&apikey=ce687b3fe0554890e65d6a5e48f601f9")
aaplOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL)["rating"])

outlookURL2 = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol=MSFT&apikey=ce687b3fe0554890e65d6a5e48f601f9")
peerOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL2)["rating"])

outlookURL3 = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol=GOOGL&apikey=ce687b3fe0554890e65d6a5e48f601f9")
peerOutlook3  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL3)["rating"])
categories = ["DCF", "ROE", "ROA", "D/E", "P/E", "P/B"]
categories=[*categories, categories[0]]
x =  [aaplOutlook.ratingDetailsDCFScore[0], aaplOutlook.ratingDetailsROEScore[0], aaplOutlook.ratingDetailsROAScore[0], 
               aaplOutlook.ratingDetailsDEScore[0], aaplOutlook.ratingDetailsPEScore[0], aaplOutlook.ratingDetailsPBScore[0]]
x2 =  [peerOutlook.ratingDetailsDCFScore[0], peerOutlook.ratingDetailsROEScore[0], peerOutlook.ratingDetailsROAScore[0], 
               peerOutlook.ratingDetailsDEScore[0], peerOutlook.ratingDetailsPEScore[0], peerOutlook.ratingDetailsPBScore[0]]
x3 =  [peerOutlook3.ratingDetailsDCFScore[0], peerOutlook3.ratingDetailsROEScore[0], peerOutlook3.ratingDetailsROAScore[0], 
               peerOutlook3.ratingDetailsDEScore[0], peerOutlook3.ratingDetailsPEScore[0], peerOutlook3.ratingDetailsPBScore[0]]
x=[*x, x[0]]
x2=[*x2, x2[0]]
x3=[*x3, x3[0]]

fig = go.Figure(
    data=[
        go.Scatterpolar(r=x, theta=categories, fill='toself', name='AAPL'),
        go.Scatterpolar(r=x2, theta=categories, fill='toself', name='MSFT'),
        go.Scatterpolar(r=x3, theta=categories, fill='toself', name='GOOGL')
    ],
    layout=go.Layout(
        #title=go.layout.Title(text='COMPANY HEALTH COMPARISON'),
        #polar={'radialaxis': {'visible': True}},
        showlegend=True,
        width=400,
        height=400
    )
)
output_file("radarChart.html")
fig.write_image("radarChart.jpg")
#bokeh_dashboard/static_content/
radarChartStatic = Div(text="""<img src="bokeh_dashboard/static_content/radarChart.png" alt="radarChartStatic"> """,width=200, height=100)
show(radarChartStatic)
div_image = Div(text="""<img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png" alt="div_image">""", width=150, height=150)
show(div_image)
#       <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<    COMPANY HEALTH vs (PEERS)  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


factors = ["DCF", "ROE", "ROI", "D/E", "P/E", "P/B"]
years = ['AAPL', 'PEER1', 'PEER2']

x =  [aaplOutlook.ratingDetailsDCFScore[0], aaplOutlook.ratingDetailsROEScore[0], aaplOutlook.ratingDetailsROAScore[0], 
               aaplOutlook.ratingDetailsDEScore[0], aaplOutlook.ratingDetailsPEScore[0], aaplOutlook.ratingDetailsPBScore[0]]
x2 =  [peerOutlook.ratingDetailsDCFScore[0], peerOutlook.ratingDetailsROEScore[0], peerOutlook.ratingDetailsROAScore[0], 
               peerOutlook.ratingDetailsDEScore[0], peerOutlook.ratingDetailsPEScore[0], peerOutlook.ratingDetailsPBScore[0]]
x3 =  [peerOutlook3.ratingDetailsDCFScore[0], peerOutlook3.ratingDetailsROEScore[0], peerOutlook3.ratingDetailsROAScore[0], 
               peerOutlook3.ratingDetailsDEScore[0], peerOutlook3.ratingDetailsPEScore[0], peerOutlook3.ratingDetailsPBScore[0]]

data = {'factors' : factors,
        'AAPL'    : x,
        'PEER1'   : x2,
        'PEER2'   : x3}

source = ColumnDataSource(data=data)

compHealthHBar = figure(y_range=factors, x_range=(0, 7), plot_width=400,plot_height=500, title="COMPANY HEALTH vs (PEERS)",
           toolbar_location=None, tools="")

compHealthHBar.hbar(y=dodge('factors', -0.25, range=compHealthHBar.y_range), right='AAPL', height=0.2, source=source,
       color="#c9d9d3", legend_label="AAPL")

compHealthHBar.hbar(y=dodge('factors',  0.0,  range=compHealthHBar.y_range), right='PEER1', height=0.2, source=source,
       color="#718dbf", legend_label="PEER1")

compHealthHBar.hbar(y=dodge('factors',  0.25, range=compHealthHBar.y_range), right='PEER2', height=0.2, source=source,
       color="#e84d60", legend_label="PEER2")

compHealthHBar.y_range.range_padding = 0.1
compHealthHBar.ygrid.grid_line_color = None
compHealthHBar.legend.location = "top_right"
compHealthHBar.legend.orientation = "vertical"


# ___________________________________________________________________________________________________________________________________
#                                   WIDGETS
sectorOptions = ["Technology", "Energy", "Materials", "Real Estate", "Healthcare", "Consumer Cyclical", "Industrials"]
sectorChoice = MultiChoice(value=sectorOptions, options=sectorOptions, title="sector")
sectorChoice.js_on_change("value", CustomJS(code="""
    console.log('multi_choice: value=' + this.value, this.toString())
"""))

join1Options = ["Analyst Picks", "Biggest Growers", "Best Value", "Healthiest Companies"]

join1 = MultiChoice(value=[], options=join1Options, title="joining table 1")
join1.js_on_change("value", CustomJS(code="""
    console.log('multi_choice: value=' + this.value, this.toString())
"""))

join2Options = ["Analyst Picks", "Biggest Growers", "Best Value", "Healthiest Companies"]

join2 = MultiChoice(value=[], options=join2Options, title="joining table 2")
join2.js_on_change("value", CustomJS(code="""
    console.log('multi_choice: value=' + this.value, this.toString())
"""))


marketCapSlider = RangeSlider(start=5000000000, end=3000000000000, value=(10000000000,3000000000000 ), step=1000000, title="MarketCapRange")
# marketCapSlider.on_change()
marketCapSlider.js_on_change("value", CustomJS(code="""
    console.log('slider: value=' + this.value, this.toString())
"""))

# show(marketCapSlider)


# ___________________________________________________________________________________________________________________________________
#                                   LAYOUT

annualLayout = layout([[earningsBar]], sizing_mode='fixed')
quarterLayout = layout([[lineGraph]],sizing_mode='fixed')
annualTab = Panel(child=annualLayout,title="Annual")
quartersTab = Panel(child=quarterLayout,title="Quarter")

earningsTab = Tabs(tabs=[annualTab, quartersTab])

grid = gridplot([ [analystRatingDT,bestValueDT ],
                  [biggestGrowersDT,healthiestCompsDT ]  ])


gridTab2 = gridplot([ [candlestick,earningsTab ], [compHealthHBar, radarChartStatic, div_image] ])

columnWidgets = Column(sectorChoice, join1, join2, marketCapSlider)
                       
# combinedRow = row(inputRow1, inputRow2)

l1 = layout([[grid,columnWidgets]], sizing_mode='fixed')
l2 = layout([[gridTab2]],sizing_mode='fixed')
l3 = layout([[]], sizing_mode='fixed')
tab1 = Panel(child=l1,title="Tablez")
tab2 = Panel(child=l2,title="Analysis")
tab3 = Panel(child=l3,title="Calendar")


tabs = Tabs(tabs=[ tab1, tab2, tab3 ])

curdoc().theme = 'light_minimal'  #caliber, dark_minimal, light_minimal, night_sky, and contrast.
template = """
{% block postamble %}
<a href="https://bokeh.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
<style>
.bk-root .bk-tab {
    background-color: #002C77;
    color:#00A8C7;
    font-style: normal;
    font-weight: normal;
}
.bk-root .bk-tabs-header .bk-tab.bk-active{
    background-color: #00A8C7;
    color: #002C77;
    font-style: normal;
    font-weight: bold;
}
</style>
{% endblock %}

"""

curdoc().template = template

curdoc().add_root(row(tabs, width=1000))

curdoc().title = "Cashew ™  "



