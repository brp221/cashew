# BIGGEST GROWTH COPMANIES 

# SYMBOL
# revenueGrowth NOT ESSENTIAL YET BC IT SHOWS PAST GROWTH?
# netIncomeGrowth NOT ESSENTIAL YET BC IT SHOWS PAST GROWTH?
# debtGrowth THIS GOES IN FINANCIAL HEALTH ACTUALLY
# freeCashFlowGrowth 
# employeeGrowth
# debt_repayment
# revGrowth1Yr
# revGrowth2Yr
# netIncomeGrowth1Yr
# netIncomeGrowth2Yr
library(fmpapi)
library(ggplot2)
library(tidyr)
library(dplyr)
require(httr)
library(fmpcloudr)
library("openxlsx")
library("writexl")


#GLOBAL VARS
api_key <- 'ce687b3fe0554890e65d6a5e48f601f9'   
fmp_api_key(api_key, overwrite = TRUE)   
readRenviron('~/.Renviron') 

setwd("/Users/bratislavpetkovic/Desktop/cashew/")
stocksPicked <- read.xlsx("DataPipeline/pickedCompanies.xlsx")
biggestGrowthFeedDF<- subset(stocksPicked,select = c("Symbol" ))

#biggestGrowthFeedDF <- subset(stocksPicked,stocksPicked$AnalystResponses>5,select = c("Symbol", "DCF(IntrinsicVal)","DCFMinusPrice"))


# fetches growth KPIs 
fetchGrowth <- function(inputDF){
  returnDF <- data.frame(Symbol=character(0),
                         freeCashFlowGrowth=numeric(0),
                         revGrowth1Yr=numeric(0),
                         revGrowth2Yr=numeric(0),
                         netIncomeGrowth1Yr=numeric(0),
                         netIncomeGrowth2Yr=numeric(0),
                         debt_repayment=numeric(0),
                         employeeGrowth=numeric(0))
  for (i in (1:nrow(inputDF))) {
  #for (i in (1:15)) {
    #fetch analyst estimates
    analystEstimatesURL <- paste("https://financialmodelingprep.com/api/v3/analyst-estimates/",inputDF$Symbol[[i]],"?limit=3&apikey=ce687b3fe0554890e65d6a5e48f601f9", sep = "")
    analystEstimates <- dplyr::bind_rows(makeReqParseRes(analystEstimatesURL))
    #fetch current growth 
    financialStatementsGrowthURL <- paste("https://financialmodelingprep.com/api/v3/financial-growth/",inputDF$Symbol[[i]],"?apikey=ce687b3fe0554890e65d6a5e48f601f9", sep = "")
    finGrowth <- dplyr::bind_rows(makeReqParseRes(financialStatementsGrowthURL))
    #fetch income statements 
    incomeStatementsURL <- paste("https://financialmodelingprep.com/api/v3/income-statement/",inputDF$Symbol[[i]],"?limit=5&apikey=ce687b3fe0554890e65d6a5e48f601f9", sep = "")
    incomeStatements<- dplyr::bind_rows(makeReqParseRes(incomeStatementsURL))
    #fetch debt repayment + free cash flow(rolling)
    finStatements<-fmp_cash_flow(inputDF$Symbol[[i]])[1:3,]
    #free_cash_flow
    #debt_repaymnet
    #net_income
    
    #fetch employee count 
    employeeURL <- paste("https://financialmodelingprep.com/api/v4/historical/employee_count?symbol=",inputDF$Symbol[[i]],"&apikey=ce687b3fe0554890e65d6a5e48f601f9", sep = "")
    employeeDF<- dplyr::bind_rows(makeReqParseRes(employeeURL))
    employeeDF <- employeeDF[1:3,]
    
    #SANITY CHECK 
    print("")
    print(inputDF$Symbol[[i]])
    print(paste("nrow(analystEstimates): ", nrow(analystEstimates)))
    print(paste("nrow(finGrowth): ", nrow(finGrowth)))
    print(paste("nrow(incomeStatements): ", nrow(incomeStatements)))
    print(paste("nrow(finStatements): ", nrow(finStatements)))
    print(paste("nrow(employeeDF): ", nrow(employeeDF)))
    
    revGrowth2Yr <- (analystEstimates$estimatedRevenueAvg[[1]] - incomeStatements$revenue[[1]])/incomeStatements$revenue[[1]]
    revGrowth1Yr <- (analystEstimates$estimatedRevenueAvg[[2]] - incomeStatements$revenue[[1]])/incomeStatements$revenue[[1]]
    netIncomeGrowth2Yr <- (analystEstimates$estimatedNetIncomeAvg[[1]] - incomeStatements$netIncome[[1]])/incomeStatements$netIncome[[1]]
    netIncomeGrowth1Yr <- (analystEstimates$estimatedNetIncomeAvg[[2]] - incomeStatements$netIncome[[1]])/incomeStatements$netIncome[[1]]
    freeCashFlowGrowth <- finGrowth$freeCashFlowGrowth[1]
    #employeeGrowth3Year <- (employeeDF$employeeCount[[1]]  - employeeDF$employeeCount[[3]])/employeeDF$employeeCount[[3]]
    #APPEND TO DB 
    returnDF[i,] <- c(inputDF$Symbol[[i]],
                      as.numeric(finGrowth$freeCashFlowGrowth[1]),
                      as.numeric(revGrowth1Yr[1]),
                      as.numeric(revGrowth2Yr[1]),
                      as.numeric(netIncomeGrowth1Yr[1]),
                      as.numeric(netIncomeGrowth2Yr[1]),
                      as.numeric(finStatements$debt_repayment[1]),
                      as.character("comingSoon"))
  }
  returnDF
}

# ranks and sorts symbols the df
rankSymbols <- function(){}


biggestGrowers<-fetchGrowth(biggestGrowthFeedDF)

biggestGrowersPercent <- biggestGrowers
biggestGrowersPercent$freeCashFlowGrowth <- as.numeric(biggestGrowersPercent$freeCashFlowGrowth) * 100
biggestGrowersPercent$revGrowth1Yr <- as.numeric(biggestGrowersPercent$revGrowth1Yr) * 100
biggestGrowersPercent$revGrowth2Yr <- as.numeric(biggestGrowersPercent$revGrowth2Yr) * 100
biggestGrowersPercent$netIncomeGrowth1Yr <- as.numeric(biggestGrowersPercent$netIncomeGrowth1Yr) * 100
biggestGrowersPercent$netIncomeGrowth2Yr <- as.numeric(biggestGrowersPercent$netIncomeGrowth2Yr) * 100
biggestGrowersPercent$debt_repayment <- as.numeric(biggestGrowersPercent$debt_repayment)



biggestGrowers$freeCashFlowGrowth <- as.numeric(biggestGrowers$freeCashFlowGrowth)
biggestGrowers$revGrowth1Yr <- as.numeric(biggestGrowers$revGrowth1Yr)
biggestGrowers$revGrowth2Yr <- as.numeric(biggestGrowers$revGrowth2Yr)
biggestGrowers$netIncomeGrowth1Yr <- as.numeric(biggestGrowers$netIncomeGrowth1Yr)
biggestGrowers$netIncomeGrowth2Yr <- as.numeric(biggestGrowers$netIncomeGrowth2Yr)
biggestGrowers$debt_repayment <- as.numeric(biggestGrowers$debt_repayment)

setwd("/Users/bratislavpetkovic/Desktop/cashew/")
success <- write_xlsx(biggestGrowers,"DataPipeline/TABLES/BiggestGrowers.xlsx")





