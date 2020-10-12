import math_op as mo
import initialize as init
import operator as op
import math

class EntFibo(init.Initialize):

    
    def __init__(self):
        """
        Class that uses Fibonnacci strategy to enter the market


        Trying to enter the market with Fibonacci retracement and extension. 3 types:
            Retracement from the last wave
            Retracement from beginning of the trend
            Extension from a previous wave (largest one in the last trend)


        Notes
        -----

        No slippage included in `try_entry()`. If the price reached the desired level, we just exit at either the
            current price or the next desired price

        The system doesn't check on a shorter time frame if it reaches an entry point and a stop at the same time
            or even an exit point and stop at the same time (in case of high volatility) in `try_entry()`
            Taking into account the system, those are really rare cases. However it could be tested by using a
            shorter time every time an entry or exit signal

        """

        super().__init__()

        self.extreme = {}
        self.high="max"
        self.low="min"
        self.high_idx="max_idx"
        self.low_idx = "min_idx"
        self.fst_ext_cdt = False #by default first condition for extension is not met, set to False
    
    def __call__(self,curr_row,buy_signal=False,sell_signal=False):
        """
        Default function called to determine the entry level
        """

        #ENTRY TRACKER
        #----------------
        # Entry level, tells if the system has a position in the market, buy or sell signal

        self.curr_row=curr_row
        self.buy_signal=buy_signal
        self.sell_signal=sell_signal
        self.is_entry = False
        self.relative_extreme = None #last wave the system uses (relative low for buy, vice versa) as a
                                        # basis to calculate the profit taking price. It uses the default data (close)
                                          # to smooth data
        self.row_rel_extreme = 0

        self.first_data = self.curr_row - self.nb_data - self.buffer_extremum + 1
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
                                                     window=self.window, min_=self.low,max_=self.high)
        self.local_extremum_ = self.local_extremum_.reset_index(drop=True)

        self.largest_extension() #finding the largest extension used for potential entry and/or exit

        self.try_entry()
    
    def largest_extension(self):
        """
        Find largest extension (setback) from current trend (Fibonacci)
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

        for curr_row_ in range(len(self.local_extremum_)):

            #Sorten the name
            fst_val = self.local_extremum_.iloc[curr_row_, self.local_extremum_.columns.get_loc(fst_name)]
            sec_val = self.local_extremum_.iloc[curr_row_, self.local_extremum_.columns.get_loc(sec_name)]

            #If there are value to high and low, assign largest_extension_
            if (my_data[fst_data] != None) & (my_data[sec_data] != None):
                if math.isnan(sec_val) & (not math.isnan(my_data[fst_data])) & (not math.isnan(my_data[sec_data])):

                    if not hasattr(self,'largest_extension_'):
                        self.largest_extension_ = self.inv*(my_data[sec_data] - my_data[fst_data])

                    if (my_data[fst_data] != None) & (my_data[sec_data] != None) :
                        if op.ge(self.inv*(my_data[sec_data] - my_data[fst_data]), self.largest_extension_):
                            self.largest_extension_ = self.inv*(my_data[sec_data] - my_data[fst_data])

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
                continue

            if math.isnan(my_data[fst_data]):
                my_data[fst_data] = fst_val
                continue

            #If there is a valid first value, check if current value higher than recorded high (for buy), vice versa
            if not math.isnan(fst_val):
                if self.fst_op(fst_val, my_data[fst_data]):
                    my_data[fst_data] = fst_val
                continue

            if (my_data[sec_data] == None):
                my_data[sec_data] = sec_val
                continue

            if math.isnan(my_data[sec_data]):
                my_data[sec_data] = sec_val
                continue

            if not math.isnan(sec_val):
                if self.sec_op(sec_val, my_data[sec_data]):
                    my_data[sec_data] = sec_val
                continue
    
    def set_extremum(self):
        """
        Set the global max and min for the given range (from first_data to curr_row).

        """

        data_range = self.series.loc[self.first_data:self.curr_row,self.default_data]
        self.extreme = {self.high : data_range.max(),
                       self.low : data_range.min(),
                       self.high_idx : data_range.idxmax(),
                       self.low_idx : data_range.idxmin()
                       }

    
    def try_entry(self):
        """ Method that try entering in the market

        Function that will try to enter in the market :
                Until the system hit the desired extension and/or retracement. At the moment, only using extension (the
                    largest), which is `self.largest_extension_` set in function
                    `self.largest_extension()`. We can decide the proportion of the largest extension we want the system
                    to use in module `initialize.py` within dictionary `self.enter_dict{}` and variable `self.enter_ext`
                    (default value is 1)
                Stop trying to enter in the market when a condition is met.
                    At the moment, the only condition is when the price during a setback hits  a
                    percentage `self.fst_cdt_ext` (0.618 by default) of the largest extension `self.largest_extension_`
                    (low for a buy signal and high for a sell signal which is `self.entry`)
                    AND hits the minimum retracement in the other direction `self.sec_cdt_ext` (.882 by default)
                    Set true with this `self.bol_st_ext` in `initialize.py.


        NOTES
        -----
        Note that the system will priorise an entry over a new high or new low (to be more conservative). To solve
        this issue (rare cases, only with high volatility) :
            Check simulateneously if a new high or low is reached &  (if a buy/sell level is trigerred |
                market hits minimum required extension (if this condition is tested))
            Then, on a shorter timeframe, check if an entry | minimum required extension is reached before the
                market makes new low or high, vice versa

        The entry signal are based on extension at the moment. We could check if it true or false
        for different entry type

        If the price of the current row on which the signal is trigerred is below the buying level or above the
        selling level, the system just don't execute it and end it. CHECK THIS... Maybe the system could enter unless
        the price goes below the stop loss (buy) or above the stop loss (sell)

        At the moment, the system uses ONLY the extension to try to enter in the market. We may have to change a bit
        of the code if we want the flexibility of using other stuff



        """

        data_test = len(self.series) - self.curr_row - 1

        if self.is_entry:
            raise Exception('Already have an open position in the market...')

        for curr_row_ in range(data_test):

            #We may change that later if we decides to use other things than only the largest extension to enter in
            # the market. It checks if there is a "largest extension" set (in some case, there might not be)
            if not hasattr(self, 'largest_extension_'):
                break

            if self.enter_dict[self.enter_ext_name][self.enter_bool]:
                _entry_tentative = self.trd_op(self.extreme[self.fst_data],\
                                self.largest_extension_* self.enter_dict[self.enter_ext_name][self.enter_ext])

            #Test first if using Fibonacci extension as a signal to enter in the market.
            #Then the system first check if the price on the current row is below (for buy) or above (for sell signal)
            #If it is the case, the system just don't enter in the market.
            if self.enter_dict[self.enter_ext_name][self.enter_bool]:
                if (curr_row_ == 0) & self.fif_op(_entry_tentative, self.series.loc[self.curr_row,self.entry]):
                    self.is_entry = False
                    break

            self.curr_row += 1

            if self.relative_extreme == None:
                self.relative_extreme = self.series.loc[self.curr_row, self.default_data]
                self.row_rel_extreme = self.curr_row

            #Buy or sell signal (entry) with extension
            #   - Buy if current market price goes below our signal or equal
            #   - Sell if current market price goes above our signal or equal
            if self.enter_dict[self.enter_ext_name][self.enter_bool]:
                if self.six_op(self.series.loc[self.curr_row,self.entry],_entry_tentative):
                    self.is_entry = True
                    self.trades_track = self.trades_track.append({self.entry_row: self.curr_row,\
                                                                  self.entry_level:_entry_tentative},ignore_index=True)
                    self.relative_extreme = self.series.loc[self.curr_row,self.default_data]
                    self.row_rel_extreme = self.curr_row
                    break

            #Market hits the minimum required extension - first condition met (to stop trying entering the market)
            if self.bol_st_ext & self.six_op(self.series.loc[self.curr_row,self.entry], \
                        self.trd_op(self.extreme[self.fst_data],self.largest_extension_ * self.fst_cdt_ext)):
                if self.sec_op(self.series.loc[self.curr_row, self.default_data], self.relative_extreme):
                    self.relative_extreme = self.series.loc[self.curr_row, self.default_data]
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
                    print(f"The market hits previously the required {self.fst_cdt_ext} % of the largest extension"
                          f"and then retrace in the opposite direction of {self.sec_cdt_ext}")
                    break
                pass

            #Changing global low or high if current one is lower or higher
            if self.fst_op(self.series.loc[self.curr_row, self.default_data], self.extreme[self.fst_data]):
                self.extreme[self.fst_data] = self.series.loc[self.curr_row, self.default_data]
                self.extreme[self.fst_idx] = self.curr_row

        if self.is_entry & (op.gt(self.extreme[self.fst_idx]),self.row_rel_extreme):
            print("'Absolute' extremum is after relative extremum which doesn't work")