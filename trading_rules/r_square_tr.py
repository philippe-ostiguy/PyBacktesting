"""Module that detect buy and sell signal with r_square and if there is a trend"""

import indicator as ind
import entry.entry_fibo as enf
import exit.exit_fibo as exf
from math_op import MathOp as mo
import pandas as pd
import copy
import math

"""
Tell us if we should entry market. For now, it checked if r2 is above the desired level 
and then depending if the price's slope is negative or positive,
it trigers a signal to get long (slope is positive) or to get short (slope is negative)
"""

class RSquareTr(ind.Indicator):
    """Class that trigger entry signal based on r_square """

    def __init__(self):
        super().__init__()

    def __call__(self):

        """
        Take 2 key-word args : r2 level to triger a signal + minimum nb of data (self.min_data) between each
        signal before trigerring a new signal telling us to try to enter in the market. It gives the signal
        on each row (data), so we enter or exit in the market on the next row (data)
        """

        super().__call__()
        self.last_long = self.nb_data #last time we had a long signal
        self.last_short = self.nb_data  #last time we had a short signal
        self.trig_signal()

    def trig_signal(self):

        buy_signal = False
        sell_signal = False
        init_ = copy.deepcopy(self)

        for row in range(len(self.series)-self.nb_data+1):
            curr_row=row + self.nb_data-1

            mk_value=self.series.loc[curr_row, self.mk_key]
            r_value=self.series.loc[curr_row,self.r_square_key]
            #Buy signal
            if mk_value > 0 :
                if r_value > self.r_square_level:
                    if self.last_long >= self.min_data :
                        buy_signal = True
                        self.last_short = self.min_data
                        trades_track = exf.ExitFibo(init_).__call__(curr_row=curr_row,buy_signal=buy_signal)
                        self.trades_track = self.trades_track.append(trades_track,ignore_index = True)
                    self.last_long = 0

            #Sell signal
            if mk_value < 0 :
                if r_value > self.r_square_level:
                    self.last_short -= 1
                    if self.last_short >= self.min_data :
                        sell_signal=True
                        self.last_long = self.min_data
                        trades_track = exf.ExitFibo(init_).__call__(curr_row=curr_row,sell_signal=sell_signal)
                        self.trades_track = self.trades_track.append(trades_track,ignore_index = True)
                    self.last_short=0

            buy_signal = False
            sell_signal = False

            self.last_long += 1
            self.last_short += 1

        #Check if there is a row with no entry or exit signal
        del init_
        try:
            mo.nan_list(mo.pd_tolist(self.trades_track, self.entry_row))
        except:
            raise Exception("Nan value in entry row")

        try:
            mo.nan_list(mo.pd_tolist(self.trades_track, self.exit_row))
        except:
            raise Exception("Nan value in exit row")
