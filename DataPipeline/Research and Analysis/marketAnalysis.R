library(ggplot2)
library(tidyverse)
library(hrbrthemes)

dfFormatter <- function(df){
  df$OverallRating<- as.numeric(df$OverallRating)
  df$piotroskiScore<- as.numeric(df$piotroskiScore)
  df$altmanZScore <- as.numeric(df$altmanZScore)
  df$DCFMinusPrice <- as.numeric(df$DCFMinusPrice)
  df$grahamNumber <- as.numeric(df$GrahamMinusPrice)
  df$DCFMinusPrice <- as.numeric(df$DCFMinusPrice)
  df$AnalystRating <- as.numeric(df$AnalystRating)
  df$AnalystResponses <- as.numeric(df$AnalystResponses)
  df <- df %>%    #DATA QUALITY INCORPORATION
    mutate(AnalystResponsesBand = case_when(
      AnalystResponses < 12 ~ "insufficient",
      AnalystResponses >= 12 & AnalystResponses <= 20 ~ "decent",
      AnalystResponses >= 21 ~ "great",
    ))
  
  df <- df %>%    #DATA QUALITY INCORPORATION
    mutate(AnalystRatingBand = case_when(
      AnalystRating > 4 ~ "StrongBuy",
      AnalystRating > 3 & AnalystRating <= 4 ~ "Buy",
      AnalystRating > 2 & AnalystRating <= 3 ~ "Neutral",
      AnalystRating > 1 & AnalystRating <= 2 ~ "Sell",
      AnalystRating >= 0 & AnalystRating <= 1 ~ "StrongSell",
    ))
  
  df <- df %>%    #DATA QUALITY INCORPORATION
    mutate(OverallRatingBand = case_when(
      OverallRating >= 26 ~ "26-30",
      OverallRating >=22 & OverallRating < 26 ~ "22-27",
      OverallRating >=18 & OverallRating < 22 ~ "18-21",
      OverallRating >=14 & OverallRating < 18 ~ "14-17",
      OverallRating >=10 & OverallRating < 14 ~ "10-14",
    ))
  df
}

#set colors
linecolors <- c("#714C02", "#01587A", "#024E37")
fillcolors <- c("#9D6C06", "#077DAA", "#026D4E")

allStocksUrl <- paste('https://financialmodelingprep.com//api/v3/stock-screener?isEtf=false&apikey=',api_key, sep = "")
allStocks <- dplyr::bind_rows(makeReqParseRes(allStocksUrl))
allStocksFiltered <- allStocks %>% filter(marketCap >=45000000000)
allStocksFilteredSifted <- stockSifter(allStocksFiltered)
allStocksFilteredSifted <- dfFormatter(allStocksFilteredSifted)

#--------------------------------------------------------------------------------------------------------------------

# overallRating vs. PIOTROSKI Correlation BY probBankruptcy

ggplot(allStocksFilteredSifted, aes(OverallRating, piotroskiScore,colour = probBankruptcy, fill = probBankruptcy)) +
  geom_point(position=position_jitter(h=0.1, w=0.1),
             shape = 21, alpha = 0.5, size = 3) +
  geom_smooth(method='lm')+
  scale_color_manual(values=linecolors) +
  scale_fill_manual(values=fillcolors) +
  theme_bw()
#--------------------------------------------------------------------------------------------------------------------
# PIOTROSKI vs Altman Z 
allStocksFilteredSiftedCopy <-allStocksFilteredSifted
allStocksFilteredSiftedCopy$altmanZScoreRound<- substring(allStocksFilteredSifted$altmanZScore, 1,5)
allStocksFilteredSiftedCopy$altmanZScore <- as.numeric(allStocksFilteredSifted$altmanZScoreRound)

res <-quantile(allStocksFilteredSiftedCopy$altmanZScore, probs = c(.1, .95))
allStocksFilteredSiftedCopy<- allStocksFilteredSiftedCopy %>% filter(altmanZScore <= res[[2]] )
#options(digits=16)

