library(timeDate)
library(dplyr)
library(quantmod)
library(ggplot2)
library(reshape2)

setwd("~/scrape-sa")
sa.data <- read.csv('out.txt', header = TRUE, stringsAsFactors = FALSE)

sa.ord <- arrange(sa.data, Date)
sa.2014 <- sa.ord[which(sa.ord[, 1] == "2014-01-01"):which(sa.ord[, 1] == "2014-12-31"),]
no.days <- nrow(sa.ord)

SEC.DAY <- 60 * 60 * 24
long.days <- 365
data.df <- data.frame(dates = sa.2014[,1], no.stocks = 0, avg.ret = 0, high = -9999, low = 9999, stocks = '', stringsAsFactors = FALSE)
missing.stocks = c()
for (d in 1:nrow(sa.2014)) {
  stocks <- c()
  stock.list <- strsplit(sa.2014[d, 2], split = ' ')[[1]]
  start.date = timeDate(sa.2014[d, 1], format = "%Y-%m-%d", zone = "NewYork", FinCenter = "NewYork")
  while (isWeekend(start.date)) {
    start.date = start.date + 1 * SEC.DAY
  }
  while (sa_isHoliday(start.date)) {
    start.date = start.date + 1 * SEC.DAY
  }
  long.date = start.date + long.days * SEC.DAY
  while (isWeekend(long.date)) {
    long.date = long.date + 1 * SEC.DAY
  }
  while (sa_isHoliday(long.date)) {
    long.date = long.date + 1 * SEC.DAY
  }
  total.stocks = length(stock.list)
  total.ret = 0
  
  print(sprintf("Beginning day %s", start.date))
  print(sprintf("End date is %s", long.date))
  print(sprintf("Total number of stocks is %i", total.stocks))
  for (s in stock.list) {
    if (s %in% wiki_stocks_slim$ticker) {
      start.px <- as.double(filter(wiki_stocks_slim, ticker == s, date == as.character(start.date))[1,3])
      end.px <- as.double(filter(wiki_stocks_slim, ticker == s, date == as.character(long.date))[1,3])
      if (is.na(start.px) || is.na(end.px)) {
        print(sprintf("Error with stock %s", s))
        total.stocks = total.stocks - 1
      }
      else {
        stocks <- append(stocks, s)
        return = (end.px - start.px)/start.px
        total.ret = total.ret + return
        
        if (return > data.df[d, 'high']) {
          data.df[d, 'high'] = return
        }
        if (return < data.df[d, 'low'])
          data.df[d, 'low'] = return
      }
    }
    else {
      print(sprintf("Missing stock %s", s))
      if (!(s %in% missing.stocks)) {
        missing.stocks <- append(missing.stocks, s)
      }
    }
  }
  data.df[d, 'stocks'] = paste(stocks, collapse = ' ')
  data.df[d, 'no.stocks'] = total.stocks
  data.df[d, 'avg.ret'] = total.ret/total.stocks
  print("====== Done! ======")
}

sa_isHoliday <- function(date) {
  library(timeDate)
  year = as.numeric(format(start.date, "%Y"))
  holidays = holidayNYSE(year)
  for (d in 1:length(holidays)) {
    if (date == holidays[d]) {
      return(TRUE)
    }
  }
  return(FALSE)
}

ggplot(data.df, aes(x = dates)) + 
  geom_line(aes(y = avg.ret, color = 'avg.ret')) + 
  geom_line(aes(y = high, color = 'high')) + 
  geom_line(aes(y = low, color = 'low')) + 
  ylim(-2, 2) + 
  stat_smooth(aes(x = dates, y = avg.ret), method = 'lm') +
  stat_smooth(aes(x = dates, y = high), method = 'lm') + 
  stat_smooth(aes(x = dates, y = low), method = 'lm')
