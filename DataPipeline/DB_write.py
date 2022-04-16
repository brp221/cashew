import pandas as pd
from sqlalchemy import create_engine

from urllib.request import urlopen
import certifi
import json

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


# METADATA TABLE

screenerURL = ("https://financialmodelingprep.com/api/v3/stock-screener?limit=3000&apikey=ce687b3fe0554890e65d6a5e48f601f9")
metadataDF = pd.DataFrame.from_dict(get_jsonparsed_data(screenerURL))
metadataDF_sub = metadataDF[['symbol', 'companyName', 'marketCap', 'sector', 'industry',
       'price', 'lastAnnualDividend','exchangeShortName', 'country', 'isEtf',]]


# READ THE TABLES
analystPicksDF = pd.read_excel('/Users/bratislavpetkovic/Desktop/cashew/DataPipeline/TABLES/ANalystRanking.xlsx')
analystPicksDF=analystPicksDF.round(2)

biggestGrowersDF = pd.read_excel('/Users/bratislavpetkovic/Desktop/cashew/DataPipeline/TABLES/BiggestGrowers.xlsx')
biggestGrowersDF=biggestGrowersDF.round(2)

HealthiestCompaniesDF = pd.read_excel('/Users/bratislavpetkovic/Desktop/cashew/DataPipeline/TABLES/HealthiestCompanies.xlsx')
HealthiestCompaniesDF=HealthiestCompaniesDF.round(2)

BestValueDF = pd.read_excel('/Users/bratislavpetkovic/Desktop/cashew/DataPipeline/TABLES/BestValued.xlsx')
BestValueDF=BestValueDF.round(2)

print(BestValueDF.head())

# CONNECT TO DB
DATABASE_URL = "postgresql://rhrqiookrgcrnz:fcd238d060c40424f6e05b4ca28b9a07126e0a29a76eb1c4f3c83530a044174b@ec2-34-194-73-236.compute-1.amazonaws.com:5432/d4nvq9ol4b3f2k"
engine = create_engine(DATABASE_URL, echo = False)

# (OVER)WRITE TABLES TO DB 
analystPicksDF.to_sql('analyst_rating', con = engine, if_exists='replace')
print(engine.execute("SELECT * FROM \"analyst_rating\" ").fetchone())


metadataDF_sub.to_sql('symbol_metadata', con = engine, if_exists='replace')
print(engine.execute("SELECT * FROM \"symbol_metadata\" ").fetchone())


biggestGrowersDF.to_sql('biggest_growers', con = engine, if_exists='replace')
print(engine.execute("SELECT * FROM \"biggest_growers\" ").fetchone())


HealthiestCompaniesDF.to_sql('healthiest_companies', con = engine, if_exists='replace')
print(engine.execute("SELECT * FROM \"healthiest_companies\" ").fetchone())


BestValueDF.to_sql('best_value', con = engine, if_exists='replace')
print(engine.execute("SELECT * FROM \"best_value\" ").fetchone())

