import math_op as mo
import initialize as init
import operator as op

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

        PARAMS:
            - last_retracement is to say if we try to retrace from last wave
            - first_retracement is to say if we try to retrace from the beginning of the trend
            - extenstion is to say if we try to buy by extending largest setback from the trend
            - lenght_trend is to say how long we check for either global extremum or search for the largest
              setback/retracement (for extension). By default, it's 1.5 times the lenght of the nb_data we use as a
              parameter to test the indicator (so 50% more)
        """

        super().__init__(cls,class_method=True)
        cls.last_retracement = last_retracement
        cls.first_retracement = first_retracement
        cls.extension=extension
        cls.series=series

    @classmethod
    def __call__(cls,curr_row,buy_signal=False,sell_signal=False):
        """
        Default function to determine the entry point
        """

        cls.buy_signal = buy_signal
        cls.sell_signal = sell_signal
        cls.curr_row = curr_row

        cls.first_data = curr_row - cls.nb_data - cls.buffer_extremum + 1
        if cls.first_data < 0:
            cls.first_data = 0

        if buy_signal and sell_signal :
            raise Exception('Cannot have a buy and sell signal at the same time')

        cls.mo_ = mo.MathOp(series=cls.series, default_col=cls.default_data)

        cls.set_extremum()
        if cls.extension:
            cls.__set_extension()


    @classmethod
    def set_extremum(cls):

        data_range = cls.series.loc[cls.first_data:cls.curr_row,cls.default_data]
        cls.high = data_range.max()
        cls.low = data_range.min()
        cls.high_idx=data_range.idxmax()
        cls.low_idx = data_range.idxmin()


    @classmethod
    def __set_extension(cls):
        """
        Find largest extension from current trend
        """

        if cls.buy_signal:
            start_point=cls.low_idx
            string_operator=op.ge

        if cls.sell_signal:
            start_point=cls.high_idx
            string_operator=op.le

        local_extremum=cls.mo_.local_extremum(start_point=start_point, end_point=cls.curr_row, window=cls.window)

        for curr_row_ in range(len(local_extremum)):
            if cls.buy_signal:
                local_low = local_extremum.loc[curr_row_,cls.min]

            if cls.sell_signal:
                local_low = local_extremum.loc[curr_row_, cls.min]

    @classmethod
    def __extension(cls):

        pass

