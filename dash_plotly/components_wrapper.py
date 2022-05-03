#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:01:57 2022

@author: bratislavpetkovic
"""
from dash import dash_table, dcc, html
import dash_bootstrap_components as dbc
import sys
sys.path.append(r'/Users/bratislavpetkovic/Desktop/cashew/dash_plotly/')

LOGO_1 = "https://img.freepik.com/free-vector/cashew-nut-vector-illustration-concept-design-templatecashew_598213-23.jpg?w=1380"
LOGO_2 = "https://img.freepik.com/free-vector/cashew-nut-vector-illustration-concept-design-templatecashew_598213-70.jpg?w=2000"

navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("DataDiscovery", href="#"),
                dbc.DropdownMenuItem("Fishing", href="#"),
                dbc.DropdownMenuItem("Analysis", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Explore",
        ),
    ],
    brand="CASHEW - Investing & Data Dicovery Tool",
    brand_href="#",
    color="dark",
    dark=True,
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [   dbc.Col(html.Plaintext("                                                 ")),
                        dbc.Col(html.Img(src=LOGO_1, height="90px", width = "90px")),
                        dbc.Col(html.Plaintext("    ")),
                        dbc.Col(dbc.NavbarBrand("            CASHEW ™", class_name="ms-2")),
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
    ),
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
    
    # checklist = dbc.Checklist(
    #         id="checklist-selected-style",
    #         options=all_choices,
    #         label_checked_style={"color": "red"},
    #         input_checked_style={
    #             "backgroundColor": "#fa7268",
    #             "borderColor": "#ea6258",
    #         },
    #     ),
    
    return checklist