# partially transparent points by setting `alpha = 0.5` add colour = probBankruptcy, fill = probBankruptcy to group
ggplot(allStocksFilteredSiftedCopy, aes(altmanZScore, piotroskiScore,  fill = probBankruptcy)) +
  geom_point(position=position_jitter(h=0.1, w=0.1),
             shape = 21, alpha = 0.5, size = 3) +
  #geom_smooth(method='lm')+
  scale_color_manual(values=linecolors) +
  scale_fill_manual(values=fillcolors) +
  theme_bw()

#NOTES: Seems like after ~2, altmanZ does not impact piotroskiScore very much. 
#--------------------------------------------------------------------------------------------------------------------

# GrahamMinusPrice DISTRIBUTION (to determine how overpriced everything is 4 normalization purposes)
allStocksFilteredSiftedCopy <-allStocksFilteredSifted
res<-quantile(allStocksFilteredSiftedCopy$GrahamMinusPrice, probs = c(.05,.95), na.rm=T)
allStocksFilteredSiftedCopy<- allStocksFilteredSiftedCopy %>% filter(GrahamMinusPrice <= res[[2]] & GrahamMinusPrice >= res[[1]] & !is.na(GrahamMinusPrice))
ggplot(allStocksFilteredSiftedCopy, aes(x=GrahamMinusPrice))+
  geom_histogram(fill="#69b3a2", color="#e9ecef", alpha=0.9) +
  ggtitle("Distribution of Price Minus Graham") +
  theme_ipsum() +
  theme(
    plot.title = element_text(size=15)
  )

#--------------------------------------------------------------------------------------------------------------------
# DCFMinusPriceDISTRIBUTION (to determine how overpriced everything is 4 normalization purposes)
allStocksFilteredSiftedCopy <-allStocksFilteredSifted
res<-quantile(allStocksFilteredSiftedCopy$DCFMinusPrice, probs = c(.01, .97), na.rm=T)
allStocksFilteredSiftedCopy<- allStocksFilteredSiftedCopy %>% filter(DCFMinusPrice <= res[[2]] & DCFMinusPrice >= res[[1]] & !is.na(DCFMinusPrice) & !is.infinite(DCFMinusPrice))
allStocksFilteredSiftedCopy %>% ggplot( aes(x=DCFMinusPrice, fill=probBankruptcy))+
  geom_histogram( binwidth=3, fill="#69b3a2", color="#e9ecef", alpha=0.6, position = 'identity') +
  ggtitle("Distribution of DCF Minus Price") +
  scale_fill_manual(values=c("#69b3a2", "#404080", '#714C02')) +
  theme_ipsum() +
  labs(fill="")+
  theme(
    plot.title = element_text(size=15)
  )
#--------------------------------------------------------------------------------------------------------------------
# BoxplotDistributions
ggplot(allStocksFilteredSiftedCopy, aes(x=probBankruptcy, y=DCFMinusPrice)) + 
  geom_boxplot(outlier.colour="red", outlier.shape=1,
               outlier.size=4) +
  ggtitle("Distribution of DCF Minus Price by Probablity of Bankruptcy") 
#NOTES: DISTRESS STOCKS ARE AT A DISCOUNT :). If we had the ability to pick out distressed undervalued/discounted stocks that we knew would not go bankrupt it would be sick
#--------------------------------------------------------------------------------------------------------------------
# Analyst Rating vs DCF (Correlation)
allStocksFilteredSiftedCopy <-allStocksFilteredSifted
res<-quantile(allStocksFilteredSiftedCopy$DCFMinusPrice, probs = c(.05, .95), na.rm=T)
allStocksFilteredSiftedCopy<- allStocksFilteredSiftedCopy %>% filter(AnalystRating>0 & DCFMinusPrice <= res[[2]] & DCFMinusPrice >= res[[1]] & !is.na(DCFMinusPrice) & !is.infinite(DCFMinusPrice))

ggplot(allStocksFilteredSiftedCopy, aes(AnalystRating, DCFMinusPrice,colour = AnalystResponsesBand, fill = AnalystResponsesBand)) +
  geom_point(position=position_jitter(h=0.1, w=0.1),
             shape = 21, alpha = 0.5, size = 3) +
  geom_smooth(method='lm')+
  scale_color_manual(values=linecolors) +
  scale_fill_manual(values=fillcolors) +
  theme_bw()
