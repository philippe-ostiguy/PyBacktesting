!(https://github.com/philos123/PyBacktesting/blob/master/images/artificial-intelligence.png)

# [WIP] Using the Elliott Wave Theory to forecast the financial markets and optimize with a genetic algorithm


Hi! 

My name is Philippe. The goal of this project is to model the Elliott Wave Theory to forecast the financial markets. Once we have the model and know the parameters, we optimize it using a machine learning technique called genetic algorithm and test in a different period (Walk forward optimization). The fitness function we're using for optimization and testing is the Sharpe ratio. 

The experiment was carried out on the EUR/USD currency pair on hourly basis data. The time period was from 2015/10 to 2020/04 (including 2 training and 2 testing periods). The training periods were each 18 months each (2015-10-15 to 2017-04-15 and 2018-01-15 to 2019-07-15) and the testing periods were 9 months each  (2017-04-15 to 2018-01-15 and 2019-07-15 to 2020-04-15). 

For each training period, the Sharpe ratio was above 3, which is excellent. For the testing period, the results were mixed. For the first testing period, the Sharpe ratio was 1.63, which is really good. For the second testing period, the Sharpe ratio -13.99 with 0 winning trades.

One of the issue with the model during the testing periods is that generated few trades (11 for the first testing period and 10 for second testing period). This may be due to the fact that the model is highly optimized (overfit). We could also test the same model on different assets and different timeframes.

To find more details about this project, scroll down

To see the list of the hyperparameters and parameters to optimize, go to this [file](https://github.com/philos123/PyBacktesting/blob/master/initialize.py)

Every .py file has its docstring, so make sure to check it out to understand the details of the program. 

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

We




AT THE END
What we would like to improve : - test on other market, using retracements
