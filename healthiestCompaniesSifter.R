                                                      # HEALTHIEST COMPANIES
# LIQUIDITY (current ratio, quick ratio, and operating cash flow ratio.)
    # A quick ratio lower than 1.0 is often a warning sign, as it indicates current liabilities exceed current assets.
# SOLVENCY (debt-to-assets ratio, the interest coverage ratio, the equity ratio, and the debt-to-equity (D/E) ratio)
  #Solvency ratios calculate a company's long-term debt in relation to its assets or equity.
  #D/E ratios vary widely between industries. However, regardless of the specific nature of a business, a downward trend 
      #over time in the D/E ratio is a good indicator a company is on increasingly solid financial ground.
# OPERATING EFFICIENCY
  # Known as EBITDA (ANALYST ESTIMATES)
# Profitability (ROA, ROE )
  # Net Profit Margin:  evaluating profitability is net margin, the ratio of net profits to total revenues (Net profit margin is one of the most important indicators of a company's financial health. By tracking increases and decreases in its net profit margin, a company can assess whether current practices are working and forecast profits based on revenues)

library(fmpapi)
library(ggplot2)
library(tidyr)
library(dplyr)
require(httr)
library(fmpcloudr)
library("openxlsx")
library("writexl")

setwd("/Users/bratislavpetkovic/Desktop/cashew/")
stocksPicked <- read.xlsx("DataPipeline/pickedCompanies.xlsx")
healthiestFeedDF<- subset(stocksPicked,select = c("Symbol"))