#NOTES SEEMS LIKE THERE IS A POSITIVE CORRELATION THERE :) (ESPECIALLY FOR GREAT)
#--------------------------------------------------------------------------------------------------------------------
# Piotroski and OverallRatingBand Bar Chart and Band 
allStocksFilteredSiftedCopy <-allStocksFilteredSifted
res<-quantile(allStocksFilteredSiftedCopy$DCFMinusPrice, probs = c(.05, .95), na.rm=T)
allStocksFilteredSiftedCopy<- allStocksFilteredSiftedCopy %>% filter(AnalystRating>0 & DCFMinusPrice <= res[[2]] & DCFMinusPrice >= res[[1]] & !is.na(DCFMinusPrice) & !is.infinite(DCFMinusPrice))
aggregate(piotroskiScore ~ OverallRatingBand, data = allStocksFilteredSiftedCopy, FUN = mean, na.rm = TRUE)

#--------------------------------------------------------------------------------------------------------------------
# overallRating vs. PIOTROSKI Correlation BY AnalystRatingBand
allStocksFilteredSiftedCopy <-allStocksFilteredSifted
res<-quantile(allStocksFilteredSiftedCopy$AnalystResponses, probs = c(.05, .95), na.rm=T)
allStocksFilteredSiftedCopy<- allStocksFilteredSiftedCopy %>% filter(AnalystResponses>=8 & !is.na(AnalystRatingBand))

ggplot(allStocksFilteredSiftedCopy, aes(OverallRating, piotroskiScore,colour = AnalystRatingBand, fill = AnalystRatingBand)) + #
  geom_point(position=position_jitter(h=0.1, w=0.1),
             shape = 21, alpha = 0.5, size = 3) +
  geom_smooth(method='lm')+
  scale_color_manual(values=linecolors) +
  scale_fill_manual(values=fillcolors) +
  theme_bw()
#SEEMS LIKE THERE IS A CORRELATION THERE. WHERE ARE STOCKS ARE SELL or STRONGSELL THO
#--------------------------------------------------------------------------------------------------------------------
# Analyst Rating vs OverallRating Bar Chart and Band 

# GROUPINGS:  
            #X-AXIS ANALYST RATING BAND
            #Y-AXIS AVERAGE OVERALL RATING 
allStocksFilteredSiftedCopy <-allStocksFilteredSifted
res<-quantile(allStocksFilteredSiftedCopy$AnalystResponses, probs = c(.05, .95), na.rm=T)
allStocksFilteredSiftedCopy<- allStocksFilteredSiftedCopy %>% filter(AnalystResponses>=8 & !is.na(AnalystRatingBand))

# No relation Analyst Rating and OverallRating 
aggregate(allStocksFilteredSiftedCopy$AnalystRating, list(allStocksFilteredSiftedCopy$OverallRatingBand), FUN=mean) 

# No relation Analyst Rating and piotroskiScore
aggregate(allStocksFilteredSiftedCopy$AnalystRating, list(allStocksFilteredSiftedCopy$piotroskiScore), FUN=length) 
aggregate(allStocksFilteredSiftedCopy$AnalystRating, list(allStocksFilteredSiftedCopy$piotroskiScore), FUN=mean) 



#--------------------------------------------------------------------------------------------------------------------
# Analyst Rating Distribution ( OverallRating grouping)
allStocksFilteredSiftedCopy <-allStocksFilteredSifted
res<-quantile(allStocksFilteredSiftedCopy$AnalystRating, probs = c(.01, .97), na.rm=T)
allStocksFilteredSiftedCopy<- allStocksFilteredSiftedCopy %>% filter(AnalystRating >= res[[1]] & allStocksFilteredSiftedCopy$AnalystResponsesBand != "insufficient")
allStocksFilteredSiftedCopy %>% ggplot( aes(x=AnalystRating, , fill=OverallRatingBand))+
  geom_histogram(fill="#69b3a2", color="#e9ecef", alpha=0.6, position = 'identity') +
  ggtitle("Distribution of Analyst Rating") +
  scale_fill_manual(values=c("#69b3a2", "#404080", '#714C02')) +
  theme_ipsum() +
  labs(fill="")+
  theme(
    plot.title = element_text(size=15)
  )
