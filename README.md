# Advent of Code 2021

## System
- Windows 10
- Python 3.8
- R 3.5.1

## Run Python code

Create Conda environment from file:  
`conda env create --file AOC_2021.yaml`

or install requirements using pip:  
`pip install -r requirements.txt`

To run the code of a day:  
`python ./src/day_[x].py [path/to/input_day_x].txt`  
For example: `python ./src/day_1.py ./data/day_1.txt`  

This outputs the answer to the command line  
`Output: [X]`

## Run R
Requires 'here' package, run the following:  
`install.packages("here")`

Data is expected to be in `[project/path]/data/day_[x].txt`  
For example `./data/day_1.txt` for the first day