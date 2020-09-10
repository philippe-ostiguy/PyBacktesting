import math_op as mo
import initialize as init
import operator as op
import math

"""
Trying to enter the market with fibonacci retracement and extension. 3 types:
    1- Retracement from last wave
    2- Retracement from beginning of the trend
    3- Extension from a previous wave (largest one in the trend)

Basically, it will try to fin the peak from a trend if we are trying to buy (or a peak if we are trying to sell)
"""

class EntFibo(init.Initialize):

    @classmethod
    def __init__(cls,series,last_retracement = True, first_retracement = True, extension = True):

        """
        PARAMS
        ------
            - last_retracement is to say if we try to retrace from last wave
            - first_retracement is to say if we try to retrace from the beginning of the trend
            - extenstion is to say if we try to buy by extending largest setback from the trend
            - lenght_trend is to say how long we check for either global extremum or search for the largest
              setback/retracement (for extension). By default, it's 1.5 times the lenght of the nb_data we use as a
              parameter to test the indicator (so 50% more)

        NOTES
        ----
            - No slippage included in entry or exit. If the price reached the desired level, we just exit at either the
            current price or the next desired price
            - The system doesn't check on a sh

        """

        super().__init__(cls,class_method=True)
        cls.last_retracement = last_retracement
        cls.first_retracement = first_retracement
        cls.extension=extension
        cls.series=series
        cls.extreme = {}
        cls.high="high"
        cls.low="low"
        cls.high_idx="high_idx"
        cls.low_idx = "low_idx"


    @classmethod
    def __call__(cls,curr_row,buy_signal=False,sell_signal=False):
        """
        Default function to determine the entry point
        """

        cls.buy_signal = buy_signal
        cls.sell_signal = sell_signal
        cls.curr_row = curr_row
        cls.is_entry = False

        cls.first_data = curr_row - cls.nb_data - cls.buffer_extremum + 1
        if cls.first_data < 0:
            cls.first_data = 0

        if buy_signal and sell_signal :
            raise Exception('Cannot have a buy and sell signal at the same time')

        cls.set_extremum()

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

        cls.mo_ = mo.MathOp(series=cls.series, default_col=cls.default_data)
        cls.local_extremum_=cls.mo_.local_extremum(start_point=start_point, end_point=cls.curr_row, window=cls.window)

        if cls.extension:
            cls.largest_extension()

        cls.try_entry()


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
            if  my_data[fst_data] == None:
                my_data[fst_data] = cls.local_extremum_.iloc[curr_row_,cls.local_extremum_.columns.get_loc(fst_name)]
                curr_row_+=1
                continue

            if (math.isnan(my_data[fst_data]) \
                 | cls.fst_op(cls.local_extremum_.iloc[curr_row_,cls.local_extremum_.columns.get_loc(fst_name)], \
                          my_data[fst_data])) & (my_data[sec_data] == None):
                my_data[fst_data] = cls.local_extremum_.iloc[curr_row_,cls.local_extremum_.columns.get_loc(fst_name)]
                curr_row_+=1
                continue

            if my_data[sec_data] == None:
                my_data[sec_data] = cls.local_extremum_.iloc[curr_row_, cls.local_extremum_.columns.get_loc(sec_name)]
                curr_row_+=1
                if curr_row_ ==  len(cls.local_extremum_):
                    pass
                else:
                    continue

            if (math.isnan(my_data[sec_data])) \
                    | cls.sec_op(cls.local_extremum_.iloc[curr_row_,cls.local_extremum_.columns.get_loc(sec_name)], \
                         my_data[sec_data]):
                my_data[sec_data] = cls.local_extremum_.iloc[curr_row_, cls.local_extremum_.columns.get_loc(sec_name)]
                curr_row_+=1
                if curr_row_ ==  len(cls.local_extremum_):
                    pass
                else:
                    continue

            if not hasattr(cls,'largest_extension_'):
                cls.largest_extension_ = my_data[sec_data] - my_data[fst_data]
                my_data[fst_data] = None
                my_data[sec_data] = None
                continue

            if cls.sec_op((my_data[sec_data] - my_data[fst_data]), cls.largest_extension_):
                cls.largest_extension_ = my_data[sec_data] - my_data[fst_data]
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
        """
        PURPOSE
        -------
        Function that will try to enter in the market :
                - until we hit the desired extension and/or retracement
                - stop trying to enter in the market when a condition is met
                (Fibonnacci extension 0.618% of largest past extension)

        """



        data_test = len(cls.series)-cls.curr_row-1
        new_extreme = False

        for curr_row_ in range(data_test):

            if cls.buy_signal:
                pass

            if cls.sell_signal:
                pass

            #Changing global low or high if current one is lower or higher
            cls.curr_row += 1

            if cls.fst_op(cls.series.loc[curr_idx, cls.default_data], cls.extreme[cls.fst_data]):

                #The system will stop trying to enter in the market :
                #   - market made a new low or high +
                #   - hit a required % of the largest extension, previously (61.8% by default)
                if cls.fst_ext_cdt :
                    print("The market made a new low or high and it hits previously \
                    the required % of the largest extension")
                    break

                cls.extreme[cls.fst_data] = cls.series.loc[cls.curr_row, cls.default_data]
                cls.extreme[cls.fst_idx] = cls.curr_row
                new_extreme = True

            #Buy or sell signal (entry)
            #   - Buy if current market price goes below our signal
            #   - Sell if current market price goe above our signal

            if cls.fif_op(cls.trd_op(cls.extreme[cls.fst_data],cls.largest_extension_),\
                          cls.series.loc[cls.curr_row,cls.entry]):

                cls.is_entry = True
                break

            #Market hit the minimum required extension - first condition met (point to enter in the market)
            if not new_extreme & cls.fif_op(cls.trd_op(cls.extreme[cls.fst_data], \
                        cls.largest_extension_ * cls.cdt_ext), cls.series.loc[cls.curr_row,cls.entry]):

                cls.fst_ext_cdt = True
                continue



            new_extreme = False
