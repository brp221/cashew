
#Created on Thu Mar  3 22:36:50 2022

#@author: bratislavpetkovic

#@abstract: Baby algorithm which serves to pull stock market data using FMP API and generates reccomendations on potential investments. 
#The limitations of this algorithm are based on the FMP API membership which was 300 API calls per minute at the time that this prototype algo was written. 
#The recommendations are outputed to an excel file. I think of this process as gold panning. The program will catch a lot of dirt rocks and other nonsense and strain for gold. 

library(fmpapi)
library(ggplot2)
library(tidyr)
library(dplyr)
require(httr)

#GLOBAL VARS
api_key <- 'ce687b3fe0554890e65d6a5e48f601f9'   
fmp_api_key(api_key, overwrite = TRUE)   
readRenviron('~/.Renviron') 
headers = c(`Upgrade-Insecure-Requests` = '1')
params = list(`datatype` = 'json')
url = 'https://financialmodelingprep.com/api/v4/earnings-calendar-confirmed-api?from=2022-03-10&to=2022-05-01'


allStocksUrl <- paste('https://financialmodelingprep.com//api/v3/stock-screener?isEtf=false&apikey=',api_key, sep = "")
allStocks <- dplyr::bind_rows(makeReqParseRes(allStocksUrl))

#FETCH STOCKS VIA PARAMETERS<- c(marketCapMoreThan, marketCapLowerThan, sector, limit, exchange)
marketCapMoreThan <- as.character(1e7)
marketCapLowerThan <- as.character(1e9)
sectors <- unique(allStocks$sector)
industry <- unique(allStocks$industry)
ratingEnumarated <- c('S+' = c(30,31,32,33),'S')
#stockScreenBySectorURL <- paste('https://financialmodelingprep.com//api/v3/stock-screener?sector=',sectors[6],'&isEtf=false&apikey=',api_key, sep = "")
#selectedStocks<-makeReqParseRes(stockScreenBySectorURL)

#DEFINE MARKET CAP CATEGORIES
megaCap <- allStocks %>% filter(marketCap >=200000000000)
largeCap <- allStocks %>% filter(marketCap <200000000000 & marketCap >=10000000000)
midCap <- allStocks %>% filter(marketCap >=2000000000 & marketCap <10000000000)
smallCap <- allStocks %>% filter(marketCap >=300000000 & marketCap <2000000000)
microCap <- allStocks %>% filter(marketCap <300000000 )


#MAKES AN FMP API REQUEST AND PARŠES THEIR RESPONSE
makeReqParseRes <- function(url){
  res <- httr::GET(url, httr::add_headers(.headers=headers), query = params)
  content(res)
}




#SIFT THROUGH STOCKS, PICK OUT GOLD 
stockSifter <- function(selectedStocks){
  #PREPARE THE OUTPUT DF 
  stockMetaData <- data.frame(matrix(ncol = 12, nrow = 0))
  colnames(stockMetaData) <- c('Symbol', 'Price','OverallRating', 'DiscountedCashFlow', 'ReturnOnEarnings','ReturnOnAssets','Debt/Equity',
                               'Price/Earnings','Price/Book','altmanZScore','piotroskiScore', 'grahamNumber' )
  for (i in 1:(nrow(selectedStocks)-1)){
    #for (i in 500:1000){
    #fetch company outlook
    outlookUrl=paste('https://financialmodelingprep.com/api/v4/company-outlook?symbol=',selectedStocks$symbol[[i]],'&apikey=',api_key, sep="")
    companyOutlook <-makeReqParseRes(outlookUrl)
    #fetch company's scores
    scoresUrl=paste('https://financialmodelingprep.com/api/v4/score?symbol=',selectedStocks$symbol[[i]],'&apikey=',api_key, sep = "")
    scores <- makeReqParseRes(scoresUrl)
    #fetch company's key metrics
    keyMetrics<-fmp_key_metrics(selectedStocks$symbol[[i]])
    #Important line. If any data is missing do not include such a company
    #print(paste("Key Metrics length", length(keyMetrics[1,])))
    #print(paste("Key Metrics rows", nrow(keyMetrics[1,])))
    #print(paste("Key Metrics length", length(scores)))
    #print(paste("Key Metrics rows", nrow(scores)))
    print(selectedStocks$symbol[[i]])
    if(length(keyMetrics[1,])==0 | length(scores)==0 | length(companyOutlook)==0| length(companyOutlook$rating)==0 ){
      if(length(keyMetrics[1,])==0){
        print(paste("keyMetrics DATA MISSING : ",selectedStocks$symbol[[i]]))
      }
      if(length(scores)==0){
        print(paste("scores DATA MISSING : ",selectedStocks$symbol[[i]]))
      }
      if(length(companyOutlook)==0 | length(companyOutlook$rating)==0 ){
        print(paste("companyOutlook DATA MISSING : ",selectedStocks$symbol[[i]]))
      }
      next
    }
    else (
      print(c(selectedStocks$symbol[[i]],
              companyOutlook$profile$price, 
              companyOutlook$rating[[1]]$ratingDetailsDCFScore,
              companyOutlook$rating[[1]]$ratingDetailsROEScore,
              companyOutlook$rating[[1]]$ratingDetailsROAScore, 
              companyOutlook$rating[[1]]$ratingDetailsDEScore, 
              companyOutlook$rating[[1]]$ratingDetailsPEScore, 
              companyOutlook$rating[[1]]$ratingDetailsPBScore, 
              scores[[1]]$altmanZScore, 
              scores[[1]]$piotroskiScore, 
              keyMetrics$graham_number[[1]]))
    )
    ratingOverall <- companyOutlook$rating[[1]]$ratingDetailsDCFScore+ companyOutlook$rating[[1]]$ratingDetailsROEScore+ 
      companyOutlook$rating[[1]]$ratingDetailsROAScore + companyOutlook$rating[[1]]$ratingDetailsDEScore + 
      companyOutlook$rating[[1]]$ratingDetailsPEScore + companyOutlook$rating[[1]]$ratingDetailsPBScore
    #provide data 
    stockMetaData[nrow(stockMetaData) + 1,] = c(selectedStocks$symbol[[i]],
                                                as.numeric(companyOutlook$profile$price), 
                                                as.numeric(ratingOverall),
                                                as.numeric(companyOutlook$rating[[1]]$ratingDetailsDCFScore),
                                                as.numeric(companyOutlook$rating[[1]]$ratingDetailsROEScore),
                                                as.numeric(companyOutlook$rating[[1]]$ratingDetailsROAScore), 
                                                as.numeric(companyOutlook$rating[[1]]$ratingDetailsDEScore), 
                                                as.numeric(companyOutlook$rating[[1]]$ratingDetailsPEScore), 
                                                as.numeric(companyOutlook$rating[[1]]$ratingDetailsPBScore), 
                                                as.numeric(scores[[1]]$altmanZScore), 
                                                as.numeric(scores[[1]]$piotroskiScore), 
                                                as.numeric(keyMetrics$graham_number[[1]]))
  }
  
  #compute difference between Graham_number and current price
  #print(stockMetaData$grahamNumber)
  stockMetaData$PriceMinusGraham<-(as.numeric(stockMetaData$grahamNumber) - as.numeric(stockMetaData$Price))
  #likelihood of bankruptcy according to the altmanZScore
  stockMetaData <- stockMetaData %>%
    mutate(probBankruptcy = case_when(
      altmanZScore > 2.6 ~ "safe",
      altmanZScore > 1.1 & altmanZScore <= 2.6 ~ "grey",
      altmanZScore <= 1.1 ~ "distress"
    ))
  #print(stockMetaData$probBankruptcy)
  #sort by mpg (ascending) and cyl (descending)
  stockMetaData
} 