#--------------------------------------------------------------------------------------------------------------------
# BoxplotDistributions
ggplot(allStocksFilteredSiftedCopy, aes(x=OverallRatingBand, y=AnalystRating)) + 
  geom_boxplot(outlier.colour="red", outlier.shape=1,
               outlier.size=4) +
  ggtitle("Distribution of DCF Minus Price by Probablity of Bankruptcy") 

#--------------------------------------------------------------------------------------------------------------------
# GrahamMinusPrice vs DCFMinusPrice
allStocksFilteredSiftedCopy <-allStocksFilteredSifted
res <-quantile(allStocksFilteredSiftedCopy$GrahamMinusPrice, probs = c(.02, .98), na.rm=T)
res1 <-quantile(allStocksFilteredSiftedCopy$DCFMinusPrice, probs = c(.02, .98), na.rm=T)
allStocksFilteredSiftedCopy<- allStocksFilteredSiftedCopy %>% filter(
                                    allStocksFilteredSiftedCopy$GrahamMinusPrice <= res[[2]], 
                                    allStocksFilteredSiftedCopy$GrahamMinusPrice >= res[[1]])
allStocksFilteredSiftedCopy<- allStocksFilteredSiftedCopy %>% filter(
  allStocksFilteredSiftedCopy$DCFMinusPrice <= res1[[2]], 
  allStocksFilteredSiftedCopy$DCFMinusPrice >= res1[[1]])

#options(digits=16)

# partially transparent points by setting `alpha = 0.5` add colour = probBankruptcy, fill = probBankruptcy to group
ggplot(allStocksFilteredSiftedCopy, aes(DCFMinusPrice, GrahamMinusPrice)) + #,  fill = probBankruptcy
  geom_point(position=position_jitter(h=0.1, w=0.1),
             shape = 21, alpha = 0.5, size = 3) +
  #geom_smooth(method='lm')+
  scale_color_manual(values=linecolors) +
  scale_fill_manual(values=fillcolors) +
  theme_bw()


# NEED MORE ANALYSIS HERE, SEEMS LIKE IT IS TRUE WITH NUMBERS WHICH ARE CERTAIN AMOUNT AWAY FROM ZERO 
# GRAHAM NUMBER DEFINATELY NEEDS TO BE NORMALIZED THOUGH ACROSS MARKET
#--------------------------------------------------------------------------------------------------------------------

# PERHAPS ADD INSIDER TRADING 
# Analyst Rating Distribution ( OverallRating grouping)
insideTradingDFCOPY <-insideTradingDF
insideTradingDFCOPY$InsiderPurchased <- as.numeric(insideTradingDFCOPY$InsiderPurchased)
res <-quantile(insideTradingDFCOPY$InsiderPurchased, probs = c(.03, .97), na.rm=T)
insideTradingDFCOPY <- insideTradingDFCOPY %>% filter(InsiderPurchased > res[[1]] & InsiderPurchased < res[[2]])

insideTradingDFCOPY %>% ggplot( aes(x=InsiderPurchased))+
  geom_histogram(fill="#69b3a2", color="#e9ecef", alpha=0.6, position = 'identity') +
  ggtitle("Distribution of InsiderPurchased SUM") +
  scale_fill_manual(values=c("#69b3a2", "#404080", '#714C02')) +
  theme_ipsum() +
  labs(fill="")+
  theme(
    plot.title = element_text(size=15)
  )

# BoxplotDistributions
ggplot(insideTradingDFCOPY, aes(x=TransactionCountBand, y=InsiderPurchased)) + 
  geom_boxplot(outlier.colour="red", outlier.shape=1,
               outlier.size=4) +
  ggtitle("Distribution of DCF Minus Price by Probablity of Bankruptcy") 

# TO BE USED FOR NORMALIZING ACROSS MARKET (PERHAPS INSUDSTRY TOO)
# ALTERNATIVE TO SUM MIGHT BE MEAN BECAUSE more transactions skew data. 

#--------------------------------------------------------------------------------------------------------------------
# INSIDER TRADING AND DCFMINUSPRICE CORRELATION 

#--------------------------------------------------------------------------------------------------------------------
# DEBT REPAYMENT DISTRIBUTION
res <-quantile(debt_repayment, probs = c(.02,0.1,0.25,0.5,0.75,0.9,.98), na.rm=T)
hist(debt_repayment, breaks=50)

#--------------------------------------------------------------------------------------------------------------------






