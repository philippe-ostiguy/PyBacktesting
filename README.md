![](https://github.com/philos123/PyBacktesting/blob/master/images/artificial-intelligence.png)

# [WIP] Using the Elliott Wave Theory to forecast the financial markets and optimize with a genetic algorithm


Hi! 

My name is Philippe. The goal of this project is to model the Elliott Wave Theory to forecast the financial markets. Once we have the model and know the parameters, we optimize it using a machine learning technique called genetic algorithm and test in a different period (Walk forward optimization). The fitness function we're using for optimization and testing is the Sharpe ratio. 

The experiment was carried out on the EUR/USD currency pair on hourly basis data. The time period was from 2015/10 to 2020/04 (including 2 training and 2 testing periods). The training periods were each 18 months each (2015-10-15 to 2017-04-15 and 2018-01-15 to 2019-07-15) and the testing periods were 9 months each  (2017-04-15 to 2018-01-15 and 2019-07-15 to 2020-04-15). 

For each training period, the Sharpe ratio was above 3, which is excellent. For the testing period, the results were mixed. For the first testing period, the Sharpe ratio was 1.63, which is really good. For the second testing period, the Sharpe ratio -13.99 with 0 winning trades.

One of the issue with the model during the testing periods is that generated few trades (11 for the first testing period and 10 for second testing period). This may be due to the fact that the model is highly optimized (overfit). We could also test the same model on different assets and different timeframes.

The library is divided so that it is possible to modify the trading strategy by creating modules in the different packages (indicators, optimize, trading_rules). For example, the current rule for trying to enter the market is when a trend is detected (r2 and Mann-Kendall). We could create a new module that tries to enter the market when we are 2 standard deviations from the average price of the last 100 days (in the trading_rules package).

To find more details about this project, scroll down

To see the list of the hyperparameters and parameters to optimize, go to this [file](https://github.com/philos123/PyBacktesting/blob/master/initialize.py)

Each .py file has its docstring, so make sure to check it out to understand the details of the project. 

To find out more about [me](https://github.com/philos123)

For questions or comments, please feel free to reach out on [LinkedIn](https://www.linkedin.com/in/philippe-ostiguy/?locale=en_US)

1- A clear explanation of the problem your're trying to solve and why it's important<br />
2- A summary of your data cleaning and exploration. including visualizations<br />
3- How you created a baseline model<br />
4- Your logic for selecting models to test, tuning models and measuring their efficacy (Share Ratio in this case)<br />
5- The results that you got for each model and making predictions, including vizualisations here<br />
6- Your approach to training the final model and making predictions<br />
7- A summary of the projects, results, findings and area that could be improved or explored in the future<br />


## Part 1 - DEFINE

### ---- 1 Defining the problem ----

The goal of this project is to model the Elliott Wave Theory to forecast the financial markets. Once we have the model and know the parameters, we optimize it using a machine learning technique called genetic algorithm and test in a different period (Walk forward optimization). The fitness function we're using for optimization and testing is the Sharpe ratio. 

There is no real technique at the moment to model the Elliott Wave Theory as it is difficult to model and the modeling is highly subjective. To understand the concept of Elliott Wave Theory, refer to this [post](https://www.investopedia.com/articles/technical/111401.asp).

![](https://github.com/philos123/PyBacktesting/blob/master/images/El_wave.jpg)

Since the optimization space of a trading strategy can be complex, genetic algorithms are efficient are efficient machine learning technique for this kind of optimization. They mimic the biological process of evolution. 

![](https://github.com/philos123/PyBacktesting/blob/master/images/genetic.jpg)

## Part 2 - DISCOVER

### ---- 2 Loading the data ----

The experiment was carried out on the EUR/USD currency pair on hourly basis data. The time period was from 2015/10 to 2020/04 (including 2 training and 2 testing periods). The training periods were each 18 months each (2015-10-15 to 2017-04-15 and 2018-01-15 to 2019-07-15) and the testing periods were 9 months each  (2017-04-15 to 2018-01-15 and 2019-07-15 to 2020-04-15). 

The data source for this experiment was [Dukascopy](https://www.dukascopy.com/swiss/english/marketwatch/historical/) as a lot of data was needed on an hourly basis. The program read the data in a csv format. If you want to do an experiment on a different asset and/or timeframe, make sure to load the data in the folder of your choice and change the path with the variable `self.directory` in [initialize.py](https://github.com/philos123/PyBacktesting/blob/master/initialize.py). 

If less data is needed for an experiment or the experiment is carried on daily basis data, the Alpha Vantage API is a great source to get free and quality data (with certain restrictions, like a maximum API call per minute). [This](https://algotrading101.com/learn/alpha-vantage-guide/) is a great article on the Alpha Vantage API.

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


In [manip_data.py](https://github.com/philos123/PyBacktesting/blob/master/manip_data.py), we drop the nan value, if any (none) and remove the data when the market is closed with `series_.drop_duplicates(keep=False,subset=list(dup_col.keys()))`

```
series_ = series_.dropna() #drop nan values
if dup_col != None:
    #If all values in column self.dup_col are the same, we erase them
    series_ = series_.drop_duplicates(keep=False,subset=list(dup_col.keys()))
series_=series_.reset_index(drop=True)
```

We can see that it removed 172 data.

| # | Column    | Non-Null Count | Dtype          |
|---|-----------|----------------|----------------|
| 0 | Date      | 28024 non-null | datetime64[ns] |
| 1 | Open      | 28024 non-null | float64        |
| 2 | High      | 28024 non-null | float64        |
| 3 | Low       | 28024 non-null | float64        |
| 4 | Adj Close | 28024 non-null | float64        |


The time period was from 2015/10 to 2020/04 (including 2 training and 2 testing periods). The training periods were each 18 months each (2015-10-15 to 2017-04-15 and 2018-01-15 to 2019-07-15) and the testing periods were 9 months each (2017-04-15 to 2018-01-15 and 2019-07-15 to 2020-04-15). We can see the split on chart below.

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

If someone would like to do standard time series analysis like ARIMA (not the case here), we would have to check if the serie is stationary. The [Augmented Dickey–Fuller test](https://en.wikipedia.org/wiki/Augmented_Dickey%E2%80%93Fuller_test) does that

```
from statsmodels.tsa.stattools import adfuller

series_diff = self.series.copy()
if adfuller(series_diff[self.default_data])[1] > self.p_value:
    raise Exception("The series is not stationary")

```

If the serie is not stationary and it's only a matter of "trend", first differencing is in general fine to make a financial time series stationary. It there is seasonality, other manipulations may be required

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

AT THE END
What we would like to improve : - test on other market, using retracements
