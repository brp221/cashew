#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 21:44:08 2022

@author: bratislavpetkovic
"""

main_tabs_styles = {
    'height': 50,
    'width': 1400, 
    'marginLeft':200
}
earnings_tabs_styles = {
    'height': 20,
    'width': 300, 
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold', 
    'backgroundColor' : '#7851a9',#7851a9
    'color' : 'white'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#5e8078',#5e8078
    'color': 'white',
    'padding': '6px'
}

dt_style={
    'whiteSpace': 'normal',
    'height': 'auto',
    'width' : '500',
    'lineHeight': '15px',
    'marginLeft' : '410'
}

analyst_dt_style=[
        {
            'if': {
                'column_id': 'Symbol'
            },
            'fontWeight': 'bold'
        },
        {
            'if': {
                'row_index': 'even',  # number | 'odd' | 'even'
                'column_id': ['Symbol','AnalystRating','AnalystResponses', 'RatingRank', 'ResponsesRank', 'AverageRank', 'companyName', 'sector', 'industry', 'country', 'marketCap']
            },
            'backgroundColor': '#d2e5e5',
            'color': 'black'
        },
        {
            'if': {
                'filter_query': '{AnalystRating} > 4.10',
                'column_id': 'AnalystRating'
            },
            'color': 'green', 
            'fontWeight': 'bold',
        },
        {
            'if': {
                'filter_query': '{AnalystRating} < 3.5',
                'column_id': 'AnalystRating'
            },
            'fontWeight': 'bold',
            'color': 'red'
        },
        {
            'if': {
                'filter_query': '{AnalystResponses} > 25',
                'column_id': 'AnalystResponses'
            },
            'color': 'green', 
            'fontWeight': 'bold',
        },
        {
            'if': {
                'filter_query': '{AnalystResponses} < 14',
                'column_id': 'AnalystResponses'
            },
            'fontWeight': 'bold',
            'color': 'red'
        }
        
        
    ]

discount_dt_style=[
        {
            'if': {
                'column_id': 'Symbol'
            },
            'fontWeight': 'bold'
        },
        {
            'if': {
                'row_index': 'odd',  # number | 'odd' | 'even'
                'column_id': ['Symbol','DCFminusPrice','grahamNumber', 'InsiderPurchased', 'TransactionCount', 'Price_BV', 'yearHigh', 'yearLow', 'DCF', 'companyName', 'sector', 'industry', 'country', 'marketCap']
            },
            'backgroundColor': '#d2e5e5',
            'color': 'black'
        },
        {
            'if': {
                # 'filter_query': '({DCFMinusPrice}/{Price_BV}) > 0.10',
                #issue here ; is DCFMINUSPRICE A number?
                'filter_query': '{DCFMinusPrice} > 15',
                'column_id': 'Symbol'
            },
            'color': 'green', 
            'fontWeight': 'bold',
        }
        
    ]

growers_dt_style=[
        {
            'if': {
                'column_id': 'Symbol'
            },
            'fontWeight': 'bold'
        },
        {
            'if': {
                'row_index': 'even',  # number | 'odd' | 'even'
                'column_id': ['Symbol','freeCashFlowGrowth','revGrowth1Yr','revGrowth2Yr','netIncomeGrowth1Yr', 'netIncomeGrowth2Yr','debt_repayment', 'employeeGrowth' ,'companyName', 'sector', 'industry', 'country', 'marketCap']
            },
            'backgroundColor': '#d2e5e5',
            'color': 'black'
        },
        {
            'if': {
                'filter_query': '{freeCashFlowGrowth} > 0.5',
                'column_id': ['Symbol','freeCashFlowGrowth']
            },
            'color': 'green', 
            'fontWeight': 'bold',
        },
        {
            'if': {
                'filter_query': '{freeCashFlowGrowth} < -0.5',
                'column_id': ['Symbol','freeCashFlowGrowth']
            },
            'color': 'red', 
            'fontWeight': 'bold',
        },
    ]

healthiest_dt_style=[
        {
            'if': {
                'column_id': 'Symbol'
            },
            'fontWeight': 'bold'
        },
        {
            'if': {
                'row_index': 'odd',  # number | 'odd' | 'even'
                'column_id': ['Symbol','ROA','ROE','currentRatio','debtEquityRatio', 'ebitda','piotroskiScore', 'netProfitMargin', 'priceToOperatingCashFlowRatio', 'companyName', 'sector', 'industry', 'marketCap' ]
            },
            'backgroundColor': '#d2e5e5',
            'color': 'black'
        },
        {
            'if': {
                'filter_query': '{piotroskiScore} > 6',
                'column_id': ['Symbol','ROA','ROE','currentRatio','debtEquityRatio', 'ebitda','piotroskiScore', 'netProfitMargin', 'priceToOperatingCashFlowRatio', 'companyName', 'sector', 'industry', 'marketCap' ]
            },
            'color': 'green', 
            'fontWeight': 'bold',
        },
        {
            'if': {
                'filter_query': '{piotroskiScore} <= 4',
                'column_id': ['Symbol','ROA','ROE','currentRatio','debtEquityRatio', 'ebitda','piotroskiScore', 'netProfitMargin', 'priceToOperatingCashFlowRatio', 'companyName', 'sector', 'industry', 'marketCap' ]        
            },
            'color': 'red', 
            'fontWeight': 'bold',
        },
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
