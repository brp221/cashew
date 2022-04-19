#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 21:44:08 2022

@author: bratislavpetkovic
"""

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


dt_style={
    'whiteSpace': 'normal',
    'height': 'auto',
    'width' : '500',
    'lineHeight': '15px'
}

style_data_conditional=[
        {
            'if': {
                'column_id': 'Symbol'
            },
            'color': '#18ACF0',
            'backgroundColor': '#F0880C',
            'fontWeight': 'bold'
        },
        {
            'if': {
                'filter_query': '{AnalystRating} > 4.10',
                'column_id': 'AnalystRating'
            },
            'textDecoration': 'underline'
        }
    ]

# style_data_conditional=[
#         {
#             'if': {
#                 'column_id': 'Region',
#             },
#             'backgroundColor': 'dodgerblue',
#             'color': 'white'
#         },
#         {
#             'if': {
#                 'filter_query': '{Humidity} > 19 && {Humidity} < 41',
#                 'column_id': 'Humidity'
#             },
#             'backgroundColor': 'tomato',
#             'color': 'white'
#         },

#         {
#             'if': {
#                 'column_id': 'Pressure',

#                 # since using .format, escape { with {{
#                 'filter_query': '{{Pressure}} = {}'.format(df['Pressure'].max())
#             },
#             'backgroundColor': '#85144b',
#             'color': 'white'
#         },

#         {
#             'if': {
#                 'row_index': 5,  # number | 'odd' | 'even'
#                 'column_id': 'Region'
#             },
#             'backgroundColor': 'hotpink',
#             'color': 'white'
#         },

#         {
#             'if': {
#                 'filter_query': '{id} = 4',  # matching rows of a hidden column with the id, `id`
#                 'column_id': 'Region'
#             },
#             'backgroundColor': 'RebeccaPurple'
#         },

#         {
#             'if': {
#                 'filter_query': '{Delivery} > {Date}', # comparing columns to each other
#                 'column_id': 'Delivery'
#             },
#             'backgroundColor': '#3D9970'
#         },

#         {
#             'if': {
#                 'column_editable': False  # True | False
#             },
#             'backgroundColor': 'rgb(240, 240, 240)',
#             'cursor': 'not-allowed'
#         },

#         {
#             'if': {
#                 'column_type': 'text'  # 'text' | 'any' | 'datetime' | 'numeric'
#             },
#             'textAlign': 'left'
#         },

#         {
#             'if': {
#                 'state': 'active'  # 'active' | 'selected'
#             },
#            'backgroundColor': 'rgba(0, 116, 217, 0.3)',
#            'border': '1px solid rgb(0, 116, 217)'
#         }
