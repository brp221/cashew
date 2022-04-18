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

df = px.data.gapminder()

fig = px.scatter(merged_df, x="rank_overall_bv", y="rank_overall_hc",
	         size="marketCap", color="sector",
                 hover_name="country", log_x=True, size_max=60)
#fig.show()
fig.update_layout(
    width=700, height = 700
)

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