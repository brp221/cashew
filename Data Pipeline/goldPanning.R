
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
library("writexl")

#GLOBAL VARS
api_key <- 'ce687b3fe0554890e65d6a5e48f601f9'   
fmp_api_key(api_key, overwrite = TRUE)   
readRenviron('~/.Renviron') 
headers = c(`Upgrade-Insecure-Requests` = '1')
params = list(`datatype` = 'json')
#MAKES AN FMP API REQUEST AND PARŠES THEIR RESPONSE
makeReqParseRes <- function(url){
  res <- httr::GET(url, httr::add_headers(.headers=headers), query = params)
  content(res)
}

allStocksUrl <- paste('https://financialmodelingprep.com//api/v3/stock-screener?isEtf=false&apikey=',api_key, sep = "")
allStocks <- dplyr::bind_rows(makeReqParseRes(allStocksUrl))

url <- paste('https://financialmodelingprep.com//api/v3/financial-growth/AAPL&apikey=', api_key, sep = "")
aaplGrowth <- fmp_financial_growth('AAPL')
upcomingEarningsCal <- fmp_earnings_calendar()
#FETCH STOCKS VIA PARAMETERS<- c(marketCapMoreThan, marketCapLowerThan, sector, limit, exchange)
marketCapMoreThan <- as.character(1e7)
marketCapLowerThan <- as.character(1e9)
sectors <- unique(allStocks$sector)
industry <- unique(allStocks$industry)

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

#ANALYST RATINGS 
formatAnalystRanking <- function(df, n=3){
  if(length(df)==0){
    NULL
    }
  df <-df[1:n,]
  df$average<-0
  df$totalRespondents <-0
  #print("PRELOOP SUCCESS")
  for (i in 1:nrow(df)) {
    #print(paste("i:", i, sep = ""))
    total <- c()
    if(df$analystRatingsStrongBuy[[i]] != 0){total <- c(total,rep(5, df$analystRatingsStrongBuy[[i]]))}
    if(df$analystRatingsbuy[[i]] != 0){total <- c(total,rep(4, df$analystRatingsbuy[[i]]))}
    if(df$analystRatingsHold[[i]] != 0){total <- c(total,rep(3, df$analystRatingsHold[[i]]))}
    if(df$analystRatingsSell[[i]] != 0){total <- c(total,rep(2, df$analystRatingsSell[[i]]))}
    if(df$analystRatingsStrongSell[[i]] != 0){total <- c(total,rep(1, df$analystRatingsStrongSell[[i]]))}
    #print(total)
    df$average[[i]] <- mean(total)
    df$totalRespondents[[i]] <- df$analystRatingsStrongBuy[[i]] + df$analystRatingsbuy[[i]] + df$analystRatingsHold[[i]]+ df$analystRatingsSell[[i]] + df$analystRatingsStrongSell[[i]]
  }
  df
}

#SIFT THROUGH STOCKS, PICK OUT GOLD 
stockSifter <- function(selectedStocks){
  #PREPARE THE OUTPUT DF 
  stockMetaData <- data.frame(matrix(ncol = 15, nrow = 0))
  colnames(stockMetaData) <- c('Symbol', 'Price','OverallRating', 'DiscountedCashFlow', 'ReturnOnEarnings','ReturnOnAssets','Debt/Equity',
                               'Price/Earnings','Price/Book','altmanZScore','piotroskiScore', 'grahamNumber', 'DCF(IntrinsicVal)', 'AnalystRating', 'AnalystResponses' )
  for (i in 1:(nrow(selectedStocks)-1)){
    #for (i in 500:1000){
    print(selectedStocks$symbol[[i]])
    if(is.null(selectedStocks$sector[[i]]) | selectedStocks$sector[[i]]=="" ){next}
    
    
    outlookUrl=paste('https://financialmodelingprep.com/api/v4/company-outlook?symbol=',selectedStocks$symbol[[i]],'&apikey=',api_key, sep="")
    companyOutlook <-makeReqParseRes(outlookUrl)    #fetch company outlook
    
    scoresUrl=paste('https://financialmodelingprep.com/api/v4/score?symbol=',selectedStocks$symbol[[i]],'&apikey=',api_key, sep = "")
    scores <- makeReqParseRes(scoresUrl) #fetch company's financial scores
    
    keyMetrics<-fmp_key_metrics(selectedStocks$symbol[[i]])   #fetch company's key metrics
    
    
    #TAP INTO FUTURE GROWTH ESTIMATED: #GrabBoth Things? 
    estGrowthURL = paste('https://financialmodelingprep.com/api/v3/analyst-estimates/',selectedStocks$symbol[[i]],'?apikey=', api_key, sep = "")
    estimatedGrowth <- dplyr::bind_rows(makeReqParseRes(estGrowthURL))
    
    
    #ANALYST RATINGS 
    analystRatingURL <- paste('https://financialmodelingprep.com/api/v3/analyst-stock-recommendations/',selectedStocks$symbol[[i]],'?limit=15&apikey=', api_key, sep = "")
    analystRating <- dplyr::bind_rows(makeReqParseRes(analystRatingURL))
    #print("RATING:")
    if(length(analystRating)>0){analystRating <- formatAnalystRanking(analystRating)}
    #else{
    #  analystRating$average<-NULL
    #  analystRating$totalRespondents<-c(0)
    #  }
    #print("DCF:")
    #DCF
    dcf<-fmpc_financial_dcfv(selectedStocks$symbol[[i]])
    
    #SANITY CHECK 
    print("RATING:")
    print(analystRating$average)
    print("# of Analysts:")
    print(analystRating$totalRespondents[[1]])
    print("DCF:")
    print(dcf$dcf)
    print(selectedStocks$symbol[[i]])
    
    #Important line. If any data is missing do not include such a company
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
                                                as.numeric(keyMetrics$graham_number[[1]]), 
                                                as.numeric(dcf$dcf),
                                                ifelse(length(analystRating)>0,as.numeric(analystRating$average[[1]]),0),# CONVERT INTO LIST/OBJECT DATA FORMAT  
                                                ifelse(length(analystRating)>0,as.numeric(analystRating$totalRespondents[[1]]),0))# CONVERT INTO LIST/OBJECT DATA FORMAT  
  }
  
  #compute difference between Graham_number and current price
  #print(stockMetaData$grahamNumber)
  stockMetaData$GrahamMinusPrice<-(as.numeric(stockMetaData$grahamNumber) - as.numeric(stockMetaData$Price))
  #likelihood of bankruptcy according to the altmanZScore
  stockMetaData <- stockMetaData %>%
    mutate(probBankruptcy = case_when(
      altmanZScore > 2.6 ~ "safe",
      altmanZScore > 1.1 & altmanZScore <= 2.6 ~ "grey",
      altmanZScore <= 1.1 ~ "distress"
    ))
  #print(stockMetaData$probBankruptcy)
  stockMetaData$DCFMinusPrice <-(as.numeric(stockMetaData$`DCF(IntrinsicVal)`) - as.numeric(stockMetaData$Price))
  stockMetaData
} 

