import entry.entry_fibo as ef


class ExitFibo(ef.EntFibo):

    @classmethod
    def __init__(cls):

        """ Class that uses Fibonnacci strategy to exit the market.

        It first uses the EntFibo to enter the market (inheritance)
        Then it tries to exit the market with Fibonacci retracement and extension. 1 type at the moment:
            1- Extension from a previous wave (largest one in the last trend)


        Notes (Improvements to do)
        --------------------------

            - Need to use also Fibonnacci retracements to exit the market

        """

        super().__init__()

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

        # Put cls.entry to false if the system exit the market

        # define stop loss and taking profit first
        # using extension strategy to exit
        if cls.exit_dict[cls.exit_ext_name][cls.exit_bool]:
            stop = cls.trd_op(cls.extreme[cls.fst_data], \
                              cls.exit_dict[cls.exit_ext_name][cls.stop_ext] * cls.largest_extension_)
            # exit_ =

        # HERE

        # if cls.

        # Buy or sell signal (taking profit)
        #   - Buy if current market price goes below our signal or equal
        #   - Sell if current market price goes above our signal or equal

        if cls.fif_op(cls.trd_op(cls.extreme[cls.fst_data], cls.largest_extension_), \
                      cls.series.loc[cls.curr_row, cls.entry]):
            pass
        # break

        cls.is_entry = False