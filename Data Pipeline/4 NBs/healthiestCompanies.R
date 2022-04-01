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
  # 


finMetrics<- fmpc_financial_metrics("BABA", quarterly = F)
##currentRatio
#quickRatio
#operatingCashFlowSalesRatio  OR easier priceToOperatingCashFlowsRatio



finStatements<-fmp_cash_flow("BABA")
#debt_repayment
#operating_cash_flow



finStatementsURL <- paste("https://financialmodelingprep.com/api/v3/income-statement/BABA?limit=5&apikey=ce687b3fe0554890e65d6a5e48f601f9")
finStatements2<- dplyr::bind_rows(makeReqParseRes(finStatementsURL))
#ebitda
#netProfitMargin = netIncome /revenue *100


finRatingsURL<- paste("https://financialmodelingprep.com/api/v3/historical-rating/BABA?limit=40&apikey=ce687b3fe0554890e65d6a5e48f601f9")
finRating<- dplyr::bind_rows(makeReqParseRes(finRatingsURL))