# FETCHES COPMANY HEALTH INFORMATION
healthiestCompanies <- function(inputDF){
  returnDF <- data.frame(Symbol=character(0),
                         piotroskiScore=numeric(0),
                         quickRatio=numeric(0),
                         currentRatio=numeric(0),
                         priceToOperatingCashFlowsRatio=numeric(0),
                         ebitda=numeric(0) ,
                         ROA=numeric(0),
                         ROE=numeric(0),
                         debtEquityRatio=numeric(0),
                         netProfitMargin=numeric(0), 
                         interestCoverage=numeric(0)
                         )
  for (i in (1:nrow(inputDF))) {
  #for (i in (1:15)) {
    finMetrics<- fmpc_financial_metrics(inputDF$Symbol[[i]], quarterly = F)
    
    finScoresURL <- paste("https://financialmodelingprep.com/api/v4/score?symbol=",inputDF$Symbol[[i]],"&apikey=", api_key, sep = "") 
    finScores<- dplyr::bind_rows(makeReqParseRes(finScoresURL))
    
    finStatementsURL <- paste("https://financialmodelingprep.com/api/v3/income-statement/",inputDF$Symbol[[i]],"?limit=5&apikey=", api_key, sep = "")
    finStatements<- dplyr::bind_rows(makeReqParseRes(finStatementsURL))
    
    finRatingsURL<- paste("https://financialmodelingprep.com/api/v3/historical-rating/",inputDF$Symbol[[i]],"?limit=40&apikey=", api_key, sep = "")
    finRating<- dplyr::bind_rows(makeReqParseRes(finRatingsURL))
    
    finRatiosURL<- paste("https://financialmodelingprep.com/api/v3/ratios/",inputDF$Symbol[[i]],"?limit=10&apikey=", api_key, sep = "")
    finRatios<- dplyr::bind_rows(makeReqParseRes(finRatiosURL))
    
    print("")
    print(inputDF$Symbol[[i]])
    print(paste(" finMetrics: ", nrow(finMetrics), sep=""))
    print(paste(" finScores: ", nrow(finScores), sep=""))
    print(paste(" finStatements: ", nrow(finStatements), sep=""))
    print(paste(" finRating: ", nrow(finRating), sep=""))
    print(paste(" finRatios: ", nrow(finRatios), sep=""))
    
    ### DO A METRIC OVER TIME HERE MAYBE TO SHOW PROGRESS AND CHANGE YoY. 
    ### ON DASHBOARD DISPLAY DYNAMICALLY CHANGING GRAPH AT WHICH SUERS WILL HAVE CONTROL OVER X-AXIS AND MAYBE EVEN HOW MANY YEARS ? 
    
    #SANITY CHECK
    print(paste(" piotroskiScore: ", finScores$piotroskiScore, sep=""))
    print(paste(" quickRatio: ", finMetrics$quickRatio[[1]], sep=""))
    print(paste(" currentRatio: ", finMetrics$currentRatio[[1]], sep=""))
    print(paste(" priceToOperatingCashFlowsRatio: ", finRatios$priceToOperatingCashFlowsRatio[[1]], sep=""))
    print(paste(" ebitda: ", finStatements$ebitda[[1]], sep=""))
    print(paste(" ROA: ", finRatios$returnOnAssets[[1]], sep=""))
    print(paste(" ROE: ", finRatios$returnOnEquity[[1]], sep=""))
    print(paste(" debtEquityRatio: ", finRatios$debtEquityRatio[[1]], sep=""))
    print(paste(" netProfitMargin: ", ((finStatements$netIncome[[1]] / finStatements$revenue[[1]])*100 ), sep=""))
    print(paste(" interestCoverage: ", finRatios$interestCoverage[[1]], sep=""))
    
    print(inputDF$Symbol[[i]])
    print("")
    netProfitMargin <- ((finStatements$netIncome[[1]] / finStatements$revenue[[1]])*100 )
    
    #DATA MASSAGING PART
    #if(is.null(finRatios$interestCoverage)){finRatios$interestCoverage[[1]]<- -1.11111 } #secret value 
#    if(is.null(finScores$piotroskiScore)){finScores$piotroskiScore[[1]]<- -1.11111 } #secret value 
    #if(is.null(finRatios$returnOnAssets[[1]])){finRatios$returnOnAssets[[1]]<- -1.11111 } #secret value 
    #if(is.null(finRatios$returnOnEquity[[1]])){finRatios$returnOnEquity[[1]][[1]]<- -1.11111 } #secret value 
    #if(is.null(finRatios$debtEquityRatio[[1]])){finRatios$debtEquityRatio[[1]]<- -1.11111 } #secret value 
    #if(is.null(finRatios$priceToOperatingCashFlowsRatio[[1]])){finRatios$priceToOperatingCashFlowsRatio[[1]]<- -1.11111 } #secret value 
    
    returnDF[i,] <- c(inputDF$Symbol[[i]],
                      ifelse(length(finScores)>0,finScores$piotroskiScore[[1]],NA),
                      ifelse(length(finMetrics)>0,finMetrics$quickRatio[[1]],NA),
                      ifelse(length(finMetrics)>0,finMetrics$currentRatio[[1]],NA),
                      ifelse((length(finRatios)>0 & !is.null(finRatios$priceToOperatingCashFlowsRatio)),finRatios$priceToOperatingCashFlowsRatio[[1]],NA),
                      ifelse(length(finStatements)>0,finStatements$ebitda[[1]],NA),
                      ifelse((length(finRatios)>0 & !is.null(finRatios$returnOnAssets)),finRatios$returnOnAssets[[1]],NA),
                      ifelse((length(finRatios)>0 & !is.null(finRatios$returnOnEquity)),finRatios$returnOnEquity[[1]],NA),
                      ifelse((length(finRatios)>0  & !is.null(finRatios$debtEquityRatio)),finRatios$debtEquityRatio[[1]],NA),
                      netProfitMargin,
                      ifelse((length(finRatios)>0 & !is.null(finRatios$interestCoverage)) ,finRatios$interestCoverage[[1]],NA))
              }
  returnDF
}


healthiestCompanies <- healthiestCompanies(healthiestFeedDF)


setwd("/Users/bratislavpetkovic/Desktop/cashew/")
success <- write_xlsx(healthiestCompanies,"DataPipeline/TABLES/HealthiestCompanies.xlsx")




