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

Cl_card_style={'width':  "100%", "display": 'flex', "flexDirection":"column","background": "dark"}
Cl_card_style_horizontal={"height": 30,'width':  "100%", "display": 'inline-flex', "flexDirection":"row","background": "dark", "marginTop":10}
