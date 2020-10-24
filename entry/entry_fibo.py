import math_op as mo
import initialize as init
import operator as op
import math

class EntFibo():

    
    def __init__(cls):
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
        cls.extreme = {}
        cls.high="max"
        cls.low="min"
        cls.high_idx="max_idx"
        cls.low_idx = "min_idx"
        cls.fst_ext_cdt = False #by default first condition for extension is not met, set to False
        cls.is_entry = False
        cls.relative_extreme = None #last wave the system uses (relative low for buy, vice versa) as a
                                        # basis to calculate the profit taking price. It uses the default data (close)
                                          # to smooth data
        cls.row_rel_extreme = 0
        cls.largest_time = 0 #extension in time
        cls.index_name = 'index'

    
    def ent_fibo(cls,curr_row,buy_signal=False,sell_signal=False):
        """
        Default function called to determine the entry level
        """

        #ENTRY TRACKER
        #----------------
        # Entry level, tells if the system has a position in the market, buy or sell signal

        cls.curr_row=curr_row
        cls.buy_signal=buy_signal
        cls.sell_signal=sell_signal

        if (cls.largest_time != 0):
            raise Exception("Largest extension in term of times is not equal to 0 in __init__")

        cls.first_data = cls.curr_row - cls.nb_data + 1
        if cls.first_data < 0:
            cls.first_data = 0

        if cls.buy_signal and cls.sell_signal :
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
        cls.local_extremum_=cls.mo_.local_extremum(start_point=start_point, end_point=cls.curr_row, \
                                            window=cls.window, min_=cls.low,max_=cls.high,index_= cls.index_name)
        cls.local_extremum_ = cls.local_extremum_.reset_index(drop=True)

        cls.largest_extension() #finding the largest extension used for potential entry and/or exit
        cls.set_value()
        cls.try_entry()

    
    def largest_extension(cls):
        """
        Find largest extension (setback) from current trend (Fibonacci) in size + largest in time
        """

        if cls.buy_signal:
            my_data={}
            fst_data='curr_high'
            sec_data='curr_low'
            my_data[fst_data]=None
            my_data[sec_data] = None
            fst_name=cls.high
            sec_name=cls.low

        if cls.sell_signal:
            my_data={}
            fst_data='curr_low'
            sec_data='curr_high'
            my_data[fst_data]=None
            my_data[sec_data] = None
            fst_name=cls.low
            sec_name=cls.high

        trd_data = 'first_index'
        my_data[trd_data] = 0
        fth_data = 'sec_index'
        my_data[fth_data] = 0

        for curr_row_ in range(len(cls.local_extremum_)):

            #Sorten the name
            fst_val = cls.local_extremum_.iloc[curr_row_, cls.local_extremum_.columns.get_loc(fst_name)]
            sec_val = cls.local_extremum_.iloc[curr_row_, cls.local_extremum_.columns.get_loc(sec_name)]
            _current_index = cls.local_extremum_.iloc[curr_row_, cls.local_extremum_.columns.get_loc(cls.index_name)]

            #If there are value to high and low, assign largest_extension_
            if (my_data[fst_data] != None) & (my_data[sec_data] != None):
                if math.isnan(sec_val) & (not math.isnan(my_data[fst_data])) & (not math.isnan(my_data[sec_data])):

                    if not hasattr(cls,'largest_extension_'):
                        cls.largest_extension_ = cls.inv*(my_data[sec_data] - my_data[fst_data])

                    if (my_data[fst_data] != None) & (my_data[sec_data] != None) :
                        if op.ge(cls.inv*(my_data[sec_data] - my_data[fst_data]), cls.largest_extension_):
                            cls.largest_extension_ = cls.inv*(my_data[sec_data] - my_data[fst_data])

                    _ext_time = my_data[fth_data]- my_data[trd_data]
                    if (_ext_time>cls.largest_time):
                        cls.largest_time = _ext_time

                    my_data[fst_data] = None
                    my_data[sec_data] = None


            #It checks at the second last data, if there is a data for second_name (new relative high for sell
            # or new relative low for buy), it just basically don't check it, because it is not a real extension
            if curr_row_ == (len(cls.local_extremum_) -1):
                if not math.isnan(sec_val) & (curr_row_ == (len(cls.local_extremum_) -1 )):
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
                if cls.fst_op(fst_val, my_data[fst_data]):
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
                if cls.sec_op(sec_val, my_data[sec_data]):
                    my_data[sec_data] = sec_val
                    my_data[fth_data] = _current_index
                continue

    
    def set_extremum(cls):
        """
        Set the global max and min for the given range (from first_data to curr_row).

        """

        data_range = cls.series.loc[cls.first_data:cls.curr_row,cls.default_data]
        cls.extreme = {cls.high : data_range.max(),
                       cls.low : data_range.min(),
                       cls.high_idx : data_range.idxmax(),
                       cls.low_idx : data_range.idxmin()
                       }

    
    def set_value(cls):
        """
        Method to set some values that are used in class and sublcass
        """

        # extension level if condition in initialize.py is True
        if cls.exit_dict[cls.exit_name][cls.exit_ext_bool]:
            cls.extension_lost = cls.largest_extension_ * cls.exit_dict[cls.exit_name][cls.stop_ext]
            cls.extension_profit = cls.largest_extension_ * cls.exit_dict[cls.exit_name][cls.profit_ext]
            cls.stop_value = cls.trd_op(cls.extreme[cls.fst_data], cls.extension_lost)

            if cls.extension_lost < 0:
                raise Exception(
                    f"Houston, we've got a problem, Extension lost in enter_fibo.py is {cls.extension_lost} "
                    f"and should not be negative")
            if cls.extension_profit < 0:
                raise Exception(f"Houston, we've got a problem, Extension profit in enter_fibo.py is "
                                f"{cls.extension_profit} and should not be negative")

    
    def try_entry(cls):
        """
        Method that try entering in the market

        Function that will try to enter in the market :
                Until the system hit the desired extension and/or retracement. At the moment, only using extension (the
                    largest), which is `cls.largest_extension_` set in function
                    `cls.largest_extension()`. We can decide the proportion of the largest extension we want the system
                    to use in module `initialize.py` within dictionary `cls.enter_dict{}` and variable `cls.enter_ext`
                    (default value is 1)
                Stop trying to enter in the market when a condition is met.
                    At the moment, the only condition is when the price during a setback hits  a
                    percentage `cls.fst_cdt_ext` (0.618 by default) of the largest extension `cls.largest_extension_`
                    (low for a buy signal and high for a sell signal which is `cls.entry`)
                    AND hits the minimum retracement in the other direction `cls.sec_cdt_ext` (.882 by default)
                    Set true with this `cls.bol_st_ext` in `initialize.py.


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

        data_test = len(cls.series) - cls.curr_row - 1

        #Data used only in entry.fibo at the moment
        _largest_time = cls.largest_time * cls.enter_dict[cls.enter_time][cls.time_ext]
        _bool_time = cls.enter_dict[cls.enter_time][cls.enter_bool]
        _largest_ext = cls.largest_extension_ * cls.enter_dict[cls.enter_ext_name][cls.enter_ext]
        _bool_ext = cls.enter_dict[cls.enter_ext_name][cls.enter_bool]

        if cls.is_entry:
            raise Exception('Already have an open position in the market...')

        cls.set_value()

        for curr_row_ in range(data_test):

            #We may change that later if we decides to use other things than only the largest extension to enter in
            # the market. It checks if there is a "largest extension" set (in some case, there might not be)
            if not hasattr(cls, 'largest_extension_'):
                cls.is_entry = False
                print("Not any largest extension")
                break

            if _bool_ext:
                if _largest_ext < 0: #Can happens when the market moves really fast and not able to find
                                        # a `cls.largest_extension` that is positive
                    cls.is_entry = False
                    break
                _entry_tentative = cls.trd_op(cls.extreme[cls.fst_data], _largest_ext)

            #Test first if using Fibonacci extension as a signal to enter in the market.
            #Then the system first check if the price on the current row is below (for buy) or above (for sell signal)
            #If it is the case, the system just don't enter in the market.
            if cls.enter_dict[cls.enter_ext_name][cls.enter_bool]:
                if (curr_row_ == 0) & cls.fif_op(_entry_tentative, cls.series.loc[cls.curr_row,cls.entry]):
                    cls.is_entry = False
                    break

            cls.curr_row += 1

            _current_value = cls.series.loc[cls.curr_row, cls.default_data] #curent value with default data type
            _current_stop = cls.series.loc[cls.curr_row, cls.stop] #current stop value with data stop type
            _current_entry = cls.series.loc[cls.curr_row, cls.entry]

            if not hasattr(cls, 'stop_value'):
                cls.is_entry = False
                print("Not any stop_value")
                break

            if cls.relative_extreme == None:
                cls.relative_extreme = cls.series.loc[cls.curr_row, cls.default_data]
                cls.row_rel_extreme = cls.curr_row

            #Check if has to enter after a certain time only
            if _bool_time & (curr_row_ <_largest_time):
                # Retrace two quickly (in time) and went below (for a buy signal) the stop loss. Do not enter
                if cls.six_op(_current_stop, cls.stop_value):
                    cls.is_entry = False
                    break
                else :
                    continue

            #Buy or sell signal (entry) with extension
            #   - Buy if current market price goes below our signal or equal
            #   - Sell if current market price goes above our signal or equal
            if cls.enter_dict[cls.enter_ext_name][cls.enter_bool]:
                if cls.six_op(_current_entry,_entry_tentative):

                    #Check if current price is below (for buy) desired entry level after the minimum time. If yes,
                    #the market enters at the current price and not the desired
                    if _bool_time & (cls.curr_row == math.ceil(_largest_time)):
                        _entry_level = _current_entry
                    else :
                        _entry_level = _entry_tentative

                    cls.is_entry = True
                    cls.trades_track = cls.trades_track.append({cls.entry_row: cls.curr_row,\
                                                            cls.entry_level:_entry_level},ignore_index=True)

                    if cls.sec_op(_current_value, cls.relative_extreme):
                        cls.relative_extreme = _current_value
                        cls.row_rel_extreme = cls.curr_row
                    break

            #Market hits the minimum required extension - first condition met (to stop trying entering the market)
            if cls.bol_st_ext & cls.six_op(_current_entry, \
                        cls.trd_op(cls.extreme[cls.fst_data],cls.largest_extension_ * cls.fst_cdt_ext)):
                if cls.sec_op(_current_value, cls.relative_extreme):
                    cls.relative_extreme = _current_value
                    cls.row_rel_extreme = cls.curr_row
                cls.fst_ext_cdt = True
                continue

            # The system will stop trying to enter the market :
            #   - first condition (extension) is met. It hit the required
            #       % of the largest extension, previously (61.8% by default) - low for buy, high for sell
            #   - It went back then reached the minimum retracement in the other direction (88.2% by default)
            if cls.bol_st_ext & cls.fst_ext_cdt & (cls.relative_extreme != None) :
                if cls.fif_op(cls.series.loc[cls.curr_row,cls.default_data],cls.fth_op(cls.relative_extreme,\
                            cls.inv*(op.sub(cls.relative_extreme, cls.extreme[cls.fst_data])*cls.sec_cdt_ext))) :
                    print(f"The market hits previously the required {cls.fst_cdt_ext} % of the largest extension"
                          f"and then retrace in the opposite direction of {cls.sec_cdt_ext}")
                    cls.is_entry = False
                    break
                pass

            #Changing global low or high if current one is lower or higher
            if cls.fst_op(cls.series.loc[cls.curr_row, cls.default_data], cls.extreme[cls.fst_data]):
                cls.extreme[cls.fst_data] = cls.series.loc[cls.curr_row, cls.default_data]
                cls.extreme[cls.fst_idx] = cls.curr_row

                #Changing stop value
                if cls.exit_dict[cls.exit_name][cls.exit_ext_bool]:
                    cls.stop_value = cls.trd_op(cls.extreme[cls.fst_data], cls.extension_lost)