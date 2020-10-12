import entry.entry_fibo as ef
import sys

class ExitFibo(ef.EntFibo):

  
    def __init__(self):
        """
        Class that uses Fibonnacci strategy to exit the market.

        It first uses the EntFibo to enter the market (inheritance)
        Then it tries to exit the market with Fibonacci retracement and extension. 1 type at the moment:
            1- Extension from a previous wave (largest one in the last trend)


        Notes
        -----

        Need to use also Fibonnacci retracements to exit the market

        No slippage included in `try_exit()`. If the price reached the desired level, we just exit at either the
            current price or the next desired price

        """

        super().__init__()

    def __call__(self,curr_row,buy_signal=False,sell_signal=False):

        super().__call__(curr_row=curr_row, buy_signal=buy_signal, sell_signal=sell_signal)
        self.try_exit()
        #self.try_exit()


    def try_exit(self):
        """
        Method which try to exit the market.

        This method will make the system exit the market when a close or a stop loss signal is triggered

        Notes
        -----
        The stops may be tightened (see "stop tightening" in `initialize.py`)

        The system doesn't check on a shorter time frame if it reaches an exit point and a stop in `try_exit()`
            in case of high volatility. Really rare cases

        No slippage included in `try_exit()`. If the price reached the desired level, we just exit at either the
            current price.

        """

        #If no entry signal, exit the function
        if not self.is_entry:
            return

        __entry_level = self.trades_track.iloc[-1, self.trades_track.columns.get_loc(self.entry_level)]
        is_tightened = False #stop has been tightened

        # Changing global low or high if current one is lower or higher
        if self.fst_op(__current_value, self.extreme[self.fst_data]):
            self.extreme[self.fst_data] = __curent_value
            self.extreme[self.fst_idx] = self.curr_row

        #extension level if condition in initialize.py is True
        if self.exit_dict[self.exit_name][self.exit_ext_bool]:
            __extension_lost = self.largest_extension_ * self.exit_dict[self.exit_name][self.stop_ext]
            __extension_profit = self.largest_extension_ * self.exit_dict[self.exit_name][self.profit_ext]
            __stop_value = self.trd_op(self.extreme[self.fst_data], __extension_lost)

            if __extension_lost < 0:
                sys.exit(f"Houston, we've got a problem, Extension lost in exit_fibo.py is {__extension_lost}"
                         f"and should not be negative")
            if __extension_profit < 0:
                sys.exit(f"Houston, we've got a problem, Extension profit in exit_fibo.py is {__extension_profit}"
                         f"and should not be negative")

        #stop tightening using extension
        _is_stop_ext = self.stop_tight_dict[self.stop_tight_ret][self.is_true]
        if _is_stop_ext:
            _extension_tight =  self.inv * op.sub(self.relative_extreme,self.extreme[self.fst_data])
            if _extension_tight < 0:
                sys.exit("_extension tight cannot be negative")
            _extension_stop = _extension_tight * self.stop_tight_dict[self.stop_tight_ret][self.stop_ret_level]

            if self.stop_tight_dict[self.stop_tight_ret][self.default_data_]:
                _data_stop = self.default_data
            else :
                _data_stop = self.stop

        #Check if the first row (where the signal is trigerred) is already below the stop loss (for buy)
        # and vice versa for sell signal. If yes, just not entering in the market
        if self.exit_dict[self.exit_name][self.exit_ext_bool] & \
            self.six_op(self.series.loc[self.curr_row,self.stop],self.trd_op(self.extreme[self.fst_data],\
                                                                             __extension_lost)):
            self.is_entry = False
            return

        data_test = len(self.series) - self.curr_row - 1

        for curr_row_ in range(data_test):
            self.curr_row += 1
            __curent_value = self.series.loc[self.curr_row, self.default_data] #curent value with default data type
            __current_stop = self.series.loc[self.curr_row, self.stop] #current stop value with data stop type

            #Profit can change if relative_extreme changes
            if self.exit_dict[self.exit_name][self.exit_ext_bool]:
                __profit_value = self.fth_op(self.relative_extreme, __extension_profit)

            #Value that will make tighten the stop
            if _is_stop_ext:
                _tight_trig = self.fth_op(self.relative_extreme,_extension_stop)

            #Checking if stop is triggered
            if self.exit_dict[self.exit_name][self.exit_ext_bool] & \
                    self.six_op(__current_stop, __stop_value):
                self.is_entry = False

                self.trades_track.iloc[-1,self.trades_track.columns.get_loc(self.exit_row)] = self.curr_row
                self.trades_track.iloc[-1, self.trades_track.columns.get_loc(self.exit_level)] = \
                    __stop_value #exit level
                self.trades_track.iloc[-1, self.trades_track.columns.get_loc(self.trade_return)] = \
                    self.inv*((__entry_level-__stop_value)/__stop_value)

            #Changing relative low (for a buying), vice versa
            if self.sec_op(__curent_value, self.relative_extreme):
                self.relative_extreme = __curent_value
                self.row_rel_extreme = self.curr_row

                #Changing stop tightening level
                if _is_stop_ext:
                    _extension_tight = self.inv * op.sub(self.relative_extreme, self.extreme[self.fst_data])
                    if _extension_tight < 0:
                        sys.exit("_extension tight cannot be negative")
                    _extension_stop = _extension_tight * self.stop_tight_dict[self.stop_tight_ret][self.stop_ret_level]

            #Taking profit
            if self.exit_dict[self.exit_name][self.exit_ext_bool] & self.fif_op(__curent_value,__profit_value):
                self.is_entry = False
                self.trades_track.iloc[-1, self.trades_track.columns.get_loc(self.exit_row)] = self.curr_row
                self.trades_track.iloc[-1, self.trades_track.columns.get_loc(self.exit_level)] = \
                    __profit_value  # exit level
                self.trades_track.iloc[-1, self.trades_track.columns.get_loc(self.trade_return)] = \
                    self.inv * ((__entry_level - __profit_value) / __profit_value)

            #Tightening the stop using extension
            if _is_stop_ext & self.fst_op(__curent_value,_tight_trig):
                if sec_op(__stop_value,self.series.loc[self.row_rel_extreme, _data_stop]):
                    __stop_value = self.series.loc[self.row_rel_extreme, _data_stop]

        #return self.trades_track

