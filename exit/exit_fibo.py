import entry.entry_fibo as ef


class ExitFibo(ef.EntFibo):

  
    def __init__(self,curr_row,buy_signal=False,sell_signal=False):

        """ Class that uses Fibonnacci strategy to exit the market.

        It first uses the EntFibo to enter the market (inheritance)
        Then it tries to exit the market with Fibonacci retracement and extension. 1 type at the moment:
            1- Extension from a previous wave (largest one in the last trend)


        Notes (Improvements to do)
        --------------------------

            - Need to use also Fibonnacci retracements to exit the market

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


        #If no entry signal, exit the function
        if not self.is_entry:
            return

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

        #Check if the first row (signal) is already below the stop loss (for buy) and vice versa for sell signal
        #If yes, just not entering in the market
        if self.is_tentative & self.exit_dict[self.exit_name][self.exit_ext_bool] & \
            self.six_op(self.series.loc[self.curr_row,self.stop],self.trd_op(self.extreme[self.fst_data],\
                            self.largest_extension_* self.exit_dict[self.exit_name][self.stop_ext])):

            self.is_entry = False
            return

        data_test = len(self.series) - self.curr_row - 1

        for curr_row_ in range(data_test):

            pass


            # Put self.entry to false if the system exit the market

        # define stop loss and taking profit first
        # using extension strategy to exit
        if self.exit_dict[self.exit_name][self.exit_ext_bool]:
            stop = self.trd_op(self.extreme[self.fst_data], \
                              self.exit_dict[self.exit_name][self.stop_ext] * self.largest_extension_)
            # exit_ =

        # HERE

        # if self.

        # Buy or sell signal (taking profit)
        #   - Buy if current market price goes below our signal or equal
        #   - Sell if current market price goes above our signal or equal

        if self.fif_op(self.trd_op(self.extreme[self.fst_data], self.largest_extension_), \
                      self.series.loc[self.curr_row, self.entry]):
            pass
        # break

        self.is_entry = False