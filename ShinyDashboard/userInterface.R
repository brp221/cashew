library(shiny)
library(shinydashboard)
library(fmpapi)
library(ggplot2)
library(tidyr)
library(dplyr)
library(fmsb)#Spider Graph 
library(reshape2)#melt
require(httr)

#MAKES AN FMP API REQUEST AND PARŠES THEIR RESPONSE
makeReqParseRes <- function(url){
  res <- httr::GET(url, httr::add_headers(.headers=headers), query = params)
  content(res)
}

#MAKES A RADAR CHART 
radarChart <- function(dataframe, symbol, competitorSymbol){
  colnames(dataframe) <- c("DiscountedCashFlow" , "ReturnOnInvestment" , "ReturnOnAssests" , "Debt2Equity" , "Price2Eearnings", "Price2Book" )
  rownames(dataframe) <- c(symbol, competitorSymbol)
  # To use the fmsb package, I have to add 2 lines to the dataframe: the max and min of each variable to show on the plot!
  dataframe <- rbind(rep(5,1) , rep(0,1) , dataframe)
  
  # Color vector
  colors_border=c( rgb(0.2,0.5,0.5,0.9), rgb(0.8,0.2,0.5,0.9) )
  colors_in=c( rgb(0.2,0.5,0.5,0.4), rgb(0.8,0.2,0.5,0.4) )
  
  # plot with default options:
  radarchart( dataframe  , axistype=1 , 
            #custom polygon
            pcol=colors_border , pfcol=colors_in , plwd=1 , plty=1,
            #custom the grid
            cglcol="grey", cglty=1, axislabcol="grey", caxislabels=seq(0,5,1), cglwd=0.8,
            #custom labels
            vlcex=0.8, title=paste(symbol," : Investment Reccomendations")
  )
  # Add a legend
  legend(x=1, y=1, legend = rownames(dataframe[-c(1,2),]), bty = "n", pch=20 , col=colors_in , text.col = "grey", cex=1.2, pt.cex=3)
}

#CREATES FINANCIAL PPER COMPARISON DF FOR THE RADAR CHART
financialsPeerComparsion <- function(compOutlookRating, symbol){
  #Get Peers 
  url = paste('https://financialmodelingprep.com/api/v4/stock_peers?symbol=',symbol,'&apikey=',api_key,sep="")
  peers <- makeReqParseRes(url)
  DCF <- c()
  ROE <- c()
  ROA <- c()
  DE  <- c()
  PE  <- c()
  PB  <- c()
  index = 1
  for (i in 1:length(peers[[1]]$peersList)) {
    peerCompOutlook <- fmp_company_outlook(peers[[1]]$peersList[i][[1]])
    if(length(peerCompOutlook)==0 ){next}
    if(length(peerCompOutlook[[1]]$rating)==0 ){next}
    DCF[index] = peerCompOutlook[[1]]$rating$ratingDetailsDCFScore
    ROE[index] = peerCompOutlook[[1]]$rating$ratingDetailsROEScore
    ROA[index] = peerCompOutlook[[1]]$rating$ratingDetailsROAScore
    DE[index] = peerCompOutlook[[1]]$rating$ratingDetailsDEScore
    PE[index] = peerCompOutlook[[1]]$rating$ratingDetailsPEScore
    PB[index] = peerCompOutlook[[1]]$rating$ratingDetailsPBScore
    index=index+1
  }
  finComparsionDf <- data.frame(
             "DCF"=c(compOutlookRating$ratingDetailsDCFScore, mean(DCF)),
             "ROE"=c(compOutlookRating$ratingDetailsROEScore, mean(ROE)),
             "ROA"=c(compOutlookRating$ratingDetailsROAScore, mean(ROA)),
             "DE"=c(compOutlookRating$ratingDetailsDEScore, mean(DE)),
             "PE"=c(compOutlookRating$ratingDetailsPEScore,mean(PE)),
             "PB"=c(compOutlookRating$ratingDetailsPBScore,mean(PB)))
  return(finComparsionDf)
}

#GLOBALS
api_key <- 'ce687b3fe0554890e65d6a5e48f601f9'
fmp_api_key(api_key, overwrite = TRUE)
readRenviron('~/.Renviron') 
headers = c(`Upgrade-Insecure-Requests` = '1')
params = list(`datatype` = 'json')
allStocksUrl <- paste('https://financialmodelingprep.com//api/v3/stock-screener?isEtf=false&apikey=',api_key, sep = "")
stockDF <- dplyr::bind_rows(makeReqParseRes(allStocksUrl))
randomPopSymbol <- "TSLA"
earningsCalendar<- fmp_earnings_calendar() #Important to display on the stock screener page filter to exclude BS
sectPerformance<-fmp_sector_performance() # Dique about this line  

