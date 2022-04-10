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
from bokeh.models import ColumnDataSource, LabelSet, Div, TextInput, CustomJS, Button, FactorRange, DataTable, TableColumn, Column
#from bokeh.transform import factor_cmap, factor_mark
from bokeh.models.widgets import Tabs, Panel, MultiSelect, Paragraph, Select

import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text


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

# DataTable Sources
analystRatingDTsource = ColumnDataSource(analyst_rating_df)
biggestGrowersDTsource = ColumnDataSource(biggest_growers_df)
bestValueDTsource = ColumnDataSource(best_value_df)
healthiestCompsDTsource = ColumnDataSource(healthiest_companies_df)


def column_formatter(df):
    columns=[]
    for i in df.columns:
        columns.append(TableColumn(field=i, title=i))
    return columns

analystRatingColumns=column_formatter(analyst_rating_df)
analystRatingDT = DataTable(source=analystRatingDTsource, columns=analystRatingColumns, autosize_mode="force_fit", background="#4e85b1", width=600, height=600)

biggestGrowersColumns=column_formatter(biggest_growers_df)
biggestGrowersDT = DataTable(source=biggestGrowersDTsource, columns=biggestGrowersColumns, autosize_mode="fit_viewport", background="blue", width=600, height=600)

bestValueColumns=column_formatter(best_value_df)
bestValueDT = DataTable(source=bestValueDTsource, columns=bestValueColumns, autosize_mode="force_fit", background="green", width=600, height=600)

# output_file("healthiestCompsDT")
healthiestCompColumns=column_formatter(healthiest_companies_df)
healthiestCompsDT = DataTable(source=healthiestCompsDTsource, columns=healthiestCompColumns, autosize_mode="fit_viewport",  width=600, height=600)
show(healthiestCompsDT)




# ___________________________________________________________________________________________________________________________________
#                                   LAYOUT

# analystRatingColumn = column(analystRatingDT)
# bestValueColumn = column(bestValueDT)
# biggestGrowersColumn = column(biggestGrowersDT)
# healthiestCompColumn = column(healthiestCompsDT)

grid = gridplot([ [analystRatingDT,bestValueDT ],
                  [biggestGrowersDT,healthiestCompsDT ]  ])
# inputRow1=column(analystRatingDT, bestValueDT )
# inputRow2=column(biggestGrowersDT, healthiestCompsDT)

# combinedRow = row(inputRow1, inputRow2)
l1 = layout([[grid]], sizing_mode='fixed')
l2 = layout([[]],sizing_mode='fixed')
l3 = layout([[]], sizing_mode='fixed')
tab1 = Panel(child=l1,title="Tablez")
tab2 = Panel(child=l2,title="BarChart")
tab3 = Panel(child=l3,title="Download")


tabs = Tabs(tabs=[ tab1, tab2, tab3 ])

curdoc().theme = 'light_minimal'  #caliber, dark_minimal, light_minimal, night_sky, and contrast.
template = """
{% block postamble %}
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



