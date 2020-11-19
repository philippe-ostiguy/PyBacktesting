"""Module that will try to exit the market when we are in """

import entry.entry_fibo as ef
import sys
import operator as op
import math
import copy
import pandas as pd

class ExitFibo(ef.EntFibo):
    """ Class that uses Fibonnacci strategy to exit the market.

        It first uses the `EntFibo()` class in `entry_fibo.py` to enter in the market.
        """
    
    def __init__(self,init_):

        new_obj = init_
        self.__dict__.update(new_obj.__dict__) #replacing self object with Initialise object
        del init_,new_obj
        self.trades_track_ = pd.DataFrame(columns=[self.entry_row, self.entry_level, self.exit_row, self.exit_level, \
                                                  self.trade_return])

    def __call__(self,curr_row,buy_signal=False,sell_signal=False):
        """ Method that will first try to enter the market with `self.ent_fibo` then it will try to exit with
        `self.try_exit()` whenever we have a position
        """

        super().__init__()
        self.ent_fibo(curr_row=curr_row, buy_signal=buy_signal, sell_signal=sell_signal)
        return self.try_exit()
    
    def try_exit(self):
        """
        This is the method that tries to exit the market when we have a position with `entry_fibo.py`

        We first get an entry confirmation with the function `self.ent_fibo()` in `entry_fibo.py`. Then we run through
        the remaining data (according to the determined data range). We have an profit, stop loss and the method
        even tighten the stop under certain circumstances.

        Then it tries to exit the market using Fibonacci retracement and extension. 1 type at the moment:
            1- Largest extension `self.largest_extension_` from the current trend. The `self.largest_extension_` is set
            in `entry_fibo.py`. It is in fact the largest setback in the current trend. This method uses
            `self.profit_ext` to calculate the profit level and `self.stop_ext` for the stop level

        There is no slippage included in `try_exit()`. If the price reached the desired level, we just exit at
        either the current price or the next desired price

        Parameters
        ----------
        `self.profit_ext` : float
             % of the largest extension from previous trend that the system uses to exit the market to take profit
             Default value is 2.618. Possible values are 1.618, 2 , 2.618, 3.382, 4.236.
        `self.stop_ext` : float
             % of the largest extension from previous trend that the system uses as a stop loss.
             Default value is 1.618. Possible values are 1, 1.382, 1.618, 2.
        `self.is_entry` : bool
            The value comes from `entry_fibo.py`. It says if we have a position.

        Notes
        -----
        The stops may be tightened (see "stop tightening" in `initialize.py`)

        The system doesn't check on a shorter time frame if it reaches an exit point and a stop in `try_exit()`
            in case of high volatility. Really rare cases

        """

        #If no entry signal, exit the function
        if not self.is_entry:
            return None

        _entry_level = self.trades_track_.iloc[-1, self.trades_track_.columns.get_loc(self.entry_level)]

        #stop tightening using extension
        _is_stop_ext = self.stop_tight_dict[self.stop_tight_ret][self.is_true]
        if _is_stop_ext:
            _extension_tight =  self.inv * op.sub(self.relative_extreme,self.extreme[self.fst_data])
            if _extension_tight < 0:
                _is_stop_ext = False #can happen in case of high volatility
            _extension_stop = _extension_tight * self.stop_tight_dict[self.stop_tight_ret][self.stop_ret_level]

            if self.stop_tight_dict[self.stop_tight_ret][self.default_data_]:
                _data_stop = self.default_data
            else :
                _data_stop = self.stop

        _is_stop_pour = self.stop_tight_dict[self.stop_tight_pour][self.is_true]
        if _is_stop_pour :
            _tight_value = self.stop_tight_dict[self.stop_tight_pour][self.tight_value]
            _pour_tight = self.stop_tight_dict[self.stop_tight_pour][self.pour_tight]

        #Check if the first row (where the signal is trigerred) is already below the stop loss (for buy)
        # and vice versa for sell signal. If yes, stop loss trigerred
        if self.exit_dict[self.exit_name][self.exit_ext_bool] & \
            self.six_op(self.series.loc[self.curr_row,self.stop],self.stop_value):
            self.is_entry = False
            self.trades_track_.iloc[-1, self.trades_track_.columns.get_loc(self.exit_row)] = self.curr_row
            self.trades_track_.iloc[-1, self.trades_track_.columns.get_loc(self.exit_level)] = \
                self.stop_value  # exit level
            self.trades_track_.iloc[-1, self.trades_track_.columns.get_loc(self.trade_return)] = \
                self.inv * ((_entry_level - self.stop_value) / _entry_level)
            return self.trades_track_

        data_test = len(self.series) - self.curr_row - 1

        #This is the part where we run through the data to try to exit the market
        for curr_row_ in range(data_test):

            self.curr_row += 1
            _curent_value = self.series.loc[self.curr_row, self.default_data] #curent value with default data type
            _current_stop = self.series.loc[self.curr_row, self.stop] #current stop value with data stop type

            #Profit can change if relative_extreme changes
            if self.exit_dict[self.exit_name][self.exit_ext_bool]:
                _profit_value = self.fth_op(self.relative_extreme, self.extension_profit)

            #Value that will make tighten the stop using extension
            if _is_stop_ext:
                _tight_trig = self.fth_op(self.relative_extreme,_extension_stop)

            # Value that will make tighten the stop using pourcentage
            if _is_stop_pour:
                _tight_pour_trig = _tight_value * (_profit_value - _entry_level) + _entry_level
                _tight_pour_level = _pour_tight *(_curent_value - _entry_level) + _entry_level

            #Stop loss trigerred?
            if self.exit_dict[self.exit_name][self.exit_ext_bool] & \
                    self.six_op(_current_stop, self.stop_value):
                self.is_entry = False
                self.trades_track_.iloc[-1,self.trades_track_.columns.get_loc(self.exit_row)] = self.curr_row
                self.trades_track_.iloc[-1, self.trades_track_.columns.get_loc(self.exit_level)] = \
                    self.stop_value #exit level
                self.trades_track_.iloc[-1, self.trades_track_.columns.get_loc(self.trade_return)] = \
                    self.inv*((_entry_level-self.stop_value)/_entry_level)
                break

            #Changing relative low (for a buying), vice versa
            if self.sec_op(_curent_value, self.relative_extreme):
                self.relative_extreme = _curent_value
                self.row_rel_extreme = self.curr_row

                #Changing stop tightening level
                if _is_stop_ext:
                    _extension_tight = self.inv * op.sub(self.relative_extreme, self.extreme[self.fst_data])
                    if _extension_tight < 0: #does happen in case of high volatility
                        _is_stop_ext = False
                    _extension_stop = _extension_tight * self.stop_tight_dict[self.stop_tight_ret][self.stop_ret_level]

            #Taking profit
            if self.exit_dict[self.exit_name][self.exit_ext_bool] & self.fif_op(_curent_value,_profit_value):
                self.is_entry = False
                self.trades_track_.iloc[-1, self.trades_track_.columns.get_loc(self.exit_row)] = self.curr_row
                self.trades_track_.iloc[-1, self.trades_track_.columns.get_loc(self.exit_level)] = \
                    _profit_value  # exit level
                self.trades_track_.iloc[-1, self.trades_track_.columns.get_loc(self.trade_return)] = \
                    self.inv * ((_entry_level - _profit_value) / _entry_level )
                break

            #Tightening the stop using extension
            if _is_stop_ext:
                if self.fst_op(_curent_value,_tight_trig):
                    if self.fst_op(self.series.loc[self.row_rel_extreme, _data_stop],self.stop_value):
                        self.stop_value = self.series.loc[self.row_rel_extreme, _data_stop]

            #Tightening using percentage reached
            if _is_stop_pour :
                if self.fst_op(_curent_value,_tight_pour_trig) & \
                        (self.fst_op(_tight_pour_level, self.stop_value)):
                    self.stop_value = _tight_pour_level

        if math.isnan(self.trades_track_.iloc[-1, self.trades_track_.columns.get_loc(self.exit_level)]):
            self.trades_track_ = self.trades_track_[:-1]

        return self.trades_track_

