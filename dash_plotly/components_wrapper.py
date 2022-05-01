#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:01:57 2022

@author: bratislavpetkovic
"""
from dash import dash_table, dcc
import dash_bootstrap_components as dbc
import sys
sys.path.append(r'/Users/bratislavpetkovic/Desktop/cashew/dash_plotly/')

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