#SORT/PICK NUGGETS OF GOLD FROM BEST OT WORST 
stockPicker <- function(selectedStocks){
  #Order stocks in descending order (overall rating, piotroski score, PriceMinusGraham)
  stockMetaDataOrdered <- stockMetaData[order(stockMetaData$OverallRating,stockMetaData$piotroskiScore, stockMetaData$PriceMinusGraham, decreasing = c(T,T, T)),]
  
  #get rid of companies which are high risk factors
  stockMetaDataOrdered <- stockMetaDataOrdered %>% filter(probBankruptcy == "safe" | altmanZScore >= 2)
}

#FILTER FUNCTIONS
# filter by risk of bankruptcy ( altmanZScore )
filterByRisk <-function(df, higherThan, lessThan=1000){
  res_df <- df %>% filter(altmanZScore >=higherThan & altmanZScore <=lessThan )
  return(res_df)
}

#filter by the value of price ( graham Number)
filterByValue <- function(df, priceDiffLower, priceDiffHigher=max()){
  res_df <- df %>% filter(PriceMinusGraham>=priceDiffLower & PriceMinusGraham <= priceDiffHigher)
  return(res_df)
}

#filter by overall company health ( piotroskiScore)
filterByPiotroski <- function(df, scoreLow, scoreHigh = NULL ){
  if(is.null(scoreHigh)){
    #scoreHigh = min(as.numeric(df$piotroskiScore), na.rm=TRUE)
    res_df <- df %>% filter(piotroskiScore>=scoreLow & piotroskiScore <= scoreHigh)
    return(res_df)
  }
  res_df <- df %>% filter(piotroskiScore>=scoreLow )
  return(res_df)
}

#filter by releasedEarnings
filterByCalendar<-function(date1, date2){
  url = paste('https://financialmodelingprep.com/api/v4/earnings-calendar-confirmed-api?from=', date1,'&to=', date2, sep = "")
  #&apikey=ce687b3fe0554890e65d6a5e48f601f9
  #earnings_calendar <- makeReqParseRes(url)
  print(url)
  #earnings_calendar
}
#TO BE TESTED
calendarURL <- paste('https://financialmodelingprep.com/api/v4/earnings-calendar-confirmed-api?from=2021-03-10&to=2022-10-01&apikey=',api_key, sep = "")
earnCal <- makeReqParseRes(calendarURL)

earnings_calendar_2 <- filterByCalendar('2022-03-10', '2022-03-29')


#LOOK TO THE FUTURE FIND NEW GOLD FIELDS
#earningsCalendar


largeCapSifted <- stockSifter(largeCap)
largeCapOrdered<- stockPicker(largeCapSifted)

megaCapSifted <- stockSifter(megaCap)


