sa_data <- read.csv('long_ideas_out.csv', header = TRUE, stringsAsFactors = FALSE)

for (i in 1:nrow(sa_data)) {
  sa_data[i, 2] <- gsub("[[:punct:]]", "", sa_data[i, 2])
}

