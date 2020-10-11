import entry.entry_fibo as ef

class ExitFibo(ef.EntFibo):

  
    def __init__(self,curr_row,buy_signal=False,sell_signal=False):
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
        super().__call__(curr_row=curr_row,buy_signal=buy_signal,sell_signal=sell_signal)


    def __call__(self):

        # EXIT TRACKER
        # ----------------
        # Entry level, tells if the system has a position in the market, buy or sell signal
        self.price_exit = 0
        self.try_exit()

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

        #extension level if condition in initialize.py is True
        if self.exit_dict[self.exit_name][self.exit_ext_bool]:
            __extension = self.largest_extension_ * self.exit_dict[self.exit_name][self.stop_ext]
            if __extension < 0:
                print(f"Houston, we've got a problem, Extension value in exit_fibo.py is {__extension} \
                and should not be negative")

        #Check if the first row (where the signal is trigerred) is already below the stop loss (for buy)
        # and vice versa for sell signal. If yes, just not entering in the market
        if self.exit_dict[self.exit_name][self.exit_ext_bool] & \
            self.six_op(self.series.loc[self.curr_row,self.stop],self.trd_op(self.extreme[self.fst_data], __extension)):
            self.is_entry = False
            return

        data_test = len(self.series) - self.curr_row - 1

        for curr_row_ in range(data_test):
            self.curr_row += 1
            __curent_value = self.series.loc[self.curr_row, self.default_data] #curent value with default data type
            __entry_level = self.trades_track.iloc[-1,self.trades_track.columns.get_loc(self.entry_level)]

            if self.exit_dict[self.exit_name][self.exit_ext_bool]:
                __stop_value = self.trd_op(self.extreme[self.fst_data], __extension)

            #First check if price is below a stop (for a buy signal)
            if self.exit_dict[self.exit_name][self.exit_ext_bool] & \
                    self.six_op(self.series.loc[self.curr_row, self.stop],
                                self.trd_op(self.extreme[self.fst_data], __extension)):

                self.is_entry = False

                self.trades_track.iloc[-1,self.trades_track.columns.get_loc(self.exit_row)] = self.curr_row
                self.trades_track.iloc[-1, self.trades_track.columns.get_loc(self.exit_level)] = \
                    __stop_value #exit level
                self.trades_track.iloc[-1, self.trades_track.columns.get_loc(self.trade_return)] = \
                    self.inv*((__entry_level-__stop_value)/__stop_value)

            #Changing global low or high if current one is lower or higher
            if self.fst_op(__current_value, self.extreme[self.fst_data]):
                self.extreme[self.fst_data] = __curent_value
                self.extreme[self.fst_idx] = self.curr_row

            #Changing relative low (for a buying), vice versa
            if self.sec_op(__curent_value, self.relative_extreme):
                self.relative_extreme = __curent_value




            """
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
            """

            if self.enter_dict[self.enter_ext_name][self.enter_bool]:


                pass


            # Put self.entry to false if the system exit the market

        # define stop loss and taking profit first
        # using extension strategy to exit
        if self.exit_dict[self.exit_name][self.exit_ext_bool]:
            stop = self.trd_op(self.extreme[self.fst_data], \
                              self.exit_dict[self.exit_name][self.stop_ext] * self.largest_extension_)
            # exit_ =



        # if self.

        # Buy or sell signal (taking profit)
        #   - Buy if current market price goes below our signal or equal
        #   - Sell if current market price goes above our signal or equal

        if self.fif_op(self.trd_op(self.extreme[self.fst_data], self.largest_extension_), \
                      self.series.loc[self.curr_row, self.entry]):
            pass
        # break

        self.is_entry = False