body <- dashboardBody(
  mainPanel(
    tabsetPanel(
      #SCREENER
      tabPanel("SCREENER",
        fluidRow(
          valueBox("Variables", subtitle = "Use to filter", color="olive"),
          valueBox("Stocks", subtitle = "Curr stocks filtered",color="blue")
        ),
        fluidRow(
          box(title = "FILTER",solidHeader = T,
              width = 4,collapsible = T,
              selectizeInput('sectors', 'SECTOR', choices = c("choose" = "", c("ALL", unique(sectPerformance$sector))),selected= "ALL"),
              selectizeInput('industry', 'INDUSTRY', choices = c("choose" = "", c("ALL", unique(stockDF$industry))),selected= "ALL"),
              sliderInput(inputId="market_cap", label="Market Cap", min=1e7, max=3e+12,value=c(1e7,2.762836e+12)),
          ),
          box(title = "STOCKS", solidHeader = T,
              width = 8, collapsible = T,
              div(DT::DTOutput("stockTable"), style = "font-size: 70%;")
          ),
        ),
      ),
      #FINANCIALS
      tabPanel("FINANCIALS", 
        fluidRow(
         valueBox("Ratios", subtitle = "important copmany scores", color="blue"),
         valueBox("Production", subtitle = "earnings,free cash flow and debt repayment", color="light-blue"),#navy
         valueBox("Price", subtitle = "Price Over Time ", color="olive")
        ),
        fluidRow(
           box(
              selectizeInput('symbol', 'symbol', choices = c("choose" = "", unique(stockDF$symbol)),selected=randomPopSymbol ),
              textInput("symbolText", label = h3("Stock symbol goes here..."), value = randomPopSymbol),
              actionButton("fireAction", "Lookup"),
              div(DT::DTOutput("financialTable"), style = "font-size: 70%;"), width = 4
           ),
           box(
               plotOutput("barChart"), width = 4
               #, height = 4
           ),
           box(
             selectInput("priceInterval", label = h3("Select box"), 
                         choices = list("1min"="1min", "5min"="5min", "15min"="15min", "30min"="30min", "1hour"="1hour", "4hour"="4hour"),selected = "1min"),
             plotOutput("priceChart"), width = 4
             #, height = 7
           )
         ),
      ),
      #INVESTMENT
      tabPanel("INVESTMENT",
               fluidRow(
                 valueBox("Rating", subtitle = "Use to filter", color="blue"),
                 valueBox("News", subtitle = "Curr stocks filtered", color="teal"),
                 valueBox("Scores", subtitle = "Important Scores", color="olive")
               ),
               fluidRow(
                 box(title = "Rating",solidHeader = T,
                     width = 4,collapsible = T,
                     plotOutput("radarChart")
                 ),
                 box(title = "News", solidHeader = T,
                     width = 4, collapsible = T,
                     div(DT::DTOutput("stockNews"), style = "font-size: 70%;")
                 ),
                 box(title = "News", solidHeader = T,
                     width = 4, collapsible = T,
                     div(DT::DTOutput("scoresTable"), style = "font-size: 70%;")
                 ),
               ),
      )
    )
  )
)


