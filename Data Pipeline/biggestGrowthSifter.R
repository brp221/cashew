# BIGGEST GROWTH COPMANIES 

# FINANCIAL GROWTH 
      # -> revenueGroWth
      # -> netIncomeGrowth
      # -> ebitgrowth
      # -> debtGrowth
      # -> freeCashFlowGrowth

# ANALYST ESTIMATES ("https://financialmodelingprep.com/api/v3/analyst-estimates/AAPL?limit=30&apikey=YOUR_API_KEY")
      # compare against current revenue and earnings : 
      # 1 year in advance :
                          # estimatedRevenueAvg, estimatedEbitdaAvg, estimatedNetIncomeAvg
      # 2 year in advance : (year 2 minus estimates for year 1 or vs year current)(ranges (estimated high estimated low OR average?))
                          # estimatedRevenueAvg, estimatedEbitdaAvg, estimatedNetIncomeAvg

# EMPLOYEE COUNT (https://financialmodelingprep.com/api/v4/historical/employee_count?symbol=AAPL&apikey=YOUR_API_KEY)


#SYMBOL
#revenueGroWth NOT ESSENTIAL YET BC IT SHOWS PAST GROWTH?
#netIncomeGrowth NOT ESSENTIAL YET BC IT SHOWS PAST GROWTH?
#debtGrowth THIS GOES IN FINANCIAL HEALTH ACTUALLY
#freeCashFlowGrowth 
#employeeGrowth
#debt_repayment
#revGrowth1Yr
#revGrowth2Yr
#netIncomeGrowth1Yr
#netIncomeGrowth2Yr

#GLOBAL VARS
api_key <- 'ce687b3fe0554890e65d6a5e48f601f9'   
fmp_api_key(api_key, overwrite = TRUE)   
readRenviron('~/.Renviron') 



inputDF <- subset(allStocksFilteredSifted,
                   !is.na(allStocksFilteredSifted$AnalystRating) & allStocksFilteredSifted$AnalystResponses>5,
                   select = c("Symbol"))


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
    
    revGrowth2Yr <- (analystEstimates$estimatedRevenueAvg[[1]] - aaplFinState$revenue[[1]])/aaplFinState$revenue[[1]]
    revGrowth1Yr <- (analystEstimates$estimatedRevenueAvg[[2]] - aaplFinState$revenue[[1]])/aaplFinState$revenue[[1]]
    netIncomeGrowth2Yr <- (analystEstimates$estimatedNetIncomeAvg[[1]] - aaplFinState$netIncome[[1]])/aaplFinState$netIncome[[1]]
    netIncomeGrowth1Yr <- (analystEstimates$estimatedNetIncomeAvg[[2]] - aaplFinState$netIncome[[1]])/aaplFinState$netIncome[[1]]
    freeCashFlowGrowth <- finGrowth$freeCashFlowGrowth[1]
    finStatements$debt_repayment
    employeeGrowth3Year <- (employeeDF$employeeCount[[1]]  - employeeDF$employeeCount[[3]])/employeeDF$employeeCount[[3]]
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


biggestGrowers<-fetchGrowth(inputDF)







analystEstimatesURL <- paste("https://financialmodelingprep.com/api/v3/analyst-estimates/AAPL?limit=3&apikey=ce687b3fe0554890e65d6a5e48f601f9")
analystEstimates <- dplyr::bind_rows(makeReqParseRes(analystEstimatesURL))
analystEstimates$estimatedRevenueAvg


financialStatementsGrowthURL <- paste("https://financialmodelingprep.com/api/v3/financial-growth/AAPL?apikey=ce687b3fe0554890e65d6a5e48f601f9")
finGrowth <- dplyr::bind_rows(makeReqParseRes(financialStatementsGrowthURL))
revenueGrowth <- finGrowth$revenueGrowth[1:5]
ebitgrowth <- finGrowth$ebitgrowth[1:5]
freeCashFlowGrowth <- finGrowth$freeCashFlowGrowth[1:5]
debtGrowth <- finGrowth$debtGrowth[1:5]
netIncomeGrowth <- finGrowth$netIncomeGrowth[1:5]

#CALCULATION:
revGrowth2Yr <- (analystEstimates$estimatedRevenueAvg[[1]] - aaplFinState$revenue[[1]])/aaplFinState$revenue[[1]]
revGrowth1Yr <- (analystEstimates$estimatedRevenueAvg[[2]] - aaplFinState$revenue[[1]])/aaplFinState$revenue[[1]]
#ebitdaGrowth2Yr <- (analystEstimates$estimatedEbitdaAvg[[1]] - aaplFinState$ebitda[[1]])/aaplFinState$ebitda[[1]]
#ebitdaGrowth1Yr <- (analystEstimates$estimatedEbitdaAvg[[2]] - aaplFinState$ebitda[[1]])/aaplFinState$ebitda[[1]]
netIncomeGrowth2Yr <- (analystEstimates$estimatedNetIncomeAvg[[1]] - aaplFinState$netIncome[[1]])/aaplFinState$netIncome[[1]]
netIncomeGrowth1Yr <- (analystEstimates$estimatedNetIncomeAvg[[2]] - aaplFinState$netIncome[[1]])/aaplFinState$netIncome[[1]]



finStatements<-fmp_cash_flow("AAPL")[1:3,]
#free_cash_flow
#debt_repaymnet
#net_income


finStatementsURL <- paste("https://financialmodelingprep.com/api/v3/income-statement/AAPL?limit=5&apikey=ce687b3fe0554890e65d6a5e48f601f9")
aaplFinState<- dplyr::bind_rows(makeReqParseRes(finStatementsURL))
#revenue
#netIncome
#ebitda

employeeURL <- paste("https://financialmodelingprep.com/api/v4/historical/employee_count?symbol=AAPL&apikey=ce687b3fe0554890e65d6a5e48f601f9")
aaplEmployee<- dplyr::bind_rows(makeReqParseRes(employeeURL))
aaplEmployee <- aaplEmployee[1:5,]
employeeGrowth <- (aaplEmployee$employeeCount[[1]]  - aaplEmployee$employeeCount[[5]])/aaplEmployee$employeeCount[[5]]
#4 year growth?
# perhaps look at companies where company net_income and free cash flow has grown whereas as the number of employees has not ?



