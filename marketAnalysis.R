library(ggplot2)

# RATING vs. PIOTROSKI Correlation
#set colors
linecolors <- c("#714C02", "#01587A", "#024E37")
fillcolors <- c("#9D6C06", "#077DAA", "#026D4E")
#change data type into numeric 
largeCapSifted$OverallRating<- as.numeric(largeCapSifted$OverallRating)
largeCapSifted$piotroskiScore<- as.numeric(largeCapSifted$piotroskiScore)
# partially transparent points by setting `alpha = 0.5` add colour = probBankruptcy, fill = probBankruptcy to group
ggplot(largeCapSifted, aes(OverallRating, piotroskiScore)) +
  geom_point(position=position_jitter(h=0.1, w=0.1),
             shape = 21, alpha = 0.5, size = 3) +
  geom_smooth(method='lm')+
  scale_color_manual(values=linecolors) +
  scale_fill_manual(values=fillcolors) +
  theme_bw()

# PIOTROSKI vs Altman Z 
largeCapSiftedCopy <-largeCapSifted
largeCapSiftedCopy$altmanZScoreRound<- substring(largeCapSiftedCopy$altmanZScore, 1,5)
largeCapSiftedCopy$altmanZScore <- as.numeric(largeCapSiftedCopy$altmanZScoreRound)
options(digits=16)
# partially transparent points by setting `alpha = 0.5` add colour = probBankruptcy, fill = probBankruptcy to group
ggplot(largeCapSiftedCopy, aes(altmanZScore, piotroskiScore)) +
  geom_point(position=position_jitter(h=0.1, w=0.1),
             shape = 21, alpha = 0.5, size = 3) +
  geom_smooth(method='lm')+
  scale_color_manual(values=linecolors) +
  scale_fill_manual(values=fillcolors) +
  theme_bw()


# PIOTROSKI vs Altman Z HISTOGRAM

# GRAHAM vs ACTUAL (to determine how overpriced everything is 4 normalization purposes)


