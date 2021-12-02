library(here)

data <- read.table(here("data", "day_2.txt"), header=FALSE)
names(data) <- c("direction", "steps")


## PART 1
" It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:

 - forward X increases the horizontal position by X units.
 - down X increases the depth by X units.
 - up X decreases the depth by X units. 

What do you get if you multiply your final horizontal position by your final depth?
"

make_moves <- function(moves) {
  horizontal <- 0
  depth <- 0
  for (i in 1:nrow(moves)){
    row <- moves[i,]
    if (row$direction == 'forward') {
      horizontal = horizontal + strtoi(row$steps)
    } else if (row$direction == 'up') {
      depth = depth - strtoi(row$steps)
    } else if (row$direction == 'down') {
      depth = depth + strtoi(row$steps)
    }
  }
  return(horizontal * depth)
}
make_moves(data)

## PART 2
" 
In addition to horizontal position and depth, you'll also need to track a third value, aim, which also starts at 0. The commands also mean something entirely different than you first thought:

 - down X increases your aim by X units.
 - up X decreases your aim by X units.
 - forward X does two things:
   - It increases your horizontal position by X units.
   - It increases your depth by your aim multiplied by X.

What do you get if you multiply your final horizontal position by your final depth?
"

make_moves_and_aim <- function(moves) {
  horizontal <- 0
  depth <- 0
  aim <- 0
  for (i in 1:nrow(moves)){
    row <- moves[i,]
    if (row$direction == 'forward') {
      horizontal = horizontal + strtoi(row$steps)
      depth <- depth + aim * strtoi(row$steps)
    } else if (row$direction == 'up') {
      aim = aim - strtoi(row$steps)
    } else if (row$direction == 'down') {
      aim = aim + strtoi(row$steps)
    }
  }
  return(horizontal * depth)
}
make_moves_and_aim(data)



