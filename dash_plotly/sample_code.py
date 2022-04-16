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


import plotly.express as px

healthiest_companies_metadata_df["rank_ROA"] =  healthiest_companies_metadata_df["ROA"].rank()
healthiest_companies_metadata_df["rank_ROE"] =  healthiest_companies_metadata_df["ROE"].rank()
healthiest_companies_metadata_df["rank_piotroski"] =  healthiest_companies_metadata_df["piotroskiScore"].rank()
healthiest_companies_metadata_df["rank_DE"] =  healthiest_companies_metadata_df["debtEquityRatio"].rank(method="max")
healthiest_companies_metadata_df["rank_overall"] = ((0.25* healthiest_companies_metadata_df["rank_ROA"]) + (0.25* healthiest_companies_metadata_df["rank_ROE"]) 
                                                    + (0.25* healthiest_companies_metadata_df["rank_piotroski"]) + (0.25* healthiest_companies_metadata_df["rank_DE"]))

best_value_metadata_df["DCFminusPrice/Price"] = best_value_metadata_df["DCFminusPrice"] / best_value_metadata_df["price"]
best_value_metadata_df["percToCeiling"] = (best_value_metadata_df["yearHigh"] - best_value_metadata_df["price"]) / best_value_metadata_df["price"] 
best_value_metadata_df["percToFloor"] = (best_value_metadata_df["price"] - best_value_metadata_df["yearLow"]) / best_value_metadata_df["price"] 
best_value_metadata_df["InsiderPurchased/TransCount"] = best_value_metadata_df["InsiderPurchased"] / best_value_metadata_df["TransactionCount"]

best_value_metadata_df["rank_1"] =  best_value_metadata_df["DCFminusPrice/Price"].rank()
best_value_metadata_df["rank_2"] =  best_value_metadata_df["percToCeiling"].rank()
best_value_metadata_df["rank_3"] =  best_value_metadata_df["InsiderPurchased/TransCount"].rank()
best_value_metadata_df["rank_DE"] =  best_value_metadata_df["debtEquityRatio"].rank(method="max")
best_value_metadata_df["rank_overall"] = ((0.25* best_value_metadata_df["rank_ROA"]) + (0.25* best_value_metadata_df["rank_ROE"]) 
                                                    + (0.25* best_value_metadata_df["rank_piotroski"]) + (0.25* best_value_metadata_df["rank_DE"]))

best_value_metadata_df

merged_df = healthiest_companies_metadata_df.merge(best_value_metadata_df)

df = px.data.gapminder()

fig = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp",
	         size="pop", color="continent",
                 hover_name="country", log_x=True, size_max=60)
#fig.show()
fig.update_layout(
    width=700, height = 700
)