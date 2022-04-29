#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:01:57 2022

@author: bratislavpetkovic
"""
from dash import dash_table, dcc
import sys
sys.path.append(r'/Users/bratislavpetkovic/Desktop/cashew/dash_plotly/')


def create_table(ID, df, columns_chosen,data_style, conditional_data_style):
    table = dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in columns_chosen],page_size=12, id = ID, 
                                 style_data = data_style, fill_width=True, editable=True, style_data_conditional=conditional_data_style)
    return table

def create_dropdown(ID, all_columns, chosen_columns, column_style):
    dropdown = dcc.Dropdown( all_columns, chosen_columns,multi=True, id = ID, style=column_style)
    return dropdown

def create_single_dropdown(ID, all_columns, chosen_columns, column_style):
    dropdown = dcc.Dropdown( all_columns, chosen_columns,multi=False, id = ID, style=column_style, optionHeight=60)
    return dropdown

def create_checklist(ID, all_choices, chosen_choices, listStyle):
    checklist = dcc.Checklist(all_choices, chosen_choices, id = ID, labelStyle=listStyle)
    return checklist
