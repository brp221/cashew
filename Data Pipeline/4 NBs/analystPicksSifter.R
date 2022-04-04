# ANALYST PICKS 

# AVERAGE RATING BY ANALYSTS 
# AVERAGE RATING FROM companyOutlook
# NUMBER OF RESPONSES 
# (ANALYST RATING STANDARD DEVIATION )

# Better to make FMP API calls here than in the goldPanner.R !


analystRankingDF <- subset(stocksPicked,  stocksPicked$AnalystResponses>5, select = c("Symbol", "AnalystRating", "AnalystResponses"))

analystRankingDF$RatingRank <- rank(analystRankingDF$AnalystRating)
analystRankingDF$ResponsesRank <- rank(analystRankingDF$AnalystResponses)

# RANK : Maybe something more sophisticated. Maybe weight them according to responsesBand 
analystRankingDF$AverageRank <- (0.8*analystRankingDF$AnalystRating) + (0.2*analystRankingDF$AnalystResponses)

workingDir <- getwd()
setwd("/Users/bratislavpetkovic/Desktop/cashew/Data Pipeline/TABLES")
success <- write.csv(analystRankingDF,"AnalystPicks.csv", row.names = FALSE)
