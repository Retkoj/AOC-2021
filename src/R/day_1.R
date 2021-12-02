setwd("C:\\Users\\j_ka_\\PycharmProjects\\AOC_2021")
data = read.table("data\\day_1.txt", header=FALSE)


## PART 1
" count the number of times a depth measurement increases from the previous measurement. "
count_increases <- function(data) {
  increases <- 0
  previous_row <- NULL
  for (i in 1:nrow(data)) {
    row <- strtoi(data[i,1])
    if (is.integer(previous_row) && (row > previous_row)) {
      increases <- increases + 1
    }
    previous_row <- row
  }
  return(increases)
}

count_increases(data)


## PART 2
" Consider sums of a three-measurement sliding window. How many sums are larger than the previous sum? "
get_three_measurement_sum <- function(data) {
  windowed_sum <- data.frame()
  for (i in 1:(nrow(data) - 2)) {
    new_value <- sum(data[i:(i+2),])
    windowed_sum <- rbind(windowed_sum, new_value)
  }
  return(windowed_sum)
}

windowed_data <- get_three_measurement_sum(data)
count_increases(windowed_data)
