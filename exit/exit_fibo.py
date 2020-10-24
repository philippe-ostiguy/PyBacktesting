import entry.entry_fibo as ef
import sys
import operator as op

class ExitFibo(ef.EntFibo):

    
    def __init__(cls,init_):
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
        new_obj = init_
        cls.__dict__.update(new_obj.__dict__) #replacing cls object with Initialise object

    def __call__(cls,curr_row,buy_signal=False,sell_signal=False):

        super().__init__()
        cls.ent_fibo(curr_row=curr_row, buy_signal=buy_signal, sell_signal=sell_signal)
        return cls.try_exit()

    
    def try_exit(cls):
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
        if not cls.is_entry:
            return None

        _entry_level = cls.trades_track.iloc[-1, cls.trades_track.columns.get_loc(cls.entry_level)]

        #stop tightening using extension
        _is_stop_ext = cls.stop_tight_dict[cls.stop_tight_ret][cls.is_true]
        if _is_stop_ext:
            _extension_tight =  cls.inv * op.sub(cls.relative_extreme,cls.extreme[cls.fst_data])
            if _extension_tight < 0:
                _is_stop_ext = False #can happen in case of high volatility
            _extension_stop = _extension_tight * cls.stop_tight_dict[cls.stop_tight_ret][cls.stop_ret_level]

            if cls.stop_tight_dict[cls.stop_tight_ret][cls.default_data_]:
                _data_stop = cls.default_data
            else :
                _data_stop = cls.stop

        _is_stop_pour = cls.stop_tight_dict[cls.stop_tight_pour][cls.is_true]
        if _is_stop_pour :
            _tight_value = cls.stop_tight_dict[cls.stop_tight_pour][cls.tight_value]
            _pour_tight = cls.stop_tight_dict[cls.stop_tight_pour][cls.pour_tight]

    #Check if the first row (where the signal is trigerred) is already below the stop loss (for buy)
        # and vice versa for sell signal. If yes, stop loss trigerred
        if cls.exit_dict[cls.exit_name][cls.exit_ext_bool] & \
            cls.six_op(cls.series.loc[cls.curr_row,cls.stop],cls.stop_value):
            cls.is_entry = False
            cls.trades_track.iloc[-1, cls.trades_track.columns.get_loc(cls.exit_row)] = cls.curr_row
            cls.trades_track.iloc[-1, cls.trades_track.columns.get_loc(cls.exit_level)] = \
                cls.stop_value  # exit level
            cls.trades_track.iloc[-1, cls.trades_track.columns.get_loc(cls.trade_return)] = \
                cls.inv * ((_entry_level - cls.stop_value) / _entry_level)
            return cls.trades_track

        data_test = len(cls.series) - cls.curr_row - 1

        for curr_row_ in range(data_test):
            cls.curr_row += 1
            _curent_value = cls.series.loc[cls.curr_row, cls.default_data] #curent value with default data type
            _current_stop = cls.series.loc[cls.curr_row, cls.stop] #current stop value with data stop type

            #Profit can change if relative_extreme changes
            if cls.exit_dict[cls.exit_name][cls.exit_ext_bool]:
                _profit_value = cls.fth_op(cls.relative_extreme, cls.extension_profit)

            #Value that will make tighten the stop using extension
            if _is_stop_ext:
                _tight_trig = cls.fth_op(cls.relative_extreme,_extension_stop)

            # Value that will make tighten the stop using pourcentage
            if _is_stop_pour:
                _tight_pour_trig = _tight_value * (_profit_value - _entry_level) + _entry_level
                _tight_pour_level = _pour_tight *(_curent_value - _entry_level) + _entry_level

            #Stop loss trigerred?
            if cls.exit_dict[cls.exit_name][cls.exit_ext_bool] & \
                    cls.six_op(_current_stop, cls.stop_value):
                cls.is_entry = False
                cls.trades_track.iloc[-1,cls.trades_track.columns.get_loc(cls.exit_row)] = cls.curr_row
                cls.trades_track.iloc[-1, cls.trades_track.columns.get_loc(cls.exit_level)] = \
                    cls.stop_value #exit level
                cls.trades_track.iloc[-1, cls.trades_track.columns.get_loc(cls.trade_return)] = \
                    cls.inv*((_entry_level-cls.stop_value)/_entry_level)
                break

            #Changing relative low (for a buying), vice versa
            if cls.sec_op(_curent_value, cls.relative_extreme):
                cls.relative_extreme = _curent_value
                cls.row_rel_extreme = cls.curr_row

                #Changing stop tightening level
                if _is_stop_ext:
                    _extension_tight = cls.inv * op.sub(cls.relative_extreme, cls.extreme[cls.fst_data])
                    if _extension_tight < 0: #does happen in case of high volatility
                        _is_stop_ext = False
                    _extension_stop = _extension_tight * cls.stop_tight_dict[cls.stop_tight_ret][cls.stop_ret_level]

            #Taking profit
            if cls.exit_dict[cls.exit_name][cls.exit_ext_bool] & cls.fif_op(_curent_value,_profit_value):
                cls.is_entry = False
                cls.trades_track.iloc[-1, cls.trades_track.columns.get_loc(cls.exit_row)] = cls.curr_row
                cls.trades_track.iloc[-1, cls.trades_track.columns.get_loc(cls.exit_level)] = \
                    _profit_value  # exit level
                cls.trades_track.iloc[-1, cls.trades_track.columns.get_loc(cls.trade_return)] = \
                    cls.inv * ((_entry_level - _profit_value) / _entry_level )
                break

            #Tightening the stop using extension
            if _is_stop_ext:
                if cls.fst_op(_curent_value,_tight_trig):
                    if cls.fst_op(cls.series.loc[cls.row_rel_extreme, _data_stop],cls.stop_value):
                        cls.stop_value = cls.series.loc[cls.row_rel_extreme, _data_stop]

            #Tightening using percentage reached
            if _is_stop_pour :
                if cls.fst_op(_curent_value,_tight_pour_trig) & \
                        (cls.fst_op(_tight_pour_level, cls.stop_value)):
                    cls.stop_value = _tight_pour_level

        return cls.trades_track

