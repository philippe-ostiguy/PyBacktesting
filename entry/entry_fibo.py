import math_op as mo
import initialize as init
import operator as op
import math



class EntFibo(init.Initialize):

    @classmethod
    def __init__(cls,series):

        """ Class that uses Fibonnacci strategy to enter and exit from the market

        Trying to enter the market with Fibonacci retracement and extension. 3 types:
            1- Retracement from the last wave
            2- Retracement from beginning of the trend
            3- Extension from a previous wave (largest one in the last trend)

        Then try to exit the market using Fibonnacci extension or retracement


        Parameters
        ----------
        series : DataFrame list
            Contains all market prices (OHLC) according to the initial date range

        Notes (Improvements to do)
        --------------------------

            - No slippage included in entry or exit. If the price reached the desired level, we just exit at either the
            current price or the next desired price
            - The system doesn't check on a shorter time frame if it reaches an entry point and a stop at the same time
            or even an exit point and stop at the same time (in case of high volatility).
                - The system is "conservative", if a stop is trigerred it will priorise it over an entry or exit.
                    It also prioritizes an entry over a new low/high or when the system reaches an extension's condition
                    (conditions that make the system stop trying to enter in the market when trigerred)
                - Taking into account the system, those are really rare cases. However it could be tested by using a
                shorter time every time an entry or exit signal
                - Desired modifications should be in functions "try_entry" and "try_exit"

        """

        super().__init__(cls,class_method=True)

        cls.series=series
        cls.extreme = {}
        cls.high="max"
        cls.low="min"
        cls.high_idx="max_idx"
        cls.low_idx = "min_idx"
        cls.fst_ext_cdt = False #by default first condition for extension it not met, set to False

    @classmethod
    def __call__(cls,curr_row,buy_signal=False,sell_signal=False):
        """
        Default function to determine the entry point
        """

        cls.buy_signal = buy_signal
        cls.sell_signal = sell_signal
        cls.curr_row = curr_row #Row on which the system has a signal. It has to enter on the next row
        cls.is_entry = False
        cls.price_entry = 0 #price at which the system enters
        cls.relative_extreme = 0 #last wave the system uses (relative low bor buy, vice versa) as a basis to calculate
                            # the profit taking price. It uses the default data (close) to smooth data

        cls.first_data = curr_row - cls.nb_data - cls.buffer_extremum + 1
        if cls.first_data < 0:
            cls.first_data = 0

        if buy_signal and sell_signal :
            raise Exception('Cannot have a buy and sell signal at the same time')

        cls.set_extremum() #set the absolute high and low on the current trend

        if cls.buy_signal:
            start_point=cls.extreme[cls.low_idx]
            cls.fst_op=op.gt
            cls.sec_op=op.lt
            cls.trd_op=op.sub
            cls.fth_op=op.add
            cls.fif_op=op.ge
            cls.six_op=op.le
            cls.fst_data = cls.high
            cls.sec_data = cls.low
            cls.fst_idx = cls.high_idx
            cls.sec_idx = cls.low_idx
            cls.entry = cls.stop = cls.low_name
            cls.exit = cls.high_name
            cls.inv = -1

        if cls.sell_signal:
            start_point = cls.extreme[cls.high_idx]
            cls.fst_op=op.lt
            cls.sec_op=op.gt
            cls.trd_op=op.add
            cls.fth_op=op.sub
            cls.fif_op=op.le
            cls.six_op=op.ge
            cls.fst_data = cls.low
            cls.sec_data = cls.high
            cls.fst_idx = cls.low_idx
            cls.sec_idx = cls.high_idx
            cls.entry = cls.stop = cls.high_name
            cls.exit = cls.low_name
            cls.inv = 1

        cls.mo_ = mo.MathOp(series=cls.series, default_col=cls.default_data)
        cls.local_extremum_=cls.mo_.local_extremum(start_point=start_point, end_point=cls.curr_row, window=cls.window, \
                                                   min_=cls.low,max_=cls.high)
        cls.local_extremum_ = cls.local_extremum_.reset_index(drop=True)
        #last_index = cls.local_extremum_[cls.sec_data].last_valid_index()
        #cls.rel_extreme = cls.local_extremum_.at[last_index, cls.sec_data]

        cls.largest_extension() #finding the largest extension used for potential entry and/or exit

        cls.try_entry()

        if cls.is_entry:
            cls.try_exit()

    @classmethod
    def largest_extension(cls):
        """
        Find largest extension from current trend
        """

        if cls.buy_signal:
            my_data={}
            fst_data='curr_high'
            sec_data='curr_low'
            my_data[fst_data]=None
            my_data[sec_data] = None
            fst_name=cls.rel_high
            sec_name=cls.rel_low

        if cls.sell_signal:
            my_data={}
            fst_data='curr_low'
            sec_data='curr_high'
            my_data[fst_data]=None
            my_data[sec_data] = None
            fst_name=cls.rel_low
            sec_name=cls.rel_high

        curr_row_ = 0

        while curr_row_ < len(cls.local_extremum_):
            if curr_row_ ==7:
                t=5

            #It checks at the second last data, if there is a data for second_name (new relative high for sell
            # or new relative low for buy), it just basically don't check it, because it is not a real extension
            if curr_row_ == (len(cls.local_extremum_) -1):
                    if not math.isnan(cls.local_extremum_.iloc[curr_row_, \
                            cls.local_extremum_.columns.get_loc(sec_name)]) & \
                    (curr_row_ == (len(cls.local_extremum_) -1 )):
                        break

                    pass

            if  my_data[fst_data] == None:
                my_data[fst_data] = cls.local_extremum_.iloc[curr_row_,cls.local_extremum_.columns.get_loc(fst_name)]
                curr_row_+=1

                t_curr_row = curr_row_

                try:
                    test = cls.local_extremum_.iloc[t_curr_row, cls.local_extremum_.columns.get_loc(fst_name)]

                except:
                    break

                while not math.isnan(cls.local_extremum_.iloc[t_curr_row, \
                                                              cls.local_extremum_.columns.get_loc(fst_name)]) & (
                                  t_curr_row < len(cls.local_extremum_)):

                    if cls.fst_op(cls.local_extremum_.iloc[t_curr_row, cls.local_extremum_.columns.get_loc(fst_name)], \
                                  my_data[fst_data]):
                        my_data[fst_data] = cls.local_extremum_.iloc[t_curr_row, \
                                                                     cls.local_extremum_.columns.get_loc(fst_name)]

                    t_curr_row += 1

                    try:
                        test = cls.local_extremum_.iloc[t_curr_row, cls.local_extremum_.columns.get_loc(fst_name)]

                    except:
                        break

                t_curr_row = 0
                continue

            if (math.isnan(my_data[fst_data]) \
                 | cls.fst_op(cls.local_extremum_.iloc[curr_row_,cls.local_extremum_.columns.get_loc(fst_name)], \
                          my_data[fst_data])) & (my_data[sec_data] == None):
                my_data[fst_data] = cls.local_extremum_.iloc[curr_row_,cls.local_extremum_.columns.get_loc(fst_name)]


            if my_data[sec_data] == None:

                my_data[sec_data] = cls.local_extremum_.iloc[curr_row_, cls.local_extremum_.columns.get_loc(sec_name)]
                curr_row_+=1

                if curr_row_ ==  len(cls.local_extremum_):
                    if math.isnan(my_data[sec_data]):
                        break
                    pass

                else:
                    t_curr_row = curr_row_

                    try:
                        test = cls.local_extremum_.iloc[t_curr_row, cls.local_extremum_.columns.get_loc(sec_name)]

                    except:
                        break

                    while not math.isnan(cls.local_extremum_.iloc[t_curr_row, \
                     cls.local_extremum_.columns.get_loc(sec_name)]) & (t_curr_row < len(cls.local_extremum_)):

                        if cls.sec_op(cls.local_extremum_.iloc[t_curr_row, \
                                        cls.local_extremum_.columns.get_loc(sec_name)], my_data[sec_data]):

                            my_data[sec_data] = cls.local_extremum_.iloc[t_curr_row, \
                                                                        cls.local_extremum_.columns.get_loc(sec_name)]

                        t_curr_row += 1

                        try:
                            test = cls.local_extremum_.iloc[t_curr_row, cls.local_extremum_.columns.get_loc(fst_name)]

                        except:
                            break

                    t_curr_row = 0
                    continue

            if curr_row_ !=  len(cls.local_extremum_):
                if (math.isnan(my_data[sec_data])) \
                        | cls.sec_op(cls.local_extremum_.iloc[curr_row_,cls.local_extremum_.columns.get_loc(sec_name)], \
                             my_data[sec_data]):
                    my_data[sec_data] = cls.local_extremum_.iloc[curr_row_, cls.local_extremum_.columns.get_loc(sec_name)]

                    curr_row_+=1

                    if curr_row_ == len(cls.local_extremum_):
                        if math.isnan(my_data[sec_data]):
                            break
                        pass

                    else:
                        continue

            if not hasattr(cls,'largest_extension_'):
                cls.largest_extension_ = cls.inv*(my_data[sec_data] - my_data[fst_data])
                my_data[fst_data] = None
                my_data[sec_data] = None
                continue

            if op.ge(cls.inv*(my_data[sec_data] - my_data[fst_data]), cls.largest_extension_):
                cls.largest_extension_ = cls.inv*(my_data[sec_data] - my_data[fst_data])
                my_data[fst_data] = None
                my_data[sec_data] = None
                continue

            my_data[fst_data] = None
            my_data[sec_data] = None

    @classmethod
    def set_extremum(cls):
        """
        PURPOSE
        -------
        Set the global max and min for the given range (from first_data to curr_row)

        """

        data_range = cls.series.loc[cls.first_data:cls.curr_row,cls.default_data]
        cls.extreme = {cls.high : data_range.max(),
                       cls.low : data_range.min(),
                       cls.high_idx : data_range.idxmax(),
                       cls.low_idx : data_range.idxmin()
                       }

    @classmethod
    def try_entry(cls):
        """ Method that try entering in the market

        Function that will try to enter in the market :
                Until the system hit the desired extension and/or retracement. At the moment, only using extension (the
                    largest because size matters), which is `cls.largest_extension_` set in function
                    `cls.largest_extension()`. We can decide the proportion of the largest extension we want the system
                    to use in module `initialize.py` within dictionary `cls.enter_dict{}` and variable `cls.enter_ext`
                    (default value is 1)
                Stop trying to enter in the market when a condition is met
                    (Fibonnacci extension 0.618% of largest past extension)

        NOTES
        -----
        - Note that the system will priorise an entry over a new high or new low (to be more conservative). To solve
        this issue (rare cases, only with high volatility) :
            Check simulateneously if a new high or low is reached &  (if a buy/sell level is trigerred |
                market hits minimum required extension (if this condition is tested))
            Then, on a shorter timeframe, check if an entry | minimum required extension is reached before the
                market makes new low or high, vice versa

        - The entry signal are based on extension at the moment. We could check if it true or false for different entry
        type

        - If the price of the current row on which the signal is trigerred is below the buying level or above the
        selling level, the system just don't execute it and end it. CHECK THIS... Maybe the system could enter unless
        the price goes below the stop loss (buy) or above the stop loss (sell)

        """

        data_test = len(cls.series) - cls.curr_row-1

        if cls.is_entry:
            raise Exception('Already have an open position in the market...')

        cls.relative_extreme = cls.series.loc[cls.curr_row, cls.default_data]

        for curr_row_ in range(data_test):

            #The system first check if the price on the current row is below (for buy) or above (for sell signal)
            #If it is the case, the system just don't enter in the market
            if curr_row_ == 0 & cls.fif_op(cls.trd_op(cls.extreme[cls.fst_data],cls.largest_extension_*\
                        cls.enter_dict[cls.enter_ext_name][cls.enter_ext]),\
                          cls.series.loc[cls.curr_row,cls.entry]):
                cls.is_entry = False
                break

            cls.curr_row += 1

            #Buy or sell signal (entry) with extension
            #   - Buy if current market price goes below our signal or equal
            #   - Sell if current market price goee above our signal or equal
            if cls.fif_op(cls.trd_op(cls.extreme[cls.fst_data],cls.largest_extension_*\
                        cls.enter_dict[cls.enter_ext_name][cls.enter_ext]),\
                          cls.series.loc[cls.curr_row,cls.entry]):
                cls.is_entry = True
                cls.price_entry=cls.series.loc[cls.curr_row,cls.entry]
                cls.relative_extreme = cls.series.loc[cls.curr_row,cls.default_data]
                break

            #Market hits the minimum required extension - first condition met (point to enter in the market)
            if cls.bol_st_ext & cls.fif_op(cls.trd_op(cls.extreme[cls.fst_data], \
                        cls.largest_extension_ * cls.fst_cdt_ext), cls.series.loc[cls.curr_row,cls.entry]):
                cls.relative_extreme = cls.series.loc[cls.curr_row, cls.default_data]
                cls.fst_ext_cdt = True
                continue

            # The system will stop trying to enter in the market :
            #   - first condition (extension) is met (hit a required
            #       % of the largest extension, previously (61.8% by default)
            #   - It went back then reached the minimum retracement (88.2% by default)

            """ 
            if cls.buy_signal:
                start_point = cls.extreme[cls.low_idx]
                cls.fst_op = op.gt
                cls.sec_op = op.lt
                cls.trd_op = op.sub
                cls.fth_op = op.add
                cls.fif_op = op.ge
                cls.six_op = op.le
                cls.fst_data = cls.high
                cls.sec_data = cls.low
                cls.fst_idx = cls.high_idx
                cls.sec_idx = cls.low_idx
                cls.entry = cls.stop = cls.low_name
                cls.exit = cls.high_name
                cls.inv = -1
            """

            if cls.bol_st_ext & cls.fst_ext_cdt :
                if cls.six_op(cls.fth_op(cls.relative_extreme,cls.inv*(op.sub(cls.relative_extreme, \
                        cls.extreme[cls.fst_data])*cls.sec_cdt_ext)),cls.series.loc[cls.curr_row,cls.exit]) :
                    print(f"The market hits previously the required {cls.fst_cdt_ext} % of the largest extension \
                       and then retrace in the opposite direction of {cls.sec_cdt_ext}")

                    break
                pass

            #Changing global low or high if current one is lower or higher
            if cls.fst_op(cls.series.loc[cls.curr_row, cls.default_data], cls.extreme[cls.fst_data]):

                cls.extreme[cls.fst_data] = cls.series.loc[cls.curr_row, cls.default_data]
                cls.extreme[cls.fst_idx] = cls.curr_row

    @classmethod
    def try_exit(cls):

        """Method which try to exit the market.

        This method exit the market when a close signal is triggered or a stop loss is
        trigerred

        Notes
        -----
        The stops is tighten if :
            `self.bol_st_ext` is `True` in `initialize.py` (we tell the system to test this feature) &
            `self.sec_cdt_ext` in `initialize.py` is met, ie the market rebounces (or setback) to the desired
                retracement compared to the last peak or low (default value is 0.882 and `self.default_data` used for
                calculation is `self.adj_close_name`

        """

        """ 
        if cls.sell_signal:
            start_point = cls.extreme[cls.high_idx]
            cls.fst_op=op.lt
            cls.sec_op=op.gt
            cls.trd_op=op.add
            cls.fth_op=op.sub
            cls.fif_op=op.le
            cls.six_op=op.ge
            cls.fst_data = cls.low
            cls.sec_data = cls.high
            cls.fst_idx = cls.low_idx
            cls.sec_idx = cls.high_idx
            cls.entry = cls.stop = cls.high_name
            cls.exit = cls.low_name
            cls.inv = 1
        """

        data_test = len(cls.series) - cls.curr_row - 1

        #Put cls.entry to false if the system exit the market


        #define stop loss and taking profit first
        #using extension strategy to exit
        if cls.exit_dict[cls.exit_ext_name][cls.exit_bool]:
            stop = cls.trd_op(cls.extreme[cls.fst_data], \
                              cls.exit_dict[cls.exit_ext_name][cls.stop_ext] * cls.largest_extension_)
            exit_ =

        #HERE

        #if cls.


        # Buy or sell signal (taking profit)
        #   - Buy if current market price goes below our signal or equal
        #   - Sell if current market price goes above our signal or equal

        if cls.fif_op(cls.trd_op(cls.extreme[cls.fst_data], cls.largest_extension_), \
                      cls.series.loc[cls.curr_row, cls.entry]):
            pass
        #break

        cls.is_entry = False