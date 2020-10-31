from dateutil.relativedelta import relativedelta
from date_manip import DateManip as dm
from manip_data import ManipData as md
import pandas as pd

class Initialize():
    """
    Module to initialize the values

    Notes
    -----
    Indicators to test are in the indicator.py file

    To improve the program, the indicators should be initialized in this module (initialize.py)

    In entry_fibo, some improvements could be done... (see notes in module entry_fibo.py)
    """

    def __init__(self):
        # directory where our data are
        self.directory = '/Users/philippeostiguy/Desktop/Trading/Programmation_python/Trading/'

        # Writing data
        self.dir_output = '/Users/philippeostiguy/Desktop/Trading/Programmation_python/Trading/results/'
        self.name_out = 'results'

        #PARAMS TO OPTIMIZE STARTS HERE
        #------------------------------
        # Set asset and date to optimize
        self.date_debut = '2017-03-15'
        self.date_fin = '2017-05-01'
        self.is_fx = True #Tell if it is forex
        self.asset = "EURUSD"

        #Value if we decide to optimize the system
        self.is_walkfoward = True #Says if we train and test
        self.min_results = 10 #minimum number of results needed in a training period to consider the results
        self.training_name_ = '_training'
        self.test_name_ =  '_test'
        self.doc_name_ = {self.training_name_ : self.training_name_,self.test_name_:self.test_name_}
        #String added to the results file name
        self.training_ = 15 #Lenght in months of training period
        self.test_ = 7 #Lenght in months of testing period
        self.dict_name_ = {self.training_name_:self.training_,self.test_name_:self.test_}

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

        #Number of data (points) we check before and after to find a local min and max
        self.window = 6

        #Initial value of portfolio
        self.init_value = 10000


        # Metrics used to calculate the strategy performance
        self.pnl_dict = {}
        self.sharpe_ratio_ = 'Sharpe ratio'  # Did not substract the risk-free rate, only return divided by vol
        self.ann_return_ = 'Annualized return'
        self.ann_vol_ = 'Annualized volatility'
        self.pour_win_ = '% win'  # pourcentage of winning trades
        self.max_draw_ = 'Maximum drawdown'
        # self.sorino_ratio

        # Values used to calculate each trade performance
        self.entry_row = 'Entry_row'
        self.entry_level = 'Entry_level'
        self.exit_row = 'Exit_row'
        self.exit_level = 'Exit_level'
        self.trade_return = 'trade_return'
        self.trades_track = pd.DataFrame(columns=[self.entry_row, self.entry_level, self.exit_row, self.exit_level, \
                                                  self.trade_return])

        self.default_data = self.adj_close_name  # Value we use by default for chart, extremum, etc.

        # DE-TRENDING
        # ------------
        self.is_detrend = False  # Possible to set to yes or no
        self.p_value = .01  # significance level to test for non stationarity with Augmented Dickey-Fuller
        self.period = 1

    def __call__(self):

        """ Set values for optimization if we decide to optimize

        The one that we don't actually want to optimize or any default value that has to be initialize

        It is the values that are initialized  and used through the system

        Attributes
        ----------

            Exit
                Extension
                `self.exit_ext_name` : str
                    name of the dictionary key to try to exit the market with Fibonnacci extensions
                `self.exit_ext` : bool
                    tells the system if tries to exit (or not) the market using the largest extension as a reference.
                    Ex : largest extension from preivous trend is 1, the system takes profit when it is 2.618 this size. So,
                    when this value is reached, it takes the profit.
                `self.profit_ext` : float
                     % of the largest extension from previous trend that the system uses to exit the market to take profit
                     (default value is 2.618)
                `self.stop_ext` : float
                        % of the largest extension from previous trend that the system uses as a stop loss
                     (default value is 1.618)

            Stop tightening
                General
                `self.stop_tight_dict` : dictionary
                    contains the different possibilities to tighten the stop
                `self.is_true` : bool
                    tells the system if it has to use this particular technique to tighten the stop or not
                `self.default_data_` : bool
                    default data used to determine if the stop loss level must be tightened. It is `True`, then
                    `self.adj_close_name` is used. Otherwise, `self.low_name` with `self.high_name` (depends if it is
                    a buy or sell signal).

                Stop tightening (technique no 1)
                `self.stop_tight_ret` : str
                     tightening the stop using Fibonacci retracement condition (contains the condition).
                `self.stop_ret_level` : float
                    level at which the system tight the stop when it reaches this retracement in the opposite direction.
                    Ex: Buy signal then, market reaches `self.stop_ret_level` (.882 by default) in the other direction.
                    The system will tighen the stop to the lowest (or highest) point

            Exit
                All the possible ways that the system can exit the market (extension, retracement)

            Trades

        """
        if self.is_walkfoward:
            self.optimize()

        self.nb_data = 200  # nb of data on which data are tested, can be 150, 200, 300
        self.buffer_extremum = self.nb_data/2  #when trying to enter in the market, we give a buffer trying to find the
                                              #the global max or min (half of self.nb_data by default)

        # Indicator value to trigger a signal
        self.r_square_level = .7 #can be .6, .7 and .9 too
        self.min_data = 100  # (0,50,100 or 150) min nb of data between a signal


        #ENTRY
        #-----
        # All the possible entry types that the system can do (extension, retracement)

        self.enter_bool = 'enter_bool' #same key name for all the exit strategy (located in different dictionary)
        self.enter_ext_name = 'enter_ext_name'
        self.enter_ext = 'enter_ext' #Entering the market with largest extension from setback in current trend
        self.stop_ext = 'stop_ext'
        self.enter_time = 'enter_time'
        self.time_ext = 'time_ext' #Entering the market only if the current setback is a minimum percentage of
                                    #largest setback from current trend in term of time

        self.enter_dict = {self.enter_ext_name :
                              {self.enter_bool : True,
                               self.enter_ext: 1, #could be .882 or .764, this is the % of largest extension at which
                                                  #the system enters the market
                               },
                           self.enter_time:
                               {self.enter_bool : True,
                                self.time_ext : 0.618 #could be .5, .764,1
                                }
                          }

        #STOP TRY ENTER
        #--------------
        #These params are conditions to stop trying to enter the market if the current
        # price reach a % of the largest extension

        self.bol_st_ext = True  #Tells the system if it has to stop trying to enter the market using
                                # Fibonacci extension techniques. Can be optimized to True or False
        self.fst_cdt_ext = .764 #% of the largest extension that if the market reaches, the system
                                # stops trying to enter the market. Can be optimized to .618, .764 or .882
        self.sec_cdt_ext = 1.382 #% if the system triggers the first condition, then if it reaches this level in the
                                #opposite direction, the system brings the stop loss closer to the last peak or
                                # low (default value = adj. close). Can be set to .618, .764, 1 or 1.382

        #STOP TIGHTENING
        #---------------

        #Stop tightening technique no 1. See description above in docstrings
        self.stop_tight_ret =  'stop_tight_ret'
        self.stop_tight_pour = 'stop_tight_pourentage'
        self.is_true = 'is_true'
        self.default_data_ = 'default_data_' #adjusted closed
        self.stop_ret_level = 'stop_ret_level'
        self.tight_value = 'tight_value'
        self.pour_tight = 'pour_tight'
        self.stop_tight_dict = {self.stop_tight_ret :
                                    {self.is_true : True, #can be optimized (possible value is True or False)
                                                            #True if the system use this technique
                                     self.default_data_ : True, #can be optimized (True or False)
                                                            #True it uses the adj. close. False it uses low for buy
                                                            #signal and high for sell signal
                                     self.stop_ret_level : 1 #can be optimized at .618, .764, 1, 1.382, 1.618 or 2
                                     },

                                self.stop_tight_pour :  #tighten when at 50% of target
                                    {self.is_true : True,
                                     self.tight_value : .5,  #.5,.618,.764 is possible too - % of target reached when
                                                            #we tight
                                     self.pour_tight : .5 #.5, .618 possible values, how much we tight
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
                              {self.exit_ext_bool : True,
                               self.profit_ext : 3.382, #also try 2.618, 3.382, 4.236
                               self.stop_ext : 1.618    #also try 1.382, 2
                               }
                          }

    def optimize(self):
        self.dict_date_ = dm.date_dict(self.date_debut, self.date_fin,
                                       **self.dict_name_)
        t = 5