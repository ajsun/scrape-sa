library(timeDate)
library(dplyr)
library(quantmod)


sa.data <- read.csv('out.txt', header = TRUE, stringsAsFactors = FALSE)

sa.ord <- arrange(sa.data, Date)

stocks = c()
for (d in 1:nrow(sa.ord)) {
  stocks.day <- strsplit(sa.ord[d, 2], split = ' ')
  for (s in stocks.day[[1]]) {
    if (!(s %in% stocks)) {
      stocks = append(stocks, s)
    }
  }
}



