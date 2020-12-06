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

"""Module that will try to enter the market using Fibonnacci techniques"""

import math_op as mo
import initialize as init
import operator as op
import math

class EntFibo():
    """
    Class that uses Fibonnacci strategies to enter the market """
    
    def __init__(self):
        self.extreme = {}
        self.high="max"
        self.low="min"
        self.high_idx="max_idx"
        self.low_idx = "min_idx"
        self.fst_ext_cdt = False #by default first condition for extension is not met, set to False
        self.is_entry = False
        self.relative_extreme = None #last wave the system uses (relative low for buy, vice versa) as a
                                        # basis to calculate the profit taking price. It uses the default data (close)
                                          # to smooth data
        self.row_rel_extreme = 0
        self.largest_time = 0 #extension in time
        self.index_name = 'index'
    
    def ent_fibo(self,curr_row,buy_signal=False,sell_signal=False):
        """This the main method that uses Fibonnacci strategies to enter the market

        First, the method finds local minimum and maximum in the current trend with function `self.local_extremum_()`.
        Then using `self.largest_extension()`, it finds the largest setback which is stored in the attribute
        `self.largest_extension_`. This function also store the largest setback in term of time in `self.largest_time`.
        Then in method `self.try_entry()`, the system will try to enter the market..

        Trying to enter the market with Fibonacci retracement and extension. 3 types:
            Retracement from the last wave
            Retracement from beginning of the trend
            Extension from the current trend (largest one in the last trend)

        At the moment, it is possible to enter the market only with extensions from the current trend.

        Parameters
        ----------
        `self.buy_signal` and `self.sell_signal` : bool
            The module `r_aquare_ty.py` (or package `trading_rules`) tells us if there a buy or sell signal. Then,
            just not to have the code twice, we set some variable depending on if `self.buy_signal` or
            `self.sell_signal` is `True`.

        Notes
        -----
        No slippage included in `self.try_entry()`. If the price reached the desired level, we just exit at either the
        current price or the next desired price

        The system doesn't check on a shorter time frame if it reaches an entry point and a stop at the same time
        or even an exit point and stop at the same time (in case of high volatility) in `self.try_entry()`
        Taking into account how the system works, those are really rare cases. However it could be tested by using a
        shorter time every time there is an entry or exit signal

        """

        self.curr_row=curr_row
        self.buy_signal=buy_signal
        self.sell_signal=sell_signal

        if (self.largest_time != 0):
            raise Exception("Largest extension in term of times is not equal to 0 in __init__")

        self.first_data = self.curr_row - self.nb_data + 1
        if self.first_data < 0:
            self.first_data = 0

        if self.buy_signal and self.sell_signal :
            raise Exception('Cannot have a buy and sell signal at the same time')

        self.set_extremum() #set the absolute high and low on the current trend

        if self.buy_signal:
            start_point=self.extreme[self.low_idx]
            self.fst_op=op.gt
            self.sec_op=op.lt
            self.trd_op=op.sub
            self.fth_op=op.add
            self.fif_op=op.ge
            self.six_op=op.le
            self.fst_data = self.high
            self.sec_data = self.low
            self.fst_idx = self.high_idx
            self.sec_idx = self.low_idx
            self.entry = self.stop = self.low_name
            self.exit = self.high_name
            self.inv = -1

        if self.sell_signal:
            start_point = self.extreme[self.high_idx]
            self.fst_op=op.lt
            self.sec_op=op.gt
            self.trd_op=op.add
            self.fth_op=op.sub
            self.fif_op=op.le
            self.six_op=op.ge
            self.fst_data = self.low
            self.sec_data = self.high
            self.fst_idx = self.low_idx
            self.sec_idx = self.high_idx
            self.entry = self.stop = self.high_name
            self.exit = self.low_name
            self.inv = 1

        self.mo_ = mo.MathOp(series=self.series, default_col=self.default_data)
        self.local_extremum_=self.mo_.local_extremum(start_point=start_point, end_point=self.curr_row, \
                                            window=self.window, min_=self.low,max_=self.high,index_= self.index_name)
        self.local_extremum_ = self.local_extremum_.reset_index(drop=True)

        self.largest_extension() #finding the largest extension used for potential entry and/or exit
        if not hasattr(self, 'largest_extension_'): #in case it doesn't find a largest_extension,
            self.is_entry = False                    # exit and just do nothing to avoid error
            return
        self.set_value()
        self.try_entry()

    def largest_extension(self):
        """ Find largest extension (setback) from current trend (Fibonacci) in size which is stored in
        `self.largest_extension_` and largest in term of time stored in `self.largest_time`.
        """

        if self.buy_signal:
            my_data={}
            fst_data='curr_high'
            sec_data='curr_low'
            my_data[fst_data]=None
            my_data[sec_data] = None
            fst_name=self.high
            sec_name=self.low

        if self.sell_signal:
            my_data={}
            fst_data='curr_low'
            sec_data='curr_high'
            my_data[fst_data]=None
            my_data[sec_data] = None
            fst_name=self.low
            sec_name=self.high

        trd_data = 'first_index'
        my_data[trd_data] = 0
        fth_data = 'sec_index'
        my_data[fth_data] = 0

        for curr_row_ in range(len(self.local_extremum_)):

            #Sorten the name
            fst_val = self.local_extremum_.iloc[curr_row_, self.local_extremum_.columns.get_loc(fst_name)]
            sec_val = self.local_extremum_.iloc[curr_row_, self.local_extremum_.columns.get_loc(sec_name)]
            _current_index = self.local_extremum_.iloc[curr_row_, self.local_extremum_.columns.get_loc(self.index_name)]

            #If there are value to high and low, assign largest_extension_
            if (my_data[fst_data] != None) & (my_data[sec_data] != None):
                if math.isnan(sec_val) & (not math.isnan(my_data[fst_data])) & (not math.isnan(my_data[sec_data])):

                    if not hasattr(self,'largest_extension_'):
                        self.largest_extension_ = self.inv*(my_data[sec_data] - my_data[fst_data])

                    if (my_data[fst_data] != None) & (my_data[sec_data] != None) :
                        if op.ge(self.inv*(my_data[sec_data] - my_data[fst_data]), self.largest_extension_):
                            self.largest_extension_ = self.inv*(my_data[sec_data] - my_data[fst_data])

                    _ext_time = my_data[fth_data]- my_data[trd_data]
                    if (_ext_time>self.largest_time):
                        self.largest_time = _ext_time

                    my_data[fst_data] = None
                    my_data[sec_data] = None


            #It checks at the second last data, if there is a data for second_name (new relative high for sell
            # or new relative low for buy), it just basically don't check it, because it is not a real extension
            if curr_row_ == (len(self.local_extremum_) -1):
                if not math.isnan(sec_val) & (curr_row_ == (len(self.local_extremum_) -1 )):
                    break
                pass

            #Assign a value to first value (high for buy, low for sell) until it's NOT None or Nan
            if (my_data[fst_data] == None):
                my_data[fst_data] = fst_val
                my_data[trd_data] = _current_index
                continue

            if math.isnan(my_data[fst_data]):
                my_data[fst_data] = fst_val
                my_data[trd_data] = _current_index
                continue

            #If there is a valid first value, check if current value higher than recorded high (for buy), vice versa
            if not math.isnan(fst_val):
                if self.fst_op(fst_val, my_data[fst_data]):
                    my_data[fst_data] = fst_val
                    my_data[trd_data] = _current_index
                continue

            if (my_data[sec_data] == None):
                my_data[sec_data] = sec_val
                my_data[fth_data] = _current_index
                continue

            if math.isnan(my_data[sec_data]):
                my_data[sec_data] = sec_val
                my_data[fth_data] = _current_index
                continue

            if not math.isnan(sec_val):
                if self.sec_op(sec_val, my_data[sec_data]):
                    my_data[sec_data] = sec_val
                    my_data[fth_data] = _current_index
                continue

    
    def set_extremum(self):
        """
        Set the global max and min for the given range (from first_data to curr_row)."""

        data_range = self.series.loc[self.first_data:self.curr_row,self.default_data]
        self.extreme = {self.high : data_range.max(),
                       self.low : data_range.min(),
                       self.high_idx : data_range.idxmax(),
                       self.low_idx : data_range.idxmin()
                       }
    
    def set_value(self):
        """Method to set some values that are used in this class and sublcass """

        # extension level if condition in initialize.py is True
        if self.exit_dict[self.exit_name][self.exit_ext_bool]:
            self.extension_lost = self.largest_extension_ * self.exit_dict[self.exit_name][self.stop_ext]
            self.extension_profit = self.largest_extension_ * self.exit_dict[self.exit_name][self.profit_ext]
            self.stop_value = self.trd_op(self.extreme[self.fst_data], self.extension_lost)

            if self.extension_lost < 0:
                raise Exception(
                    f"Houston, we've got a problem, `self.extension_lost` in enter_fibo.py is {self.extension_lost} "
                    f"and should not be negative")
            if self.extension_profit < 0:
                raise Exception(f"Houston, we've got a problem, `self.extension_profit` in enter_fibo.py is "
                                f"{self.extension_profit} and should not be negative")

    
    def try_entry(self):
        """
        Method that try entering in the market

        Function that will try to enter the market :
                Until the system hit the desired extension and/or retracement. At the moment, only using extension (the
                largest), which is `self.largest_extension_`. We can decide the proportion of the largest
                extension we want the system to use in module `initialize.py` within dictionary `self.enter_dict{}`
                and variable `self.enter_ext` (default value is 1)
                It can also enter in the market only if the market retraces (or setback) above a certain amount of time
                `self.time_ext` (set in `initialize.py`) the largest setback in term of time from the current
                trend `self.largest_time`

                Possibility to stop trying to enter in the market when a condition is met.
                    At the moment, the only condition is when the price during a setback hits  a
                    percentage `self.fst_cdt_ext` (0.618 by default) of the largest extension `self.largest_extension_`
                    (low for a buy signal and high for a sell signal which is `self.entry`)
                    AND hits the minimum retracement in the other direction `self.sec_cdt_ext` (.882 by default)
                    Set to `True` with `self.bol_st_ext` in `initialize.py to have this condition.

        Parameters
        ----------
        `self.largest_extension_` : float
            the largest extension or setback (in point) from the the current trend
        `self.enter_ext` : float
            This is the % of largest extension at which the system enters the market. Can be .882 or .764 or 1
        `self.largest_time` :
            the largest setback from the current trend
        `self.time_ext` : float
            Proportion in term in time needed that the current setback most do compared to the largest extension
            in therm of time in the current trend to enter the market. It can be .5, .618 .884,1. Set in `initialize.py`
        `self.bol_st_ext` : bool
            Tells the system if it has to stop trying to enter the market using Fibonacci extension techniques.
            Can be optimized to `True` or `False`. Set in `initialize.py`
        `self.fst_cdt_ext` : float
            % of the largest extension that if the market reaches, the system stops trying to enter the market.
            Possible values are .618, .764 or .882. Set in `initialize.py`
        `self.sec_cdt_ext` : float
             if the market triggers the first condition, then if it reaches this level in the opposite direction, the
            # system stops trying to enter in the market. Can be set to .618, .764, 1 or 1.382. Set in `initialize.py`

        Notes
        -----
        Note that the system will priorise an entry over a new high or new low (to be more conservative). To solve
        this issue (rare cases, only with high volatility) :
            Check simulateneously if a new high or low is reached &  (if a buy/sell level is trigerred or
                if the market hits minimum required extension (if this condition is tested))
            Then, on a shorter timeframe, check if an entry or minimum required extension is reached before the
                market makes new low or high, vice versa

        If the price of the current row on which the signal is trigerred is below the buying level or above the
        selling level, the system just don't execute it and end it.
        """

        data_test = len(self.series) - self.curr_row - 1

        #Data used only in entry.fibo at the moment
        _largest_time = self.largest_time * self.enter_dict[self.enter_time][self.time_ext]
        _bool_time = self.enter_dict[self.enter_time][self.enter_bool]
        _largest_ext = self.largest_extension_ * self.enter_dict[self.enter_ext_name][self.enter_ext]
        _bool_ext = self.enter_dict[self.enter_ext_name][self.enter_bool]

        if self.is_entry:
            raise Exception('Already have an open position in the market...')

        self.set_value()

        for curr_row_ in range(data_test):

            #We may change that later if we decides to use other things than only the largest extension to enter in
            # the market. It checks if there is a "largest extension" set (in some case, there might not be)
            if not hasattr(self, 'largest_extension_'):
                self.is_entry = False
                print("Not any largest extension")
                break

            if _bool_ext:
                if _largest_ext < 0: #Can happens when the market moves really fast and not able to find
                                        # a `self.largest_extension` that is positive
                    self.is_entry = False
                    break
                _entry_tentative = self.trd_op(self.extreme[self.fst_data], _largest_ext)

            #Test first if using Fibonacci extension as a signal to enter in the market.
            #Then the system first check if the price on the current row is below (for buy) or above (for sell signal)
            #If it is the case, the system just don't enter in the market.
            if self.enter_dict[self.enter_ext_name][self.enter_bool]:
                if (curr_row_ == 0) & self.fif_op(_entry_tentative, self.series.loc[self.curr_row,self.entry]):
                    self.is_entry = False
                    break

            self.curr_row += 1

            _current_value = self.series.loc[self.curr_row, self.default_data] #curent value with default data type
            _current_stop = self.series.loc[self.curr_row, self.stop] #current stop value with data stop type
            _current_entry = self.series.loc[self.curr_row, self.entry]

            if not hasattr(self, 'stop_value'):
                self.is_entry = False
                print("Not any stop_value")
                break

            if self.relative_extreme == None:
                self.relative_extreme = self.series.loc[self.curr_row, self.default_data]
                self.row_rel_extreme = self.curr_row

            #Check if has to enter after a certain time only
            if _bool_time & (curr_row_ <_largest_time):
                # Retrace two quickly (in time) and went below (for a buy signal) the stop loss. Do not enter
                if self.six_op(_current_stop, self.stop_value):
                    self.is_entry = False
                    break
                else :
                    continue

            #Buy or sell signal (entry) with extension
            #   - Buy if current market price goes below our signal or equal
            #   - Sell if current market price goes above our signal or equal
            if self.enter_dict[self.enter_ext_name][self.enter_bool]:
                if self.six_op(_current_entry,_entry_tentative):

                    #Check if current price is below (for buy) desired entry level after the minimum time. If yes,
                    #the market enters at the current price and not the desired
                    if _bool_time & (self.curr_row == math.ceil(_largest_time)):
                        _entry_level = _current_entry
                    else :
                        _entry_level = _entry_tentative

                    self.is_entry = True
                    self.trades_track_ = self.trades_track_.append({self.entry_row: self.curr_row,\
                                                            self.entry_level:_entry_level},ignore_index=True)

                    if self.sec_op(_current_value, self.relative_extreme):
                        self.relative_extreme = _current_value
                        self.row_rel_extreme = self.curr_row
                    break

            #Market hits the minimum required extension - first condition met (to stop trying entering the market)
            if self.bol_st_ext & self.six_op(_current_entry, \
                        self.trd_op(self.extreme[self.fst_data],self.largest_extension_ * self.fst_cdt_ext)):
                if self.sec_op(_current_value, self.relative_extreme):
                    self.relative_extreme = _current_value
                    self.row_rel_extreme = self.curr_row
                self.fst_ext_cdt = True
                continue

            # The system will stop trying to enter the market :
            #   - first condition (extension) is met. It hit the required
            #       % of the largest extension, previously (61.8% by default) - low for buy, high for sell
            #   - It went back then reached the minimum retracement in the other direction (88.2% by default)
            if self.bol_st_ext & self.fst_ext_cdt & (self.relative_extreme != None) :
                if self.fif_op(self.series.loc[self.curr_row,self.default_data],self.fth_op(self.relative_extreme,\
                            self.inv*(op.sub(self.relative_extreme, self.extreme[self.fst_data])*self.sec_cdt_ext))) :
                    #print(f"The market hits previously the required {self.fst_cdt_ext} % of the largest extension"
                    #      f"and then retrace in the opposite direction of {self.sec_cdt_ext}")
                    self.is_entry = False
                    break
                pass

            #Changing global low or high if current one is lower or higher
            if self.fst_op(self.series.loc[self.curr_row, self.default_data], self.extreme[self.fst_data]):
                self.extreme[self.fst_data] = self.series.loc[self.curr_row, self.default_data]
                self.extreme[self.fst_idx] = self.curr_row

                #Changing stop value
                if self.exit_dict[self.exit_name][self.exit_ext_bool]:
                    self.stop_value = self.trd_op(self.extreme[self.fst_data], self.extension_lost)