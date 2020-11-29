#!/usr/local/bin/env python3.7
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
#  The MIT License (MIT)
#  Copyright (c) 2020 Philippe Ostiguy
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
###############################################################################

"""Module to declare hyperparamaters and parameters to to optimize"""

from dateutil.relativedelta import relativedelta
from date_manip import DateManip as dm
from manip_data import ManipData as md
import pandas as pd
from datetime import datetime
import random

class Initialize():
    """Module to initialize the values.

    The __init__ constructor inialize the hyperparameters and others parameters that won't be optimized parameters. The
    optimized parameters are in __call__ function.
    """

    def __init__(self):
        """
        Initialize the hyperparameters and other parameters that won't be optimized.

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
        `self.is_walkfoward` : bool
            Tells if we do an optimization (training and testing) or only a test on the whole period
        `self.training_name` : str
            If `self.is_foward` is `True`, this is the string added to the result files name for training data
        `self.test_name_` : str
             If `self.is_foward` is `True`, this is the string added to the result files name for test data
         `self.training_` : int
            Lenght in months of training period
        `self.test_` : int
            Lenght in months of testing period (put 9)
        `self.name_col` : dict
            Says which data we need in our testing
        `self.dup_col` :  dict
            Columns we use to check if the market is closed. Ex: If OHLC are all the same, then the market is closed.
        `self.window` : int
            Number of data (points) we check before and after a data to check if it is a local min and max
        `self.pnl_dict` : dict
            Contains the metrics to calculate the strategy performance. The metrics are (keys) :
             `self.range_date_` : str
                Testing date range
             `self.sharpe_ratio_` : float
                Sharpe ratio. Did not substract the risk-free rate, only return divided by volality. Reason is that on
                Forex or small timeframe, return is low and we can leverage return (or totally
                 distort it) with margin trading
            `self.ann_return_` = float
                Annualized return
            `self.ann_vol_` = float
                Annualized volatility
            `self.pour_win_` = float
                Ratio of winning trades
            `self.max_draw_` = float
                Maximum drawdown
            `self.nb_trades_` = int
                Number of trades during the period
        `self.entry_row` : int
            Entry row number for a trade
        `self.entry_level` : float
            Entry level for a trade
        `self.exit_row` = int
            Exit row number for a trade
        `self.exit_level` : int
            Exit level for a trade
        `self.trade_return` : float
            Trade return for a trade
        `self.is_detrend` : bool
            Default is `False`. Possible to set to yes or no. It tells if we want to de-trend the current series.
            If we set it to `True`, make sure to make changes in `Indicator.py` to use `self.series_test` instead of
            `self.series` and in `init_operations.py` remove the commented code in function `init_series()` for
            `self.series_test`.
        `self.p_value` : float
            Significance level to test for non stationarity with Augmented Dickey-Fuller. Default is 0.01
        `self.period` = int
            Order of differencing of the time series. By default 1 (first order differencing)

        """

        self.directory = '/Users/philippeostiguy/Desktop/Trading/Programmation_python/genetic_programming/Trading/'
        self.dir_output = '/Users/philippeostiguy/Desktop/Trading/' \
                          'Programmation_python/genetic_programming/Trading/results/'
        self.name_out = 'results'
        self.is_fx = True
        self.asset = "EURUSD"
        self.start_date = datetime.strptime('2015-10-15', "%Y-%m-%d")
        self.end_date = datetime.strptime('2020-04-15', "%Y-%m-%d")

        self.is_walkfoward = False
        self.training_name_ = '_training'
        self.test_name_ =  '_test'
        self.training_ = 18 #Lenght in months of training period (put 18)
        self.test_ = 9 #Lenght in months of testing period (put 9)
        self.dict_name_ = {self.training_name_:self.training_,self.test_name_:self.test_}
        self.train_param= [] #Optimized training parameters used for the test period

        # Decide which data type we need in our testing
        self.date_name = 'Date'
        self.open_name = 'Open'
        self.high_name = 'High'
        self.low_name = 'Low'
        self.close_name = 'Close'
        self.adj_close_name = 'Adj Close'
        self.name_col = {
            self.date_name: [],
            self.open_name: [],
            self.high_name: [],
            self.low_name: [],
            self.adj_close_name: []
        }

        #Columns we use to check if there are duplicate values
        self.dup_col = {
            self.open_name: [],
            self.high_name: [],
            self.low_name: [],
            self.adj_close_name: []
        }

        self.window = 6

        # Metrics used to calculate the strategy performance
        self.pnl_dict = {}
        self.range_date_ = 'Date range from '
        self.sharpe_ratio_ = 'Sharpe ratio'  # Did not substract the risk-free rate, only return divided by vol
        self.ann_return_ = 'Annualized return'
        self.ann_vol_ = 'Annualized volatility'
        self.pour_win_ = '% win'  # pourcentage of winning trades
        self.max_draw_ = 'Maximum drawdown'
        self.nb_trades_ = 'nb_trade'

        # Values used to calculate each trade performance
        self.entry_row = 'Entry_row'
        self.entry_level = 'Entry_level'
        self.exit_row = 'Exit_row'
        self.exit_level = 'Exit_level'
        self.trade_return = 'trade_return'

        self.default_data = self.adj_close_name  # Value we use by default for chart, extremum, etc.


        self.is_detrend = False  # Possible to set to yes r no
        self.p_value = .01  # significance level to test for non stationarity with Augmented Dickey-Fuller
        self.period = 1

        #No need to change them. These are variable that we don't need to change
        self.name = pd.DataFrame(self.name_col)
        self.date_ordinal_name = 'Ordinal Date'
        self.marker_ = 'marker_name'
        self.color_mark = 'color_mark'
        self.marker_signal = 'marker_signal'
        self.end_format_ = "%Y-%m-%d" #format when printing date range in csv files with results

    def __call__(self):

        """ Set values for optimization if we decide to optimize

        It is the values that are initialized  and used through the system

        Parameters
        ----------
        `self.nb_data` : int
            Number of data needed to calculate the indicators. Default is 100 but can be 100, 200, 300.
        `self.r_square_level` : float
            R square level required to trigger a signal. Can be .6 , .7, .8 and .9.
        `self.min_data` : int
            Number of minimum required between each signal in the same direction. 100,200 or 300

        Entry
        `self.enter_dict` : dict
            Dictionary containing the possible entry types
        `self.enter_ext_name` : str
            Name for entering in the market with Fibonnacci extensions. We are using the largest extension of
            the previous trend as a reference. Largest extension is in fact the largest setback in the current trend.
            Ex : largest extension from previous trend is 1, the system enters in the market when it is `self.enter_ext`
            this size (1 by default). So, when this value is reached, it takes the profit.
            `self.enter_ext` : float
                This is the % of largest extension at which the system enters the market. Can be .882 or .764 or 1
        `self.enter_time` : str
            Entering the market only if the current setback is a minimum percentage of largest setback
            from current trend in term of time.
            `self.enter_bool` : bool
                Telling if we use this technic or not. Can be set to `True` or `False`
            `self.time_ext` : float
                Proportion in term in time needed that the current setback most do compared to the largest extension
                in therm of time in the current trend to enter the market. It can be .5, .618 .884,1
        Exit
        Extension
        `self.exit_dict` : dict
            Dictionary containing the possible ways to exit the market
        `self.exit_ext_name` : str
            name of the dictionary key to try to exit the market with Fibonnacci extensions
        `self.exit_ext` : bool
            tells the system if tries to exit (or not) the market using the largest extension as a reference.
            It has to be `True` at the moment because it is the only way to exit the market.
            Ex : largest extension from preivous trend is 1, the system takes profit when it is
            `self.profit_ext` of this size (2.618 by default). So, when this value is reached, it takes the profit.
        `self.profit_ext` : float
             % of the largest extension from previous trend that the system uses to exit the market to take profit
             Default value is 2.618. Possible values are 1.618, 2 , 2.618, 3.382, 4.236.
        `self.stop_ext` : float
             % of the largest extension from previous trend that the system uses as a stop loss.
             Default value is 1.618. Possible values are 1, 1.382, 1.618, 2.

        Stop trying to enter
            These params are conditions to stop trying to enter the market if the current price reach a % of the
            largest extension `self.fst_cdt_ext` goes in the other direction and retraces the last top or bottom
            with proportion `self.sec_cdt_ext`, the system stop trying to enter in the market.
        `self.bol_st_ext` : bool
            Tells the system if it has to stop trying to enter the market using Fibonacci extension techniques.
            Can be optimized to `True` or `False`
        `self.fst_cdt_ext` : float
            % of the largest extension that if the market reaches, the system stops trying to enter the market.
            Possible values are .618, .764 or .882
        `self.sec_cdt_ext` : float
             if the market triggers the first condition, then if it reaches this level in the opposite direction, the
            # system stops trying to enter in the market. Can be set to .618, .764, 1 or 1.382

        Stop tightening
        General
        `self.stop_tight_dict` : dictionary
            contains the different possibilities to tighten the stop

        `self.default_data_` : bool
            default data used to determine if the stop loss level must be tightened. It is `True`, then
            `self.adj_close_name` is used. Otherwise, `self.low_name` with `self.high_name` (depends if it is
            a buy or sell signal).

        Stop tightening (technique no 1)
        `self.stop_tight_ret` : str
             Tightening the stop using Fibonacci retracement condition (contains the condition).
        `self.stop_ret_level` : float
            Level at which the system tight the stop when it reaches this retracement in the opposite direction.
            Ex: Buy signal then, market reaches `self.stop_ret_level` (1 by default) in the other direction.
            The system will tighen the stop to the lowest (or highest) point. Default value is 1.
             Possible values are 618, .882, 1, 1.618 or 2.
        `self.is_true` : bool
            Tells the system if it has to use this particular technique to tighten the stop or not. Possible values are
            `True` or `False`

        Stop tightening (technique no 2)
        `self.stop_tight_pour` : str
            tightening the stop when the market reaches a certain percentage of the target
        `self.is_true` : bool
            Tells the system if it has to use this particular technique to tighten the stop or not. Possible values are
            `True` or `False`
        `self.tight_value` : float
            When the market reaches this percentage of the target, we tighten the stop. Possible values are
            .5,.618,.764.
        `self.pour_tight` : float
            Percentage between the current market value and entry value that the current new stop is. Possible values
            are .5 or .618.

        """

        self.nb_data = 100
        self.r_square_level =  self.return_value([.6,.7,.8,.9],.7)
        self.min_data = self.return_value([100,200,300],100)

        #ENTRY
        #-----
        # All the possible entry types that the system can do (extension, retracement)
        self.enter_bool = 'enter_bool' #same key name for all the exit strategy (located in different dictionary)
        self.enter_ext_name = 'enter_ext_name'
        self.enter_ext = 'enter_ext' #Entering the market with largest extension from setback in current trend
        self.stop_ext = 'stop_ext'
        self.enter_time = 'enter_time'
        self.time_ext = 'time_ext'

        self.enter_dict = {self.enter_ext_name :
                              {self.enter_bool : True, #At the moment, it has to be `True`, no other method to enter
                               self.enter_ext: self.return_value([.764,.882,1],1)

                               },
                           self.enter_time:
                               {self.enter_bool : self.return_value([False,True],True),
                                self.time_ext : self.return_value([.5,.618,.882,1],.618)
                                }
                          }

        #STOP TRY TO ENTER
        #--------------
        #These params are conditions to stop trying to enter the market if the current
        # price reach a % of the largest extension
        self.bol_st_ext = self.return_value([True,False],True)
        self.fst_cdt_ext = self.return_value([.618,.764,.882],.764)
        self.sec_cdt_ext = self.return_value([.618,.764,1,1.382],1)

        #STOP TIGHTENING
        #---------------
        self.stop_tight_ret =  'stop_tight_ret'
        self.stop_tight_pour = 'stop_tight_pourentage'
        self.is_true = 'is_true'
        self.default_data_ = 'default_data_' #adjusted closed
        self.stop_ret_level = 'stop_ret_level'
        self.tight_value = 'tight_value'
        self.pour_tight = 'pour_tight'
        self.stop_tight_dict = {self.stop_tight_ret : #Stop tightening technique no 1.
                                    {self.is_true : self.return_value([True,False],True),
                                     self.default_data_ : True,
                                     self.stop_ret_level : self.return_value([.618,.882,1,1.618,2],1)
                                     },

                                self.stop_tight_pour :  #Stop tightening no 2.
                                    {self.is_true : self.return_value([True,False],True), #True or False
                                     self.tight_value : self.return_value([.5,.618,.764],.5),
                                     self.pour_tight : self.return_value([.5,.618],.5)
                                    }
                                }

        # EXIT
        # -----
        # All the possible ways that the system can exit the market (extension, retracement)
        self.exit_name = 'exit_name' #same key name for all the exit strategy (located in different dictionary)
        self.exit_ext_bool = 'exit_ext_bool'
        self.profit_ext = 'profit_ext'
        self.stop_ext = 'stop_ext'
        self.exit_dict = {self.exit_name :
                              {self.exit_ext_bool : True, #It has to be `True` has it the only way for now to exit the
                                                            #market
                               self.profit_ext :self.return_value([1.618,2,2.618,3.382,4.236],3.382),
                               #also try 2 2.618, 3.382, 4.236
                               self.stop_ext : self.return_value([1,1.382,1.618,2],1.618)   #1,1.382, 1.618, 2
                               }
                          }

    def return_value(self,first_val,sec_val):
        """ Return first value if `True` (we optimize), second if False

        """
        return first_val if self.is_walkfoward else sec_val

    def optimize_param(self):
        """ Tell the parameters we want to optimize.

        Store the paramaters to optimize in a list with the name of the parameter to optimize
        """

        self.op_param = [[self.exit_dict[self.exit_name],'profit_ext'],
                          [self.exit_dict[self.exit_name],'stop_ext'],
                          [self.stop_tight_dict[self.stop_tight_ret],'is_true'],
                          [self.stop_tight_dict[self.stop_tight_ret],'stop_ret_level'],
                          [self.stop_tight_dict[self.stop_tight_pour],'is_true'],
                          [self.stop_tight_dict[self.stop_tight_pour],'tight_value'],
                          [self.stop_tight_dict[self.stop_tight_pour],'pour_tight'],
                          ['bol_st_ext'],
                          ['fst_cdt_ext'],
                          ['sec_cdt_ext'],
                          [self.enter_dict[self.enter_ext_name],'enter_ext'],
                          [self.enter_dict[self.enter_time],'enter_bool'],
                          [self.enter_dict[self.enter_time],'time_ext'],
                          ['r_square_level'],
                          ['min_data']]
