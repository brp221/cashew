"""
Created on Thu Mar  3 22:36:50 2022

@author: bratislavpetkovic

@abstract: Baby algorithm which serves to pull stock market data using FMP API and generates reccomendations on potential investments. 
The limitations of this algorithm are based on the FMP API membership which was 300 API calls per minute at the time that this prototype algo was written. 
The recommendations are outputed to a excel file. I think of this process as gold panning. The program will catch a lot of dirt rocks and other nonsense and strain for gold. 
"""
from urllib.request import urlopen
import certifi
import json
#receive url contents, aprse it as JSON and return the object 
def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

#STOCK SCREENER PARAMS
# marketCapMoreThan & marketCapLowerThan : Number
# priceMoreThan & priceLowerThan : Number
# betaMoreThan & betaLowerThan : Number
# volumeMoreThan & volumeLowerThan : Number
# dividendMoreThan & dividendLowerThan : Number
# isEtf & isActivelyTrading : true/false
# sector : Consumer Cyclical - Energy - Technology - Industrials - Financial Services - Basic Materials - Communication Services - Consumer Defensive - Healthcare - Real Estate - Utilities - Industrial Goods - Financial - Services - Conglomerates
# Industry : Autos - Banks - Banks Diversified - Software - Banks Regional - Beverages Alcoholic - Beverages Brewers - Beverages Non-Alcoholic
# Country : US - UK - MX - BR - RU - HK - CA - ...
# exchange : nyse - nasdaq - amex - euronext - tsx - etf - mutual_fund
# limit : Number
# SIC Code

#min=1e7, max=3e+12,value=c(1e7,2.762836e+12)),
#/api/v3/stock-screener?marketCapMoreThan=1000000000&betaMoreThan=1&volumeMoreThan=10000&sector=Technology&exchange=NASDAQ&dividendMoreThan=0&limit=100
more_than=str(1e7) #10 million
less_than=str(1e9) # 1 billion
url = ("https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan="+more_than+"&marketCapLessThan="+less_than+"&sector=Technology&exchange=NASDAQ&dividendMoreThan=0&apikey=ce687b3fe0554890e65d6a5e48f601f9")
mid_cap_stocks = get_jsonparsed_data(url)


#COMPANY OUTLOOK 
#operatingIncomeRatio
symbols = ['AAPL', 'V', 'NVDA', 'BABA']
for i in symbols:
    print(i)
    comp_outlook_url = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol="+"NVDA"+"&apikey=ce687b3fe0554890e65d6a5e48f601f9")
    curr_comp_outlook = get_jsonparsed_data(comp_outlook_url)


#YEAR TO YEAR UPDATES 

#FINANCIAL SCORES 
#DOESN'T WORK WITH BASIC PLAN I BELIEVE  
# fin_score_url = ("https://financialmodelingprep.com/api/v4/score?symbol=AAPL&apikey=ce687b3fe0554890e65d6a5e48f601f9")
# print(get_jsonparsed_data(fin_score_url))
#altmanZscore (bankruptcy indicator)
#piotroskiScore (used to determine the strength of a firm's financial position.) https://site.financialmodelingprep.com/developer/docs/piotroski-score




#FINANCIAL GROWTH
url = ("https://financialmodelingprep.com/api/v3/financial-growth/AAPL?apikey=ce687b3fe0554890e65d6a5e48f601f9")
print(get_jsonparsed_data(url))



#EARNINGS CALENDAR 
#DOESN'T WORK WITH BASIC PLAN I BELIEVE  
#/api/v3/earning_calendar?from=2010-03-10&to=2010-05-11
url = ("https://financialmodelingprep.com/api/v3/earning_calendar?from=2010-03-10&to=2010-05-11?apikey=ce687b3fe0554890e65d6a5e48f601f9")
print(get_jsonparsed_data(url))


#STOCK NEWS 


#LIVE UPDATES ON THE USERS INVESTMENTS. e.g. APPLE releases new product tomorrow


url = ("https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey=ce687b3fe0554890e65d6a5e48f601f9")
# print(get_jsonparsed_data(url))

url = ("https://financialmodelingprep.com/api/v3/income-statement/AAPL?apikey=ce687b3fe0554890e65d6a5e48f601f9")
#print(get_jsonparsed_data(url))