ui = dashboardPage(
  dashboardHeader(title = "Cashew"),
  dashboardSidebar(disable = TRUE, 
                   menuItem("SCREENER", tabName = "SCREENER", icon = icon("filter")),
                   menuItem("FINANCIALS", tabName = "FINANCIALS", icon = icon("filter")),
                   menuItem("INVESTMENT", tabName = "INVESTMENT", icon = icon("filter"))
                   ),
  body
)
server = function(input, output, session) {

  stockDF <- fmp_screen_stocks()
  stockDF <- stockDF[stockDF$is_etf == FALSE,]
  headers = c(
    `Upgrade-Insecure-Requests` = '1'
  )
  params = list(
    `datatype` = 'json'
  )
  #GLOBAL VARIABLE(S) 2B CHANGED DYNAMICALLY wrap in observe or reqctive??
  dynamicVals <- reactiveValues(
    companyOutlook=fmp_company_outlook(randomPopSymbol),
    selectedSymbol=randomPopSymbol,
    keyMetrics = fmp_key_metrics(randomPopSymbol),
    scores = httr::GET(url = paste('https://financialmodelingprep.com/api/v4/score?symbol=',randomPopSymbol,'&apikey=',api_key, sep = ""), 
                               httr::add_headers(.headers=headers), query = params)
    )
  
  #Observe Some Action Button (runs once when button pressed)
  observeEvent(input$fireAction, {
    dynamicVals$companyOutlook <- fmp_company_outlook(input$symbolText)
    dynamicVals$selectedSymbol <- input$symbolText
    dynamicVals$keyMetrics <- fmp_key_metrics(input$symbolText)
    dynamicVals$scores <- httr::GET(url = paste('https://financialmodelingprep.com/api/v4/score?symbol=',input$symbolText,'&apikey=',api_key, sep = ""), 
                                    httr::add_headers(.headers=headers), query = params)
  })
  

  #observeEvent(input$symbol,{
   # dynamicVals$companyOutlook <- fmp_company_outlook(input$symbol)
   # dynamicVals$selectedSymbol <- input$symbol
   # dynamicVals$keyMetrics <- fmp_key_metrics(input$symbol)
   # dynamicVals$scores <- httr::GET(url = paste('https://financialmodelingprep.com/api/v4/score?symbol=',input$symbol,'&apikey=',api_key, sep = ""), 
   #                                httr::add_headers(.headers=headers), query = params)
  #})
  
  # fetch Scores. Eventually refactor whole application to use this style rather than 3rd party library 
  getScores <-reactive({
    scores_df <- as.data.frame(content(dynamicVals$scores))
    #print(res$status_code)
    #print(as.data.frame(content(dynamicVals$scores)))
    print(scores_df)
    #print(colnames(scores_df))
    #print(dynamicVals$keyMetrics$graham_number[[1]] )
    print(dynamicVals$scores)
    scoresTable <- data.frame(Score<-c("AltmanZScore", "Piotroski Score", "Graham Score" ),
                              Values<-c(scores_df$altmanZScore, scores_df$piotroskiScore, dynamicVals$keyMetrics$graham_number[[1]]))
    scoresTable 
    #%>%
     # mutate("Sentiment" = case_when(
     #   Value ~ as.character(icon("check-circle-o", lib = "font-awesome"))
     #   endsWith(ID, "S") ~ as.character9icon("minus-circle", lib = "font-awesome")
     # ))
    #Value<-c(content(res)[[1]]$altmanZScore,
    #         content(res)[[1]]$piotroskiScore,
    #         dynamicVals$keyMetrics$graham_number[1] 
    
  })
  output$scoresTable <- DT::renderDataTable({
    DT::datatable(getScores(),selection="single",rownames = F, colnames = F)
  })
  
  #generate radarChart of the Ratings
  radarChartData <- reactive({
    print(dynamicVals$companyOutlook[[1]]$rating)
    print(input$symbolText)
    data <- financialsPeerComparsion(dynamicVals$companyOutlook[[1]]$rating, input$symbolText)
    #radarData <- data.frame("DCF"=c(dynamicVals$companyOutlook[[1]]$rating$ratingDetailsDCFScore, 3),
     #                       "ROE"=c(dynamicVals$companyOutlook[[1]]$rating$ratingDetailsROEScore, 3),
      #                      "ROA"=c(dynamicVals$companyOutlook[[1]]$rating$ratingDetailsROAScore, 3),
      #                      "DE"=c(dynamicVals$companyOutlook[[1]]$rating$ratingDetailsDEScore, 3),
       #                     "PE"=c(dynamicVals$companyOutlook[[1]]$rating$ratingDetailsPEScore,3),
     #                       "PB"=c(dynamicVals$companyOutlook[[1]]$rating$ratingDetailsPBScore,3))
    print(data)
  })
  output$radarChart <- renderPlot(
    print(
      radarChart(radarChartData(),dynamicVals$selectedSymbol, "PEERS" )
    )
  )
  
  # get news content reactively
  newsData <- reactive({
    #compOutlook <- fmp_company_outlook(input$symbol)
    newsTable <- data.frame(Columns <- c(dynamicVals$companyOutlook[[1]]$stockNews$title), Values <- c(dynamicVals$companyOutlook[[1]]$stockNews$url))
  })
  output$stockNews <- DT::renderDataTable({
    DT::datatable(newsData(),selection="single",rownames = F, colnames = F)
  })
  
  # fetch selected stock based on the range provided
  priceData <- reactive({
    priceRange<- fmp_prices(dynamicVals$selectedSymbol, interval = input$priceInterval)
    priceRange<-priceRange[,1:5]
    priceRangeMelt <- melt(priceRange ,  id.vars = 'date', variable.name = 'series')
  })
  # line graph of the chart 
  output$priceChart <- renderPlot(
    print(
        ggplot(data=priceData(), aes(x=date, y=value, group=1)) + geom_line()+geom_point()) #col=series
  )
  
  # produce data for the bar chart
  barChartData <- reactive({
    #cash flow 4 year-period
    cashFlow <- fmp_cash_flow(dynamicVals$selectedSymbol)
    #cashFlow$free_cash_flow
    #cashFlow$net_income
    keyMetricsTall <- data.frame(group = c("NetIncome", "FreeCashFlow"),
                                     year_2021 = c(cashFlow$net_income[1], cashFlow$free_cash_flow[1]),
                                     year_2020 = c(cashFlow$net_income[2], cashFlow$free_cash_flow[2]),
                                     year_2019 = c(cashFlow$net_income[3], cashFlow$free_cash_flow[3]),
                                     year_2018 = c(cashFlow$net_income[4], cashFlow$free_cash_flow[4]))
    
    keyMetricsTall <- keyMetricsTall %>% gather(key=Year, value=Value, year_2018:year_2021)
    keyMetricsTall
    
  })
  # bar Chart of Net Income/Earnings and Free Cash Flow 
  output$barChart <- renderPlot(
    print(ggplot(barChartData(), aes(Year, Value, fill = group)) + geom_col(position = "dodge") + ggtitle(dynamicVals$selectedSymbol))
  )
  
  # fetching 52 week price data of stock 
  priceDistrData<-reactive({
    # 52 week min and max. Also used to generate graph coming soon?
    yearPrice<- fmp_daily_prices(dynamicVals$selectedSymbol, last_n = 5*52)
  })
  # histogram distribution of a 52 week opening price of the Stock
  output$priceDistributionHistogram<-renderPlot(
    print(
        ggplot(priceDistrData(), aes(x=open))+
        geom_histogram(color="darkblue", fill="lightblue", bins = 20)) #bins = 30
  )
  # company growth and Outlook 
  outlookAndGrowth<-reactive({
    #Coming Soon : comp_outlook<-fmp_company_outlook(input$symbol)
    #OPTIONAL : growth<-fmp_financial_growth(input$symbol)
  })
  
  # filter data for the stock screener
  filterData <- reactive({
    #filter by sector
    if(input$sectors!="ALL"){
      stockDF <-subset(stockDF, stockDF$sector == input$sectors ,select = c("symbol", "company_name", "price", "sector","market_cap"))
    }
    #filter by industry
    if(input$industry!="ALL"){
      stockDF <-subset(stockDF, stockDF$industry == input$industry ,select = c("symbol", "company_name", "price", "sector","market_cap"))
    }
    
    stockDF <-subset(stockDF, stockDF$market_cap > input$market_cap[1] & stockDF$market_cap < input$market_cap[2]
                     ,select = c("symbol", "company_name", "price", "sector","market_cap"))
    })
  
  # return the filtered stock screener
  output$stockTable <- DT::renderDataTable({
    DT::datatable(filterData(),selection="single",rownames = F)
  })
  
  # financial data for the company. (Cautious of #API calls)
  financialData<-reactive({
    curr_symbol <-  dynamicVals$selectedSymbol
    
    #profile
    profile<-fmp_profile(curr_symbol)
    #profile$price
    #profile$range
    
    #ratios Tentative (willing to sacrifice to decrease # of calls)
    #finRatios<-fmp_ratios(input$symbol)
    #finRatios$cash_flow_to_debt_ratio

    #keyMetrics
    keyMetrics <- fmp_key_metrics(curr_symbol)
    #keyMetrics$pe_ratio
    #keyMetrics$pb_ratio
    #keyMetrics$curr_ratio
    #keyMetrics$enterprise_value
    #keyMetrics$enterprise_value_over_ebitda
    #keyMetrics$debt_to_equity
    #keyMetrics$graham_number
    #keyMetrics$debt_to_equity
    #keyMetrics$free_cash_flow_per_share
      
    #rating (in depth)
    #rating <-fmp_rating(curr_symbol)
    #line these up next to fin markers
    
    #cash flow 4 year-period
    #cashFlow <- fmp_cash_flow(curr_symbol)
    #cashFlow$free_cash_flow
    #cashFlow$net_income
    #cashFlow$debt_repayment
    
    #Compose dataframe here 
    financialsTable <- data.frame(Columns <-c("Price", 
                                              "[1-Y]PriceRange", 
                                              "IntrinsicValue", 
                                              "Price/Earnings", 
                                              "EnterpriseValue", 
                                              "E.B.I.T.D.A.", 
                                              "EV/EBITDA", 
                                              "CurrentRatio"),
                                  Values<-c(profile$price, 
                                            profile$range, 
                                            "Coming Soon :)",
                                            keyMetrics$pe_ratio[1],
                                            keyMetrics$enterprise_value[1], 
                                            (keyMetrics$enterprise_value[1]/keyMetrics$enterprise_value_over_ebitda[1]),
                                            keyMetrics$enterprise_value_over_ebitda[1], 
                                            keyMetrics$current_ratio[1]  ))
  })
  # return the financial data
  output$financialTable <- DT::renderDataTable({
    DT::datatable(financialData(),selection="single",rownames = F, colnames = F)
  })
  
  ##someday useful: updateSelectizeInput(session, 'selectInput', choices = c('a','b','c'), server = TRUE)
}
  
shinyApp(ui =ui, server = server)