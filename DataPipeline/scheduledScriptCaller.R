# AUTOMATED NOTEBOOK CALLER

# FOCUS ON :
# CONCURRENCY
# API UTILIZATION
# LATENCY 
# MINIMIZE .log output 
# MINIMIZE TIME BETWEEN JOBS 
# ASYNCHRONOUS 
library(cronR)

setwd('/Users/bratislavpetkovic/Desktop/cashew/DataPipeline/FourNBs/')
analystPicksSifter <- "analystPicksSifter.R"
biggestGrowersSifter <- "biggestGrowthSifter.R"
healthiestCompaniesSifter <- "healthiestCompaniesSifter.R"
bestValueSifter <- "bestValueSifter.R"
cmd1 <- cron_rscript(analystPicksSifter)
cmd2 <- cron_rscript(biggestGrowersSifter)
cmd3 <- cron_rscript(healthiestCompaniesSifter)
cmd4 <- cron_rscript(bestValueSifter)

setwd('/Users/bratislavpetkovic/Desktop/cashew/DataPipeline/')
goldPanner <- "goldPanning.R"
cmd0 <- cron_rscript(goldPanner)

jobs<-cron_ls()
cron_add(command = cmd0, frequency = 'daily', id = 'goldPanner.R', 
         description = 'takes a boatload of mud into a pan and prepares it for gold sifting',
         at='08:45', days_of_week = c(1,2,3,4,5,6,7))                                 # 7 mins

cron_add(command = cmd1, frequency = 'daily', id = 'analystPicksSifter.R', 
         description = 'runs A.P.S NB', at='08:55', days_of_week = c(1,2,3,4,5,6,7))  # 0 mins
"y"
cron_add(command = cmd4, frequency = 'daily', id = 'bestValueSifter.R', 
         description = 'runs B.V.S NB', at='09:12', days_of_week = c(1,2,3,4,5,6,7))  # 34 mins
"y"

cron_add(command = cmd3, frequency = 'daily', id = 'healthiestCompaniesSifter.R', 
         description = 'runs H.C.S NB', at='09:02', days_of_week = c(1,2,3,4,5,6,7))  # 5 min + 
"y"
cron_add(command = cmd2, frequency = 'daily', id = 'biggestGrowthSifter.R', 
         description = 'runs B.G.S NB', at='09:04', days_of_week = c(1,2,3,4,5,6,7))  # 5 min + 
"y"