
#Created on Thu Mar  3 22:36:50 2022

#@author: bratislavpetkovic

#@ abstract:
#           goldPanner generates a dataframe by fetching information (symbol, DCF,...) in a for loop using the FMP API and outputs it to a csv to be used by the 4 NBs. 
#           informatino necessary : "Symbol",("Price"? v vvolatile tho) "DCF(IntrinsicVal)","DCFMinusPrice", "AnalystRating", "AnalystResponses" 
#@parameters:
#           MARKET CAP SIZE
#           EXCHANGE? ( Foreign Markets incorporate)



library(fmpapi)
library(tidyr)
library(dplyr)
require(httr)
library(fmpcloudr)
library("writexl")

print(paste("KICK-OFF : ", Sys.time())) 
#GLOBAL VARS
api_key <- 'ce687b3fe0554890e65d6a5e48f601f9'   
fmp_api_key(api_key, overwrite = TRUE)   
fmpc_set_token(api_key)
readRenviron('~/.Renviron') 
headers = c(`Upgrade-Insecure-Requests` = '1')
params = list(`datatype` = 'json')

#MAKES AN FMP API REQUEST AND PAR$ES THEIR RESPONSE
makeReqParseRes <- function(url){
  res <- httr::GET(url, httr::add_headers(.headers=headers), query = params)
  content(res)
}

allStocksUrl <- paste('https://financialmodelingprep.com//api/v3/stock-screener?isEtf=false&apikey=',api_key, sep = "")
stocksDF<- dplyr::bind_rows(makeReqParseRes(allStocksUrl))

# produce calendar of earnigns to be released
upcomingEarningsCal <- fmp_earnings_calendar()

#FETCH STOCKS VIA PARAMETERS<- c(marketCapMoreThan, marketCapLowerThan, sector, limit, exchange)
marketCapMoreThan <- as.character(1e7)
marketCapLowerThan <- as.character(1e9)
sectors <- unique(stocksDF$sector)
industry <- unique(stocksDF$industry)

#DEFINE MARKET CAP CATEGORIES
cutoff <- 10000000000
bundleCap <- stocksDF %>% filter(marketCap >= cutoff)

megaCap <- stocksDF %>% filter(marketCap >=200000000000)
largeCap <- stocksDF %>% filter(marketCap <200000000000 & marketCap >=10000000000)
midCap <- stocksDF %>% filter(marketCap >=2000000000 & marketCap <10000000000)
smallCap <- stocksDF %>% filter(marketCap >=300000000 & marketCap <2000000000)
microCap <- stocksDF %>% filter(marketCap <300000000 )

#ANALYST RATINGS : computes average of the analyst rating ( soon to include standard deviation) 
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

#PICKS STOCKS
stocksPicker <- function(selectedStocks){
  #PREPARE THE OUTPUT DF 
  stockMetaData <- data.frame(matrix(ncol = 5, nrow = 0))
  colnames(stockMetaData) <- c('Symbol', 'Price','DCF', 'AnalystRating', 'AnalystResponses' )
  for (i in 1:(nrow(selectedStocks)-1)){
  #for (i in 1:100){
    print(selectedStocks$symbol[[i]])
    if(is.null(selectedStocks$sector[[i]]) | selectedStocks$sector[[i]]=="" ){
      #print("SKIP\n")
      next}
    
    outlookUrl=paste('https://financialmodelingprep.com/api/v4/company-outlook?symbol=',selectedStocks$symbol[[i]],'&apikey=',api_key, sep="")
    companyOutlook <-makeReqParseRes(outlookUrl)    #fetch company outlook
    
    #ANALYST RATINGS 
    analystRatingURL <- paste('https://financialmodelingprep.com/api/v3/analyst-stock-recommendations/',selectedStocks$symbol[[i]],'?limit=15&apikey=', api_key, sep = "")
    analystRating <- dplyr::bind_rows(makeReqParseRes(analystRatingURL))

    if(length(analystRating)>0){analystRating <- formatAnalystRanking(analystRating)}
    dcf<-fmpc_financial_dcfv(selectedStocks$symbol[[i]])
    
    #SANITY CHECK 
    #print("RATING:")
    #print(analystRating$average)
    #print("# of Analysts:")
    #print(analystRating$totalRespondents[[1]])
    #print("DCF:")
    #print(dcf$dcf)
    #print(selectedStocks$symbol[[i]])
    
    #Important line. If any data is missing do not include such a company
    if(length(companyOutlook)==0| length(companyOutlook$rating)==0  | length(analystRating)==0 ){
      #print(paste(" DATA MISSING : ",selectedStocks$symbol[[i]]))
      next
    }
    if(is.null(dcf$dcf)){dcf$dcf = -1.111}
    #provide data 
    stockMetaData[nrow(stockMetaData) + 1,] = c(selectedStocks$symbol[[i]],
                                                companyOutlook$profile$price, 
                                                dcf$dcf,
                                                ifelse(length(analystRating)>0,analystRating$average[[1]],0),# CONVERT INTO LIST/OBJECT DATA FORMAT  
                                                ifelse(length(analystRating)>0,analystRating$totalRespondents[[1]],0))# CONVERT INTO LIST/OBJECT DATA FORMAT  
  }
  
  #compute difference between DCF and current price
  #print(stockMetaData$probBankruptcy)
  stockMetaData$DCFMinusPrice <-(as.numeric(stockMetaData$DCF) - as.numeric(stockMetaData$Price))
  stockMetaData$AnalystResponses <- as.numeric(stockMetaData$AnalystResponses)
  stockMetaData$AnalystRating <- as.numeric(stockMetaData$AnalystRating)
  stockMetaData
} 

# SIFTS STOCKS FOR GOLD 
stockSifter <- function(df, altZScoreHigher, overallRating, discountThresh ){
  #get rid of companies which are high risk factors
  df <- df %>% filter(altmanZScore >= altZScoreHigher & OverallRating > overallRating & DCFMinusPrice >= discountThresh)
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

stocksPicked <- stocksPicker(bundleCap)
#stocksSifted<- stockSifter(stocksPicked, altZScoreHigher = 1.0, overallRating = 12, discountThresh = -1000)
stocksPicked$DCF <- as.numeric(stocksPicked$DCF)
stocksPicked$Price <- as.numeric(stocksPicked$Price)

setwd("/Users/bratislavpetkovic/Desktop/cashew/")
write_xlsx(stocksPicked,"DataPipeline/pickedCompanies.xlsx")

# TOOK 7 MINS + TO COMPLETE FOR A BUNDLE CAP OF 1371 COMPANIES
print(paste("FINAL WHISTLE: ", Sys.time())) 



# earnings release calendar 
#nextWeekEarnings <- filterByCalendar(upcomingEarningsCal,Sys.Date()+7, Sys.Date())
#nextMonthEearnings <- filterByCalendar(upcomingEarningsCal,Sys.Date()+31, Sys.Date())
#nextNDayEarnings <- filterByNDaysCalendar(upcomingEarningsCal, 3)






