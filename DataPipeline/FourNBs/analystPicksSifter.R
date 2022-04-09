# ANALYST PICKS 

# AVERAGE RATING BY ANALYSTS 
# AVERAGE RATING FROM companyOutlook
# NUMBER OF RESPONSES 
# (ANALYST RATING STANDARD DEVIATION )

library(fmpapi)
library(ggplot2)
library(tidyr)
library(dplyr)
require(httr)
library(fmpcloudr)
library("openxlsx")
library("writexl")


print(paste("KICK-OFF: ", Sys.time())) 

#GLOBAL VARS
api_key <- 'ce687b3fe0554890e65d6a5e48f601f9'   
fmp_api_key(api_key, overwrite = TRUE)   
readRenviron('~/.Renviron') 

setwd("/Users/bratislavpetkovic/Desktop/cashew/")
stocksPicked <- read.xlsx("DataPipeline/pickedCompanies.xlsx")

analystRankingDF <- subset(stocksPicked,  stocksPicked$AnalystResponses>5, select = c("Symbol", "AnalystRating", "AnalystResponses"))

analystRankingDF$RatingRank <- rank(analystRankingDF$AnalystRating)
analystRankingDF$ResponsesRank <- rank(analystRankingDF$AnalystResponses)

# RANK : Maybe something more sophisticated. Maybe weight them according to responsesBand 
analystRankingDF$AverageRank <- (0.8*analystRankingDF$AnalystRating) + (0.2*analystRankingDF$AnalystResponses)

setwd("/Users/bratislavpetkovic/Desktop/cashew/")
success <- write_xlsx(analystRankingDF,"DataPipeline/TABLES/AnalystRanking.xlsx")

print(paste("FINAL WHISTLE: ", Sys.time())) 
