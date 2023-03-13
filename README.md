# SMA_Backtesting
This is a Python backtester for a simple moving average (SMA) crossover trading strategy. The backtester calculates the performance metrics of the strategy and visualizes the results.

## REQUIREMENTS:
To use this backtester, you need:
1. A folder named data in the same location as your Python code file.

2. A CSV file named stock.csv in the data folder. The file should contain at least two columns: timestamp and close. The timestamp column should contain dates in the format yyyy-mm-dd and the close column should contain the closing prices of the stock.

## INSTALLATION:
To use this backtester, simply download the SMABacktester.py file and save it in the same location as your Python code file. Then, import the SMABacktester class in your code.<br>
or <br>
else clone the repo:
```
git clone https://github.com/Prem07a/SMA_Backtesting
```
Make a new folder inside in the same location of that of SMA_Backtesting and name it as data

Add the stock.csv file in that folder
## USAGE

Import the SMABACKTESTER:
```
from SMABacktester import SMABacktester
```
To use the backtester, create an instance of the SMABacktester class and pass the following parameters:

* symbol: the stock symbol to be backtested
* SMA_S: the short-term moving average window size
* SMA_L: the long-term moving average window size
* start: the start date of the backtesting period (format: 'yyyy-mm-dd')
* end: the end date of the backtesting period (format: 'yyyy-mm-dd')

## Available Method:

The SMABacktester class has the following methods:

    get_data(): retrieves the stock price data from the stock.csv file and calculates the logarithmic returns
    
    prepare_data(): calculates the short-term and long-term moving averages
    
    set_parameters(SMA_S=None, SMA_L=None): updates the short-term and/or long-term moving average window sizes
    
    test_strategy(): backtests the strategy and calculates the performance metrics
    
    plot_results(): visualizes the stock price, cumulative returns, and cumulative strategy returns
    
    optimize_parameters(SMA_S_range, SMA_L_range): finds the optimal short-term and long-term moving average window sizes by exhaustively testing all combinations
    
## EXAMPLE USAGE:

```
backtester = SMABacktester(symbol='SBI', SMA_S=50, SMA_L=200, start='Any', end='Any') *Note- Select date as per the data
backtester.test_strategy()
backtester.plot_results()
```
