#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POSTGRESQL HELPERS

Created on Sun Apr 17 21:20:16 2022

@author: bratislavpetkovic
"""
from sqlalchemy import column
from sqlalchemy import create_engine
# from sqlalchemy import select
from sqlalchemy import table
import pandas as pd

# CONNECT TO DB
DATABASE_URL = "postgresql://rhrqiookrgcrnz:fcd238d060c40424f6e05b4ca28b9a07126e0a29a76eb1c4f3c83530a044174b@ec2-34-194-73-236.compute-1.amazonaws.com:5432/d4nvq9ol4b3f2k"
engine = create_engine(DATABASE_URL, echo = False)
print(engine.execute("SELECT * FROM \"analyst_rating\" ").fetchone())

def fetch_symbol_metadata():
    # METADATA
    symbol_metadata = table("symbol_metadata", column("symbol"), column("companyName"), column("sector"),column("industry"), column("country"), 
                           column("exchangeShortName"), column("price"), column("marketCap"), column("isEtf"))
    symbol_metadata_stmt = symbol_metadata.select() #.where(analyst_rating.c.name == 'Bob')
    symbol_metadata_df = pd.read_sql_query(symbol_metadata_stmt, engine)
    symbol_metadata_df["Symbol"] = symbol_metadata_df["symbol"]
    del symbol_metadata_df["symbol"]
    return symbol_metadata_df

def fetch_analyst_rating():
    analyst_rating = table("analyst_rating", column("Symbol"), column("AnalystRating"), column("AnalystResponses"),
                           column("RatingRank"), column("ResponsesRank"), column("AverageRank"))
    analyst_stmt = analyst_rating.select() #.where(analyst_rating.c.name == 'Bob')
    analyst_rating_df = pd.read_sql_query(analyst_stmt, engine)     
    return analyst_rating_df

def fetch_biggest_growers():
    biggest_growers = table("biggest_growers", column("Symbol"), column("freeCashFlowGrowth"), column("revGrowth1Yr"),
                            column("revGrowth1Yr"), column("netIncomeGrowth1Yr"), column("netIncomeGrowth2Yr"), column("debt_repayment"))
    biggest_growers_stmt = biggest_growers.select() #.where(analyst_rating.c.name == 'Bob')
    biggest_growers_df = pd.read_sql_query(biggest_growers_stmt, engine) 
    return biggest_growers_df

def fetch_best_value():
    best_value = table("best_value", column("Symbol"), column("price"), column("DCF"), column("DCFminusPrice"),column("grahamMinusPrice"), column("grahamNumber"), 
                           column("yearHigh"), column("yearLow"), column("InsiderPurchased"), column("TransactionCount"), )
    best_value_stmt = best_value.select() #.where(analyst_rating.c.name == 'Bob')
    best_value_df = pd.read_sql_query(best_value_stmt, engine)
    best_value_df["Price_BV"] = best_value_df["price"]
    del best_value_df["price"]
    return best_value_df

def fetch_healthiest_companies():
    healthiest_companies = table("healthiest_companies", column("Symbol"), column("ROA"), column("ROE"),column("currentRatio"), column("debtEquityRatio"), 
                           column("ebitda"), column("piotroskiScore"), column("netProfitMargin"), column("priceToOperatingCashFlowsRatio"))
    healthiest_companies_stmt = healthiest_companies.select() #.where(analyst_rating.c.name == 'Bob')
    healthiest_companies_df = pd.read_sql_query(healthiest_companies_stmt, engine)
    return healthiest_companies_df