#SORT/PICK NUGGETS OF GOLD FROM BEST OT WORST 
stockPicker <- function(df, altZScoreHigher, overallRating, discountThresh ){
  #get rid of companies which are high risk factors
  df <- df %>% filter(altmanZScore >= altZScoreHigher & OverallRating > overallRating & PriceMinusGraham >= discountThresh)

  #Order stocks in descending order (overall rating, piotroski score, PriceMinusGraham)
  df <- df[order(df$OverallRating,df$piotroskiScore, df$PriceMinusGraham, decreasing = c(T,T,T)),]
}

#FILTER FUNCTIONS
# filter by risk of bankruptcy ( altmanZScore )
filterByRisk <-function(df, higherThan, lessThan=1000){
  return(df %>% filter(altmanZScore >=higherThan & altmanZScore <=lessThan ))
}

#filter by the value of price ( graham Number)
filterByValue <- function(df, priceDiffLower, priceDiffHigher=max()){
  return(df %>% filter(PriceMinusGraham>=priceDiffLower & PriceMinusGraham <= priceDiffHigher))
}

#filter by overall company health ( piotroskiScore)
filterByPiotroski <- function(df, scoreLow, scoreHigh = NULL ){
  if(is.null(scoreHigh)){ #scoreHigh = min(as.numeric(df$piotroskiScore), na.rm=TRUE)
    return(df %>% filter(piotroskiScore>=scoreLow & piotroskiScore <= scoreHigh))
  }
  return(df %>% filter(piotroskiScore>=scoreLow ))
}

#filter releasedEarnigns by Date 
filterByCalendar<-function(df, beforeDate, afterDate){
  return(upcomingEarningsCal %>% filter(date<= beforeDate & date>= afterDate))
}

#filter by releasedEarnings
filterByNDaysCalendar<-function(df, n){
  return(upcomingEarningsCal %>% filter(date<= (Sys.Date()+n) & date>= Sys.Date()))
}

largeCapSifted <- stockSifter(largeCap)
largeCapOrdered<- stockPicker(largeCapSifted, 1.5, 20, -5)
write_xlsx(largeCapOrdered,"/Users/bratislavpetkovic/Desktop/cashew/Data Pipeline/DraftOutput1.xlsx")


megaCapSifted <- stockSifter(megaCap)
megaCapOrdered <- stockPicker(megaCapSifted, 1.5, 20, -5)

#Get Peers 
url = 'https://financialmodelingprep.com/api/v4/stock_peers?symbol=V&apikey=ce687b3fe0554890e65d6a5e48f601f9'
peers <- makeReqParseRes(url)

#LOOK TO THE FUTURE FIND NEW GOLD FIELDS INCORPORATE GROWTH
nextWeekEarnings <- filterByCalendar(upcomingEarningsCal,Sys.Date()+7, Sys.Date())
nextMonthEearnings <- filterByCalendar(upcomingEarningsCal,Sys.Date()+31, Sys.Date())
nextNDayEarnings <- filterByNDaysCalendar(upcomingEarningsCal, 3)


#Creating objects for a symbol 



#analystRatingURL <- paste('https://financialmodelingprep.com/api/v3/analyst-stock-recommendations/V?limit=15&apikey=', api_key, sep = "")
#analystRating <- dplyr::bind_rows(makeReqParseRes(analystRatingURL))
#analystRating <- formatAnalystRanking(analystRating)






