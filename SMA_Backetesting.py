import pandas as pd
import numpy as np
from itertools import product

class SMABacktester():
    """
    A simple moving average crossover strategy backtester.
    
    Requirement
    -----------
    1. Have a folder data in same location that of your python code file.
    2. Have a csv file named stock.csv in data folder.
    
    Attributes
    ----------
    symbol : str
        the stock symbol to be backtested
    SMA_S : int
        the short-term moving average window size
    SMA_L : int
        the long-term moving average window size
    start : str
        the start date of the backtesting period (format: 'yyyy-mm-dd')
    end : str
        the end date of the backtesting period (format: 'yyyy-mm-dd')
    data : pandas.DataFrame
        the stock price and indicator data
    results : pandas.DataFrame
        the strategy performance metrics
    
    Methods
    -------
    get_data():
        retrieves the stock price data from a csv file and calculates the logarithmic returns
    prepare_data():
        calculates the short-term and long-term moving averages
    set_parameters(SMA_S=None, SMA_L=None):
        updates the short-term and/or long-term moving average window sizes
    test_strategy():
        backtests the strategy and calculates the performance metrics
    plot_results():
        visualizes the stock price, cumulative returns, and cumulative strategy returns
    optimize_parameters(SMA_S_range, SMA_L_range):
        finds the optimal short-term and long-term moving average window sizes by exhaustively testing all combinations
    
    """
    
    def __init__(self, symbol, SMA_S, SMA_L, start, end):
        """
        Initializes the backtester object with the given parameters.
        
        Parameters
        ----------
        symbol : str
            the stock symbol to be backtested
        SMA_S : int
            the short-term moving average window size
        SMA_L : int
            the long-term moving average window size
        start : str
            the start date of the backtesting period (format: 'yyyy-mm-dd')
        end : str
            the end date of the backtesting period (format: 'yyyy-mm-dd')
        
        """
        self.symbol = symbol
        self.SMA_S = SMA_S
        self.SMA_L = SMA_L
        self.start = start
        self.end = end
        self.data = None
        self.results = None
        self.get_data()
        self.prepare_data()
        
    def __repr__(self):
        """
        Returns the string representation of the object.
        """
        return "SMABacktester(symbol={}, SMA_S={}, SMA_L={}, start={}, end={})".format(self.symbol, self.SMA_S, self.SMA_L, self.start, self.end)
    
    def get_data(self):
        """
        Retrieves the stock price data from a csv file and calculates the logarithmic returns.
        """
        raw = pd.read_csv('data/stock.csv', parse_dates=['timestamp'], index_col='timestamp', usecols=['close', 'timestamp'])
        raw = raw.loc[self.start:self.end].copy()
        raw['returns'] = np.log(raw / raw.shift(1))
        self.data = raw
       
    
    def prepare_data(self):
        """
        Calculates the short-term and long-term moving averages.
        """
        data = self.data.copy()
        data['SMA_S'] = data['close'].rolling(self.SMA_S).mean()
        data['SMA_L'] = data['close'].rolling(self.SMA_L).mean()
        self.data = data
    
    def set_parameters(self, SMA_S=None, SMA_L=None):
        """
        Updates the values for the short and long Simple Moving Averages (SMA_S and SMA_L) used in the analysis.
        If a parameter value is provided, it updates the corresponding class attribute and calculates the rolling mean for
        the corresponding window size, storing the result in the data DataFrame.

        Parameters:
        -----------
        SMA_S : int, optional
            The window size (in periods) for the short Simple Moving Average. If not provided, the attribute is not updated.
        SMA_L : int, optional
            The window size (in periods) for the long Simple Moving Average. If not provided, the attribute is not updated.

        Returns:
        --------
        None
        """
        if SMA_S is not None:
            self.SMA_S = SMA_S
            self.data['SMA_S'] = self.data['close'].rolling(self.SMA_S).mean()
        if SMA_L is not None:
            self.SMA_L = SMA_L
            self.data['SMA_L'] = self.data['close'].rolling(self.SMA_L).mean()
            
    def test_strategy(self):
        """
        Tests the trading strategy based on the previously set Simple Moving Average parameters.
        Calculates the position and strategy returns, as well as cumulative returns for both, and stores the results in the
        `results` attribute.

        Returns the final performance of the strategy and its outperformance compared to the market returns.

        Returns:
        --------
        Tuple (float, float):
            - The final performance of the trading strategy, as a percentage.
            - The outperformance of the trading strategy compared to the market returns, as a percentage.
        """
        data = self.data.copy().dropna()
        data['position'] = np.where(data['SMA_S'] > data['SMA_L'], 1, -1) 
        data['strategy'] = data['position'].shift(1) * data['returns']
        data.dropna(inplace=True)
        data['creturns'] = data['returns'].cumsum().apply(np.exp)
        data['cstrategy'] = data['strategy'].cumsum().apply(np.exp)
        self.results = data
        
        perf = data['cstrategy'].iloc[-1]
        outperf = perf - data['creturns'].iloc[-1]
        return round(perf, 6), round(outperf, 6)
    
    def plot_results(self):
        """
        Plots the results of a backtesting strategy using the creturns and cstrategy columns of the results DataFrame.
        """
        if self.results is None:
            print('Run test_strategy() first.')
        else:
            title = '{} | SMA_S = {} | SMA_L= {}'.format(self.symbol, self.SMA_S, self.SMA_L)

            self.results[['creturns','cstrategy']].plot(title=title, figsize=(12,8))

    def optimize_parameters(self, SMA_S_range, SMA_L_range):
        """Optimizes the short-term and long-term simple moving average (SMA) parameters for a trading strategy.

        Parameters:
        -----------
        SMA_S_range : tuple
            A tuple specifying the range of values to use for the short-term SMA parameter, in the form (start, stop, step).
        SMA_L_range : tuple
            A tuple specifying the range of values to use for the long-term SMA parameter, in the form (start, stop, step).

        Returns:
        --------
        tuple
            A tuple containing the optimal SMA parameter values (SMA_S, SMA_L).
        float
            The best performance metric achieved by the strategy.
        """

        combinations = list(product(range(*SMA_S_range), range(*SMA_L_range)))

        results = []

        for comb in combinations:
            self.set_parameters(comb[0], comb[1])

            results.append(self.test_strategy()[0])


        best_perf = np.max(results)
        opt = combinations[np.argmax(results)]

        self.set_parameters(opt[0], opt[1])
        self.test_strategy()

        many_results = pd.DataFrame(data=combinations, columns=['SMA_S', 'SMA_L'])
        many_results['performance'] = results
        self.results_overview = many_results

        return opt, best_perf
