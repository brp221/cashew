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

df = px.data.stocks()
fig = px.line(incomeStatDFQuart, x="date", y=['revenue','ebitda' ,'netIncome'],
              hover_data={"date": "|%B %d, %Y"},
              title='custom tick labels')
fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y")
fig.show()


#-------------------------------------------------------------------------------------------------------------------------------------------------------------




#-------------------------------------------------------------------------------------------------------------------------------------------------------------