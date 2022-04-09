import pandas as pd
from sqlalchemy import create_engine

# READ THE TABLES
analystPicksDF = pd.read_excel('/Users/bratislavpetkovic/Desktop/cashew/DataPipeline/TABLES/ANalystRanking.xlsx')
biggestGrowersDF = pd.read_excel('/Users/bratislavpetkovic/Desktop/cashew/DataPipeline/TABLES/BiggestGrowers.xlsx')
HealthiestCompaniesDF = pd.read_excel('/Users/bratislavpetkovic/Desktop/cashew/DataPipeline/TABLES/HealthiestCompanies.xlsx')
BestValueDF = pd.read_excel('/Users/bratislavpetkovic/Desktop/cashew/DataPipeline/TABLES/BestValued.xlsx')

print(BestValueDF.head())

# CONNECT TO DB
DATABASE_URL = "postgresql://evkccxwslqxbud:5a4aafe1962d3ce9022c83f4e7358d2a62dc6197620ecabb0c68557ec6bb5483@ec2-52-73-155-171.compute-1.amazonaws.com:5432/de6ao7pbg15j5b"
engine = create_engine(DATABASE_URL, echo = False)

# (OVER)WRITE TABLES TO DB 
analystPicksDF.to_sql('analyst_rating', con = engine, if_exists='replace')
print(engine.execute("SELECT * FROM \"analyst_rating\" ").fetchone())


biggestGrowersDF.to_sql('biggest_growers', con = engine, if_exists='replace')
print(engine.execute("SELECT * FROM \"biggest_growers\" ").fetchone())


HealthiestCompaniesDF.to_sql('healthiest_companies', con = engine, if_exists='replace')
print(engine.execute("SELECT * FROM \"healthiest_companies\" ").fetchone())


BestValueDF.to_sql('best_value', con = engine, if_exists='replace')
print(engine.execute("SELECT * FROM \"best_value\" ").fetchone())

