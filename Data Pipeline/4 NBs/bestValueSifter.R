# BEST VALUED STOCKS 

# DCF and DCF Minus Price
# Insider Trading 
# 52 week average
# graham Number ( 2 b adjusted versus market though probably more analysis needed if this is to be incorporated )

#GLOBAL VARS
api_key <- 'ce687b3fe0554890e65d6a5e48f601f9'   
fmp_api_key(api_key, overwrite = TRUE)   
readRenviron('~/.Renviron') 

# FETCHES AND AGGREGATES INSIDER TRADING
fetchInsiderTrading <-function(inputDF){
  resultDF <- data.frame(matrix(ncol = 3, nrow = 0))
  colnames(resultDF) <- c('Symbol', 'InsiderPurchased', 'TransactionCount')
  for (i in (1:nrow(inputDF))){
    if(i%%5==0 ){
      print("SLOW DOWN BUDDY")
      Sys.sleep(12)
    }
    print(inputDF$Symbol[[i]])
    insideTradesURL <- paste("https://financialmodelingprep.com/api/v4/insider-trading?symbol=",inputDF$Symbol[[i]],"&page=0&apikey="
                             ,api_key, sep = "")
    insides<- dplyr::bind_rows(makeReqParseRes(insideTradesURL))
    #DATA MASSAGE HERE
    totalPurchased<-0
    transactionCount<-0
    if(length(insides)==0 || nrow(insides)==0){ 
      resultDF[nrow(resultDF) + 1,] = c(inputDF$Symbol[[i]], as.numeric(totalPurchased), as.numeric(transactionCount))
      next
    }
    insides<- dplyr::bind_rows(makeReqParseRes(insideTradesURL))
    insides$transactionDate <- as.Date(insides$transactionDate )
    insides <- insides %>% filter(insides$transactionDate >= (Sys.Date()-30)) 
    totalPurchased<-0
    if(nrow(insides)==0){
      resultDF[nrow(resultDF) + 1,] = c(inputDF$Symbol[[i]], as.numeric(totalPurchased), as.numeric(transactionCount))
      next
    }
    for (j in (1:nrow(insides))){
      if(insides$acquistionOrDisposition[[j]] == "D"){totalPurchased <- totalPurchased - (insides$securitiesTransacted[[j]] * insides$price)[[j]] }
      else{totalPurchased <- totalPurchased + (insides$securitiesTransacted[[j]] * insides$price)[[j]] }
    }
    print(paste("totalPurchased: ", totalPurchased, sep = ""))
    transactionCount <- transactionCount + nrow(insides)
    print(paste("transactionCount: ", transactionCount, sep = ""))
    resultDF[nrow(resultDF) + 1,] = c(inputDF$Symbol[[i]], as.numeric(totalPurchased), as.numeric(transactionCount))
  }
  
  
  resultDF$InsiderPurchased <- as.numeric(resultDF$InsiderPurchased)
  resultDF$TransactionCount <- as.numeric(resultDF$TransactionCount)
  resultDF <- resultDF %>%    #DATA QUALITY INCORPORATION
    mutate(TransactionCountBand = case_when(
      TransactionCount < 12 ~ "1-12",
      TransactionCount >= 12 & TransactionCount < 45 ~ "12-45",
      TransactionCount >= 45 ~ "45<",
    ))
  #resultDF<- resultDF %>% filter(TransactionCount > 0)
  resultDF
}

# FETCHES DCF, GRAHAM NUMBER, YEAR HIGH AND LOW, COMPUTES grahamMinusPrice
fetchIntrinsicVal<- function(inputDF){
  returnDF <- data.frame(Symbol=character(0),
                         price=numeric(0),
                         grahamNumber=numeric(0), 
                         yearHigh=numeric(0),
                         yearLow=numeric(0),
                         grahamMinusPrice=numeric(0), 
                         DCF=numeric(0),
                         DCFminusPrice=numeric(0))
  for (i in (1:nrow(inputDF))){
    print("")
    print(inputDF$Symbol[[i]])
    keyMetrics<-fmp_key_metrics(inputDF$Symbol[[i]])   #fetch company's key metrics
    print(paste("graham_number : ", keyMetrics$graham_number[[1]], sep = ""))
    #perhaps include growth of graham over time 
    companyOutlook<-fmp_company_outlook(inputDF$Symbol[[i]])
    print(paste("Price: ", companyOutlook[[1]]$profile$price,sep = "") ) 
    print(paste("52 week range: ", companyOutlook[[1]]$metrics$yearHigh[[1]], " - ", companyOutlook[[1]]$metrics$yearLow[[1]], sep=""))
    #print(paste("grahamMinuesPrice: ", grahamMinuesPrice,sep = "") ) 
    currRow <- nrow(returnDF) + 1
    grahamMinuesPrice <- as.numeric(keyMetrics$graham_number[[1]]) - as.numeric(companyOutlook[[1]]$profile$price)
    print(paste("grahamMinuesPrice: ", grahamMinuesPrice,sep = "") ) 
    print(inputDF$`DCF(IntrinsicVal)`[[i]])
    print(inputDF$DCFMinusPrice[[i]])
    returnDF[i,] <- c(inputDF$Symbol[[i]],
                      as.numeric(companyOutlook[[1]]$profile$price),
                      keyMetrics$graham_number[[1]],
                      companyOutlook[[1]]$metrics$yearHigh[[1]],
                      as.character(companyOutlook[[1]]$metrics$yearLow[[1]]),
                      as.double(grahamMinuesPrice),
                      as.numeric(inputDF$`DCF(IntrinsicVal)`[[i]]),
                      as.numeric(inputDF$DCFMinusPrice[[i]])
    )
  }
  #returnDF$grahamMinuesPrice <- as.numeric(returnDF$grahamNumber) - as.numeric(returnDF$price)
  returnDF
}

# Retrieve Symbol and DCF Value 
bestValFeedDF <- subset(stocksPicked,stocksPicked$AnalystResponses>5,select = c("Symbol", "DCF(IntrinsicVal)","DCFMinusPrice"))

insiderTradDF <- fetchInsiderTrading(bestValFeedDF) # adds Insider Trading 

intrinsicValDF <- fetchIntrinsicVal(bestValFeedDF) # adds DCF, Graham and Year High and Low 

bestValueDF <- merge(intrinsicValDF,insiderTradDF,by=c("Symbol"), all.x=TRUE)

bestValueDF$price<-as.numeric(bestValueDF$price)
bestValueDF$yearHigh<-as.numeric(bestValueDF$yearHigh)
bestValueDF$yearLow<-as.numeric(bestValueDF$yearLow)
bestValueDF$grahamNumber<-as.numeric(bestValueDF$grahamNumber)
bestValueDF$grahamMinusPrice<-as.numeric(bestValueDF$grahamMinusPrice)

# INSIDER TRADING DERIVES MARKET SENTIMENT 
# Brooks ratio, which divides total insider sales of a company by total insider trades (purchases and sales) and then averages this ratio for thousands of stocks. 
# If the average Brooks ratio is less than 40%, the market outlook is bullish; above 60% signals a bearish outlook.

#Market Adjusted graham
mean(bestValueDF$grahamMinusPrice, na.rm = T) # can't be this though because the difference depends on the price, larger price means more difference


