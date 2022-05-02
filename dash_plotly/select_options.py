#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 10:38:23 2022

@author: bratislavpetkovic
"""
import sys
sys.path.append(r'/Users/bratislavpetkovic/Desktop/cashew/dash_plotly/')

tables = ['Analyst Rating', 'Best Value', 'Biggest Growth', 'Healthiest']
tableOptions = [{"label": tables[0], "value": tables[0]},{"label": tables[1], "value": tables[1]},
           {"label": tables[2], "value": tables[2]},{"label": tables[3], "value": tables[3]}]
all_options = {
    'Analyst Rating': [ 'Best Value', 'Biggest Growth', 'Healthiest'],
    'Best Value': ['Analyst Rating', 'Biggest Growth', 'Healthiest'],
    'Biggest Growth': ['Analyst Rating', 'Best Value',  'Healthiest'],
    'Healthiest': ['Analyst Rating', 'Best Value', 'Biggest Growth']
}
best_value_all = ['Symbol','DCF','DCFminusPrice','grahamMinusPrice','grahamNumber','yearHigh','yearLow','InsiderPurchased','TransactionCount','Price_BV']
best_value_chosen = ['Symbol','DCFminusPrice','grahamNumber','InsiderPurchased','TransactionCount','Price_BV']

biggest_growers_all = ['Symbol', 'freeCashFlowGrowth', 'revGrowth1Yr', 'revGrowth2Yr','netIncomeGrowth1Yr', 'netIncomeGrowth2Yr', 'debt_repayment','employeeGrowth']
biggest_growers_chosen = ['Symbol', 'freeCashFlowGrowth', 'revGrowth1Yr','netIncomeGrowth1Yr', 'debt_repayment',]

healthiest_all = ['Symbol', 'ROA', 'ROE', 'currentRatio', 'debtEquityRatio', 'ebitda','piotroskiScore', 'netProfitMargin', 'priceToOperatingCashFlowsRatio']
healthiest_chosen = ['Symbol', 'ROA', 'ROE', 'currentRatio', 'debtEquityRatio','piotroskiScore' ]

analyst_rating_all = ['Symbol', 'AnalystRating', 'AnalystResponses', 'RatingRank','ResponsesRank', 'AverageRank']
analyst_rating_chosen = ['Symbol', 'AnalystRating', 'AnalystResponses', 'RatingRank','ResponsesRank', 'AverageRank']

indicators_all = ["sma","ema","wma","dema","tema","williams","rsa","adx","standardDeviation"]
indicators_chosen = ["sma","tema","rsa"]

indicator_times = ["1min","5min","15min","30min","1hour","4hour","daily"]
