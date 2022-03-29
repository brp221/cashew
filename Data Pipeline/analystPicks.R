# ANALYST PICKS 

# AVERAGE RATING BY ANALYSTS 
# AVERAGE RATING FROM companyOutlook
# NUMBER OF RESPONSES 
# (ANALYST RATING STANDARD DEVIATION )

outputDf <- subset(allStocksFilteredSifted,
            !is.na(allStocksFilteredSifted$AnalystRating) & allStocksFilteredSifted$AnalystResponses>5,
            select = c("Symbol", "AnalystRating", "AnalystResponses"))

outputDf$RatingRank <- rank(outputDf$AnalystRating)
outputDf$ResponsesRank <- rank(outputDf$AnalystResponses)
outputDf$AverageRank <- 0.8*outputDf$AnalystRating + 0.2*outputDf$AnalystResponses
# Maybe something more sophisticated. Maybe weight them according to responsesBand 