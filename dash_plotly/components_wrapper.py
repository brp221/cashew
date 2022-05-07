#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:01:57 2022

@author: bratislavpetkovic
"""
from dash import dash_table, dcc, html
import dash_bootstrap_components as dbc

import fmpsdk
import sys
import pandas as pd

sys.path.append(r'/Users/bratislavpetkovic/Desktop/cashew/dash_plotly/')
from helper_functions import *

LOGO_1 = "https://img.freepik.com/free-vector/cashew-nut-vector-illustration-concept-design-templatecashew_598213-23.jpg?w=1380"
LOGO_2 = "https://img.freepik.com/free-vector/cashew-nut-vector-illustration-concept-design-templatecashew_598213-70.jpg?w=2000"
CASHEW_JAR="https://lh3.googleusercontent.com/TpFFMagmFkjddl13xGU38ZXH8SQ__g8c1Z2AJwfEvjgLSuTb6H-DVYzasLNeBuQzQZrEikRHMJ_OI5IQYjSQITP7gKtKt5pKFWqjgpgd11kr41Pxy66oV3qoPLAnhGpKJlOGGdGNZLo=w2400"
CASHEW_JAR_CIRCLE="https://lh3.googleusercontent.com/_1qfDVO4jBGVyHLpyvGw_GyVTIziSPVmytFj0YB0Z1Mjct1DOL-XPa09G1_3TOFvfH_vNHn_vFvbqJUZxkQ4kOkzJFUP579GUKNR6yZYdka6qZgIhcwhB6WB8gchPGpsxiXSoNJiFeI=s263-p-k"

navbar = dbc.Navbar(
    [dbc.Col(html.Plaintext("     ")),
     html.Img(src=CASHEW_JAR_CIRCLE, height="100px", width = "100px"),
    dbc.Container(
        [  html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [   dbc.Col(html.Plaintext("     ")),
                        # dbc.Col(html.Img(src=CASHEW_JAR_CIRCLE, height="90px", width = "90px")),
                        dbc.Col(html.Plaintext("    ")),
                        dbc.Col(dbc.NavbarBrand("            CASHEW ™", class_name="ls-2")),
                    ],
                    align="center",
                    class_name="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
            # dbc.Collapse(
            #     dbc.Nav(
            #         [nav_item, dropdown],
            #         class_name="ms-auto",
            #         navbar=True,
            #     ),
            #     id="navbar-collapse2",
            #     navbar=True,
            # ),
        ],
    )],
    color="primary",
    dark=True,
    className="mb-5",
)


def create_table(ID, df, columns_chosen,data_style, conditional_data_style):
    table = dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in columns_chosen],page_size=12, id = ID, 
                                 style_data = data_style, fill_width=True, editable=True, sort_action='native', style_data_conditional=conditional_data_style)
    return table

def create_dropdown(ID, all_columns, chosen_columns, column_style):
    dropdown = dcc.Dropdown( all_columns, chosen_columns,multi=True, id = ID, style=column_style)
    return dropdown

def create_single_dropdown(ID, all_columns, chosen_columns, column_style):
    dropdown = dcc.Dropdown( all_columns, chosen_columns,multi=False, id = ID, style=column_style)#, optionHeight=60)
    return dropdown

def create_checklist(ID, all_choices, chosen_choices, listStyle):
    checklist = dcc.Checklist(all_choices, chosen_choices, id = ID, labelStyle=listStyle)    
    return checklist

def create_dbc_checklist(ID, all_choices, chosen_choices, listStyle):
    checklist = dbc.Checklist(id=ID,options=all_choices,label_checked_style={"color": "red"},
                              input_checked_style=listStyle,),
    return checklist

def CL_in_card(checklist, providedStyle, text):
    card = dbc.Card([dbc.CardHeader([html.Div(text)]),
                                dbc.CardBody(dbc.Row([dbc.Col([checklist])]))],
                                style=providedStyle)
    return card

def create_card(symbol, card_style):
    #https://financialmodelingprep.com/api/v3/profile/AAPL?apikey=YOUR_API_KEY
    url = ("https://financialmodelingprep.com/api/v3/profile/"+symbol+"?apikey=ce687b3fe0554890e65d6a5e48f601f9")
    profileDF = pd.DataFrame.from_dict(get_jsonparsed_data(url))
    print("website: ",profileDF["website"][0])
    print("image: ",profileDF["image"][0])
    print("price: ",profileDF["price"][0])
    card = dbc.Card(
        [
            dbc.CardImg(src=profileDF["image"][0], class_name="mx-auto", top=True, style={"display":"block","width":45, "height":45}),
            dbc.CardBody(
                [
                    html.H4(symbol, className="card-title"),  html.P(print("price: ",profileDF["price"][0]),className="card-text"),
                    dbc.CardLink("External link", href=profileDF["website"][0]),dbc.Button("Go somewhere", color="info", size="sm"),
                ]),
        ],style=card_style)
    return card



mockCard = dbc.Card(
    [
        dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
        dbc.CardBody(
            [
                html.H4("Card title", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dbc.CardLink("External link", href="https://google.com"),
                dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ],
    style={"width": 200, "height": 200, "marginLeft":12, "marginTop":12},
)