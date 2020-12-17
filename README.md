![](https://github.com/philos123/PyBacktesting/blob/master/images/artificial-intelligence.png)

# Using Elliott Wave Theory to forecast the financial markets and optimize with genetic algorithms


Hi! 

My name is Philippe. The goal of this project is to model the Elliott Wave Theory to forecast the financial markets. Once we have the model and know the parameters, we optimize it using a machine learning technique called genetic algorithm. Then we test it using Walk forward optimization. The fitness function we're using for optimization and testing is the Sharpe ratio. 

The experiment was carried out on the EUR/USD currency pair on an hourly basis. The period was from 2015/10 to 2020/04 (including 2 training and 2 testing periods). The training periods were 18 months each (from 2015-10-15 to 2017-04-15 and from 2018-01-15 to 2019-07-15) and the testing periods were 9 months each (from 2017-04-15 to 2018-01-15 and from 2019-07-15 to 2020-04-15). 

The Sharpe ratio was above 3 for each training period (which is excellent). The results were mixed for the training periods. The Sharpe ratio was 1.63 for the first training period (which is really good) and -13.99 for the second period with 0 winning trades (which is really bad).

One of the issue with the model during the testing periods is that it generated few trades (11 for the first testing period and 10 for second testing period). This may be due to an over optimized model which caused overfitting. We could also test the same model on different assets and different timeframes.

The library is built so that it is possible to modify the trading strategy by creating modules in the different packages (indicators, optimize, trading_rules). For example, the current rule for trying to enter the market is when a trend is detected (r2 and Mann-Kendall). We could create a new module that tries to enter the market using a mean-reversion strategy like when the market is 2 standard deviations from the average price of the last 100 days (in the trading_rules package).

To find more details about this project, scroll down

The project structure : 

```
├── EURUSD.csv                                  <- Data
├── LICENSE.txt                                 <- License
├── README.md                                   <- ReadMe doc
├── __init__.py                 
├── charting.py                                 <- Charting modules
├── date_manip.py                               <- Module to manipulate date
├── entry                                       <- Package that tries to enter the market (with different modules)
│   ├── __init__.py
│   └── entry_fibo.py                           <- Module that tries to enter the market using the Fibonacci technique
├── exit                                        <- Package that tries to exit the market (with different modules)
│   ├── __init__.py
│   └── exit_fibo.py                            <- Module that tries to enter the market using the Fibonacci technique
├── indicator.py                                <- Return the values of our indicators of our choice
├── indicators                                  <- Package that evaluates the indicators
│   ├── __init__.py
│   └── regression                              
│       ├── __init__.py
│       ├── linear_regression.py                <- Module that evaluates the slope and r_square of a serie
│       └── mann_kendall.py                     <- Module that assess the Mann-Kendall test
├── init_operations.py                          <- Module that resets the necessary values
├── initialize.py                               <- Module that declares hyperparamaters and parameters to optimize
├── main.py                                     <- Main module that executes the program
├── manip_data.py                               <- Helper module to manipulate csv and pandas Dataframe
├── math_op.py                                  <- Module support for mathematical operations
├── optimize                                    <- Package with optimization techniques
│   ├── __init__.py
│   └── genetic_algorithm.py                    <- Module that uses a genetic algorithm to optimize
├── optimize_.py                                <- Module that runs the optimization process if desired                
├── pnl.py                                      <- Module to assess the trading strategy performance
└── trading_rules                               <- Package with possible trading rules
    ├── __init__.py
    └── r_square_tr.py                          <- Module that detects buy and sell signals with r_square and Mann Kendall test

```

To see the list of hyperparameters and parameters to optimize, go to this [file](https://github.com/philos123/PyBacktesting/blob/master/initialize.py)

Each .py file has its docstring, so make sure to check it out to understand the details. 

To find out more about [me](https://github.com/philos123)

For questions or comments, please feel free to reach out on [LinkedIn](https://www.linkedin.com/in/philippe-ostiguy/?locale=en_US)

## Part 1 - DEFINING

### ---- Defining the problem ----

The goal of this project is to model the Elliott Wave Theory to forecast the financial markets. Once we have the model and know the parameters, we optimize it using a machine learning technique called genetic algorithm and test in a different period (Walk forward optimization). The fitness function used for optimization and testing is the Sharpe ratio. 

There is no real technique at the moment to model the Elliott Wave Theory as it is difficult to model and the modeling is highly subjective. To understand the concept of Elliott Wave Theory, refer to this [post](https://www.investopedia.com/articles/technical/111401.asp).

Since the optimization space of a trading strategy can be complex, genetic algorithms are an efficient machine learning technique to find a good approximation of the optimal solution. It mimics the biological process of evolution. 

![](https://github.com/philos123/PyBacktesting/blob/master/images/genetic.jpg)

## Part 2 - DISCOVER

### ---- Loading the data ----

The experiment was carried out on the EUR/USD currency pair on an hourly basis. The period was from 2015/10 to 2020/04 (including 2 training and 2 testing periods). The training periods were 18 months each (from 2015-10-15 to 2017-04-15 and from 2018-01-15 to 2019-07-15) and the testing periods were 9 months each (from 2017-04-15 to 2018-01-15 and from 2019-07-15 to 2020-04-15). 

The data source for this experiment was [Dukascopy](https://www.dukascopy.com/swiss/english/marketwatch/historical/) as it required a lot of data. The program read the data in a csv format. If you want to do an experiment on a different asset and/or timeframe, make sure to load the data in the folder of your choice and change the path with the variable `self.directory` in [initialize.py](https://github.com/philos123/PyBacktesting/blob/master/initialize.py). 

If less data is needed for an experiment or if the experiment is carried on daily basis data, the Alpha Vantage API is a great source to get free and quality data (with certain restrictions, like a maximum API call per minute). [This](https://algotrading101.com/learn/alpha-vantage-guide/) is a great article on the Alpha Vantage API.

```
Parameters
----------
`self.directory` : str
    Where the the data are located for training and testing periods
`self.asset` : str
    Name of the file where we get the data
`self.is_fx` : bool
    Tell if `self.asset` is forex (the data don't have the same format for forex and stocks because they are
    from different providers).
`self.dir_output` : str
    Where we store the results
`self.name_out` : str
    Name of the results file name (csv)
`self.start_date` : datetime object
    Beginning date of training and testing period. The variable is already transformed from a str to a 
    Datetime object
`self.end_date` : datetime object
    Ending date of training and testing period. The variable is already transformed from a str to a 
    Datetime object

self.directory = '/Users/philippeostiguy/Desktop/Trading/Programmation_python/Trading/'
self.dir_output = '/Users/philippeostiguy/Desktop/Trading/Programmation_python/Trading/results/'
self.name_out = 'results'
self.is_fx = True
self.asset = "EURUSD"
self.start_date = datetime.strptime('2015-10-15', "%Y-%m-%d")
self.end_date = datetime.strptime('2016-02-18', "%Y-%m-%d")
```

We can examine our data : 

```
series_.head()
```
| #    | Date                | Open    | High    | Low     | Adj Close |
|------|---------------------|---------|---------|---------|-----------|
| 96   | 2015-10-15 00:00:00 | 1.14809 | 1.14859 | 1.14785 | 1.14801   |
| 97   | 2015-10-15 01:00:00 | 1.14802 | 1.14876 | 1.14788 | 1.14828   |
| 98   | 2015-10-15 02:00:00 | 1.14831 | 1.14950 | 1.14768 | 1.14803   |
| 99   | 2015-10-15 03:00:00 | 1.14802 | 1.14826 | 1.14254 | 1.14375   |
| 100  | 2015-10-15 04:00:00 | 1.14372 | 1.14596 | 1.14335 | 1.14417   |

And see the lenght, value types and if there are empty values (none) :

```
series_.info()
```

| # | Column    | Non-Null Count | Dtype          |
|---|-----------|----------------|----------------|
| 0 | Date      | 28176 non-null | datetime64[ns] |
| 1 | Open      | 28176 non-null | float64        |
| 2 | High      | 28176 non-null | float64        |
| 3 | Low       | 28176 non-null | float64        |
| 4 | Adj Close | 28176 non-null | float64        |


### ---- Cleaning the data ----

In [manip_data.py](https://github.com/philos123/PyBacktesting/blob/master/manip_data.py), we drop the nan value, if any (none) and remove the data when the market is closed with `series_.drop_duplicates(keep=False,subset=list(dup_col.keys()))`

```
series_ = series_.dropna() #drop nan values
if dup_col != None:
    #If all values in column self.dup_col are the same, we erase them
    series_ = series_.drop_duplicates(keep=False,subset=list(dup_col.keys()))
series_=series_.reset_index(drop=True)
```

It removed 172 data.

| # | Column    | Non-Null Count | Dtype          |
|---|-----------|----------------|----------------|
| 0 | Date      | 28024 non-null | datetime64[ns] |
| 1 | Open      | 28024 non-null | float64        |
| 2 | High      | 28024 non-null | float64        |
| 3 | Low       | 28024 non-null | float64        |
| 4 | Adj Close | 28024 non-null | float64        |


### ---- Exploring the data (EDA) ----
The period was from 2015/10 to 2020/04 (including 2 training and 2 testing periods). The training periods were 18 months each (from 2015-10-15 to 2017-04-15 and from 2018-01-15 to 2019-07-15) and the testing periods were 9 months each (from 2017-04-15 to 2018-01-15 and from 2019-07-15 to 2020-04-15). We see the split on chart below.

```
x = np.linspace(pd.Timestamp(self.start_date), pd.Timestamp(self.end_date),len(self.series))
y = self.series.loc[:,self.default_data]

segment1 = (x < pd.Timestamp('2017-04-15').value)
segment2 = (x >= pd.Timestamp('2017-04-15').value) & (x < pd.Timestamp('2018-01-15').value)
segment3 = (x >= pd.Timestamp('2018-01-15').value) & (x < pd.Timestamp('2019-07-15').value)
segment4 = (x >= pd.Timestamp('2019-07-15').value)

x = pd.to_datetime(x)

plt.plot(x[segment1], y[segment1], '-b', lw=1)
plt.plot(x[segment2], y[segment2], '-g', lw=1)
plt.plot(x[segment3], y[segment3], '-b', lw=1)
plt.plot(x[segment4], y[segment4], '-g', lw=1)

plt.show()
```

The blue represents the 2 training periods and the green represents the 2 testing periods

![](https://github.com/philos123/PyBacktesting/blob/master/images/period_split.png)

If someone would like to do time series analysis like ARIMA (not the case here), we would have to check if the serie is stationary. The [Augmented Dickey–Fuller test](https://en.wikipedia.org/wiki/Augmented_Dickey%E2%80%93Fuller_test) does that.

```
from statsmodels.tsa.stattools import adfuller

series_diff = self.series.copy()
if adfuller(series_diff[self.default_data])[1] > self.p_value:
    raise Exception("The series is not stationary")

```

If the serie is not stationary and it's only a matter of "trend", first differencing is in general fine to make a financial time series stationary. It there is seasonality, other manipulations are required

```
import matplotlib.pyplot as plt

series_diff = self.series.copy()
series_diff.drop([self.date_name, self.date_ordinal_name], axis=1, inplace=True)
series_diff = series_diff.diff(periods=self.period)  # differentiate with previous row
series_diff.loc[:(self.period - 1), :] = 0 #Make first row equal to 0
series_diff.insert(0, self.date_name, self.series[self.date_name]) #re-insert the period columns

plt.plot(self.series_test[self.date_name], self.series_test[self.default_data])
plt.show()
```

![](https://github.com/philos123/PyBacktesting/blob/master/images/stationary_series.png)

### ---- Establishing a baseline ----

To make it simple and as a first version, this strategy is meant to try to enter the market when a trend is found. Note that we might be violating the assumption that there is no autocorrelation and that the error terms should follow a normal distribution, but for for the sake of simplicity, we'll assume the absence of serial correlation and that the error terms follows a normal distribution. Also, the statistical tests are used to determine if there is a trend, not to forecast the financial market. A way around this would be to make the serie stationary.

First using the Mann-Kendall test (non-parametric methods), we check if there is a trend in the market. It's better than linear regression as it does not require the data to be normally distributed or linear. In the program, it returns a 1 when there is a upward trend, -1 when there is a downward trend and 0 when there is no trend. More explanations and details about the code [here](https://github.com/philos123/PyBacktesting/blob/master/indicators/regression/mann_kendall.py)

Then using the coefficient of determination (R^2), we assess the strenght of the trend. By default, the thresold value `self.r_square_level` in `initialize.py` to say that the trend is significant is 0.7.  More explanations and details about the code [here](https://github.com/philos123/PyBacktesting/blob/master/indicators/regression/linear_regression.py)

There is an example below with dots on chart when the r^2 is above 0.7 and Mann-Kendall is -1 or 1

![](https://github.com/philos123/PyBacktesting/blob/master/images/Trading_rules.png)

Whenever we have a trend confirmation, the program tries to enter the market using the Elliott Wave Theory in the module [entry_fibo](https://github.com/philos123/PyBacktesting/blob/master/entry/entry_fibo.py). First, the method finds local minimum and maximum in the current trend with function `self.local_extremum_()`. It checks if the values for a number of points on each side (`window`) are greater or lesser and then determine the local extremum. Assessing a local extremum on a financial time series can be tricky, but this method gives satisfactory results.

```
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

cls.series=cls.series.loc[start_point:end_point,cls.default_col]
cls.series=pd.DataFrame({cls.default_col: cls.series})

cls.series[min_] = cls.series.iloc[argrelextrema(cls.series.values, np.less_equal,
                                                  order=window)[0]][cls.default_col]
cls.series[max_] = cls.series.iloc[argrelextrema(cls.series.values, np.greater_equal,
                                                  order=window)[0]][cls.default_col]
cls.series[index_] = cls.series.index
plt.scatter(cls.series.index, cls.series[min_], c='r')
plt.scatter(cls.series.index, cls.series[max_], c='g')

plt.plot(cls.series.index, cls.series[cls.default_col])
plt.ion()
plt.show()
        
```
![](https://github.com/philos123/PyBacktesting/blob/master/images/Local_extremum.png)

Then using `self.largest_extension()`, it sets the largest setback, which is the difference between a local maximum and the previous local minimum for a downward trend and the difference between the local maximum and and the next local minimum for an upward trend. In the above example, the largest setback in the downward trend would be the difference between the value at the index 148 (1.11292) minus the index at the index 139 (1.10818) for a result of 0.0047. This value play a key role for the entry and the exit level.

When the largest setback is set, the program will try to enter the market with the function `self.try_entry()` in the module [entry_fibo](https://github.com/philos123/PyBacktesting/blob/master/entry/entry_fibo.py)

Then if the system is able to enter in the market, it will exit wheter a stop loss is triggered or the profit level is reached using again the logic with the largest setback (and using the Elliott Wave Theory). Please refer to this [module](https://github.com/philos123/PyBacktesting/blob/master/exit/exit_fibo.py) for more information. 

Below is an example of 2 entries (buy in green) and 2 exits (sell in red). The first one has a profit and the other one has a lost :

![](https://github.com/philos123/PyBacktesting/blob/master/images/Entry_exit.png)

There a different values that can be used for the Elliott Wave Theory strategy. Again, please refer to the module [initialize.py](https://github.com/philos123/PyBacktesting/blob/master/initialize.py) to see all the parameters that can be optimized. We used the default value in this module to evaluate the preformance of the trading strategy. 

The metric used to evalute the preformance of the trading strategy is the Sharpe ratio. It's the most common metric used to evaluate a trading strategy. There are other useful metrics to assess the performance of a trading strategy [here](https://github.com/philos123/PyBacktesting/blob/master/pnl.py)

![](https://github.com/philos123/PyBacktesting/blob/master/images/Sharep_ratio.gif)

S<sub>a</sub> :	Sharpe ratio <br>
E : expected value <br>
R<sub>a</sub> :	asset return <br>
R<sub>b</sub> :	risk free return <br>
σ<sub>a</sub> : standard deviation of the asset excess return <br>

Below we can see the result for the 4 different periods before optimization.

| Date range from       | 2015-10-15 to 2017-04-15 |
|-----------------------|--------------------------|
| Annualized return     | -0.028538168293147037    |
| Annualized volatility | 0.001714442062259805     |
| Sharpe ratio          | -16.645746695884778      |
| Maximum drawdown      | -0.00586379729741346     |
| % win                 | 0.13636363636363635      |
| nb_trade              | 22                       |

| Date range from       | 2017-04-15 to 2018-01-15 |
|-----------------------|--------------------------|
| Annualized return     | -0.016042731033677482    |
| Annualized volatility | 0.0029188486883811172    |
| Sharpe ratio          | -5.496253059481227       |
| Maximum drawdown      | -0.0031105801006658536   |
| % win                 | 0.1                      |
| nb_trade              | 10                       |

| Date range from       | 2018-01-15 to 2019-07-15 |
|-----------------------|--------------------------|
| Annualized return     | -0.02083109080647605     |
| Annualized volatility | 0.0021923888737862       |
| Sharpe ratio          | -9.501549225845725       |
| Maximum drawdown      | -0.0042445599845946265   |
| % win                 | 0.20689655172413793      |
| nb_trade              | 29                       |


| Date range from       | 2019-07-15 to 2020-04-15 |
|-----------------------|--------------------------|
| Annualized return     | 0.009637932127751991     |
| Annualized volatility | 0.004822189306914451     |
| Sharpe ratio          | 1.9986631619651127       |
| Maximum drawdown      | -0.0047235958781114      |
| % win                 | 0.35714285714285715      |
| nb_trade              | 14                       |


The only period where the strategy performed well was from 2019-07-15 to 2020-04-15 with a Sharpe ratio of 1.998.

## Part 3 - DEVELOPING

### ---- Creating models ----

There are several ways to optimize a trading strategy, more on that [here](https://miltonfmr.com/how-to-develop-test-and-optimize-a-trading-strategy-complete-guide/). One would be a brute-force algorithm which would test all the possible candidates. The main disadvantage is when there are several candidates, it requires a lot of memory and processing time.

One good solution is the genetic algorithm which is a random-based classical evolutionary algorithm based on Charles Darwin's theory of natural evolution. The process is simple : (code in module [genetic_algorithm.py](https://github.com/philos123/PyBacktesting/blob/master/optimize/genetic_algorithm.py))

#### 1- Generate the initial population
A population is composed of chromosomes or indidivuals (each individual is a solution to the problem we want to solve) and each chromosome is characterized by a set of parameters we want to optimize known as genes. In general, each gene is represented by a binary value. In our case, each gene is a paramater that we want to optimize and can take the possible value that we define in `initialize.py`.

![](https://github.com/philos123/PyBacktesting/blob/master/images/Population.png)

In general, we want the size of the population to be 1.5 to 2 times the number of genes. In our case, we have 16 parameters to optimize and the size of the population is 25 chromosomes.

#### 2- Compute fitness
We then evaluate the performance of each chromosome (individual) using the Sharpe ratio. It gives a score to each individual.

To be consider for the next generation, each chromosome (individual) must generate at least 10 trades during the training period, otherwise it's rejected. In such case, a new chromosome is generated.

#### 3- Selection
We select the best candidates so that they can pass their genes to the next generations (creating children). Two pairs of indidivuals (parents) are selected based on their Sharpe ratio value (fitness score). Individuals with higher Sharpe ratio have more chance to be selected for the next generations. We use the roulette wheel selection for selecting potential indivuals for the next generation. This method gives a probability of choosing an individual proportionally to his fitness value. 

![](https://github.com/philos123/PyBacktesting/blob/master/images/Selection.png)

#### 4- Genetic operators
We then create the new population using genetic operators. The first one is to copy the chromosomes to the next generation with a probability of 30%. 

![](https://github.com/philos123/PyBacktesting/blob/master/images/copy_generation_.png)

The second genetic operator is the crossover. It is the most significant genetic operator as it creates new offspring by exchanging genes among the best parents (previous generation). It has a 65% probability of happening.

![](https://github.com/philos123/PyBacktesting/blob/master/images/Crossover_.png)

The last one is mutation which flips (mutates) a gene from the best parents. It's an operator which prevent to get stuck too early in a local extrema. The probability is not too high to prevent the risk that an individual was close to a solution (from previous generation). It has a 5% probability of happening.

![](https://github.com/philos123/PyBacktesting/blob/master/images/mutation_.png)

### 5- Repeat
We repeat step 2 to 4 for 25 generations. It's important to set a proper size of generations as a too small generation won't give a good coverage of the search space and too large is time-consuming. 

Another possibility would be to stop the cycle when the sharpe ratio is equal to or greater than 3 (or when it reaches a satisfactory fitness value). In this experiment, the algorithm runs for 25 generations.

### ---- Testing models ----

The experiment was carried out on the EUR/USD currency pair on an hourly basis. The period was from 2015/10 to 2020/04 (including 2 training and 2 testing periods). The training periods were each 18 months each (from 2015-10-15 to 2017-04-15 and from 2018-01-15 to 2019-07-15) and the testing periods were 9 months each (from 2017-04-15 to 2018-01-15 and from 2019-07-15 to 2020-04-15). 

The Sharpe ratio was above 3 for each training period (which is excellent). The results were mixed for the training periods. The Sharpe ratio was 1.63 for the first training period (which is really good) and -13.99 for the second period with 0 winning trades (which is really bad).


#### Training period no 1
| Date range from       | 2015-10-15 to 2017-04-15 |
|-----------------------|--------------------------|
| Annualized return     | 0.03579816749483067      |
| Annualized volatility | 0.00996732375915114      |
| Sharpe ratio          | 3.591552593238869        |
| Maximum drawdown      | -0.00997144631486068     |
| % win                 | 0.36363636363636365      |
| nb_trade              | 22                       |


#### Testing period no 1
| Date range from       | 2017-04-15 to 2018-01-15 |
|-----------------------|--------------------------|
| Annualized return     | 0.014095773085682        |
| Annualized volatility | 0.008626558234907        |
| Sharpe ratio          | 1.63399732568252         |
| Maximum drawdown      | -0.005521301258917       |
| % win                 | 0.363636363636364        |
| nb_trade              | 11                       |


#### Training period no 2
| Date range from       | 2018-01-15 to 2019-07-15 |
|-----------------------|--------------------------|
| Annualized return     | 0.009447731588671        |
| Annualized volatility | 0.00287683168216         |
| Sharpe ratio          | 3.28407520233458         |
| Maximum drawdown      | -0.000809793667447       |
| % win                 | 0.074074074074074        |
| nb_trade              | 27                       |


#### Testing period no 2
| Date range from       | 2019-07-15 to 2020-04-15 |
|-----------------------|--------------------------|
| Annualized return     | -0.006083679046796       |
| Annualized volatility | 0.000434670065322        |
| Sharpe ratio          | -13.9960846907784        |
| Maximum drawdown      | -0.001343642756988       |
| % win                 | 0                        |
| nb_trade              | 10                       |



### ---- Summarizing ----

One of the issue with the model during the testing periods is that it generated few trades (11 for the first testing period and 10 for second testing period). This may be due to an over optimized model which caused overfitting. We could also test the same model on different assets and different timeframes.

Also, this a a basic model of the Elliott Wave Theory. We could also enter the market with Fibonacci retracements and exit the market using Fibonacci extensions.
