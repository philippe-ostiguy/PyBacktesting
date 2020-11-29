![](https://github.com/philos123/PyBacktesting/blob/master/images/artificial-intelligence.png)

# [WIP] Using the Elliott Wave Theory to forecast the financial markets and optimize with a genetic algorithm


Hi! 

My name is Philippe. The goal of this project is to model the Elliott Wave Theory to forecast the financial markets. Once we have the model and know the parameters, we optimize it using a machine learning technique called genetic algorithm and test in a different period (Walk forward optimization). The fitness function we're using for optimization and testing is the Sharpe ratio. 

The experiment was carried out on the EUR/USD currency pair on hourly basis data. The time period was from 2015/10 to 2020/04 (including 2 training and 2 testing periods). The training periods were each 18 months each (2015-10-15 to 2017-04-15 and 2018-01-15 to 2019-07-15) and the testing periods were 9 months each  (2017-04-15 to 2018-01-15 and 2019-07-15 to 2020-04-15). 

For each training period, the Sharpe ratio was above 3, which is excellent. For the testing period, the results were mixed. For the first testing period, the Sharpe ratio was 1.63, which is really good. For the second testing period, the Sharpe ratio -13.99 with 0 winning trades.

One of the issue with the model during the testing periods is that generated few trades (11 for the first testing period and 10 for second testing period). This may be due to the fact that the model is highly optimized (overfit). We could also test the same model on different assets and different timeframes.

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

### ---- 1 Define the problem ----

The goal of this project is to model the Elliott Wave Theory to forecast the financial markets. Once we have the model and know the parameters, we optimize it using a machine learning technique called genetic algorithm and test in a different period (Walk forward optimization). The fitness function we're using for optimization and testing is the Sharpe ratio. 

There is no real technique at the moment to model the Elliott Wave Theory as it is difficult to model and the modeling is highly subjective. To understand the concept of Elliott Wave Theory, refer to this [post](https://www.investopedia.com/articles/technical/111401.asp).

Since the optimization space of a trading strategy can be complex, genetic algorithms are efficient are efficient machine learning technique for this kind of optimization. They mimic the biological process of evolution. 

![](https://github.com/philos123/PyBacktesting/blob/master/images/genetic.jpg)

## Part 2 - DISCOVER

### ---- 2 Load the data ----

The experiment was carried out on the EUR/USD currency pair on hourly basis data. The time period was from 2015/10 to 2020/04 (including 2 training and 2 testing periods). The training periods were each 18 months each (2015-10-15 to 2017-04-15 and 2018-01-15 to 2019-07-15) and the testing periods were 9 months each  (2017-04-15 to 2018-01-15 and 2019-07-15 to 2020-04-15). 

The data source for this experiment was [Dukascopy](https://www.dukascopy.com/swiss/english/marketwatch/historical/) as a lot of data was needed on an hourly basis. The program read the data in a csv format. If you want to do an experiment on a different asset and/or timeframe, make sure to load the data in the folder of your choice and change the path with the variable `self.directory` in [initialize.py](https://github.com/philos123/PyBacktesting/blob/master/initialize.py). 

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


CHECK FOR NAN, DUPLICATES, SPLIT THE TEST/TRAINING DATA

<class 'pandas.core.frame.DataFrame'>
Int64Index: 28176 entries, 96 to 28271
Data columns (total 5 columns):
 #   Column     Non-Null Count  Dtype         
---  ------     --------------  -----         
 0   Date       28176 non-null  datetime64[ns]
 1   Open       28176 non-null  float64       
 2   High       28176 non-null  float64       
 3   Low        28176 non-null  float64       
 4   Adj Close  28176 non-null  float64       
dtypes: datetime64[ns](1), float64(4)
memory usage: 1.3 MB


If less data is needed for an experiment or the experiment is carried on daily basis data, the Alpha Vantage API is a great source to get free and quality data (with certain restrictions, like a maximum API call per minute). [This](https://algotrading101.com/learn/alpha-vantage-guide/) is a great article on the Alpha Vantage API.



AT THE END
What we would like to improve : - test on other market, using retracements
