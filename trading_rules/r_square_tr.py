#!/usr/local/bin/env python3.7
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
#  The MIT License (MIT)
#  Copyright (c) 2020 Philippe Ostiguy
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
###############################################################################

"""Module that detect buy and sell signal with r_square and mk (Mann Kendall)"""

import indicator as ind
import exit.exit_fibo as exf
from math_op import MathOp as mo
from manip_data import ManipData as md
import pandas as pd
import copy


class RSquareTr(ind.Indicator):
    """Class that trigger entry signal based on r_square and Menn Kendall

    The signal is trigggered if `r_value` is above `self.r_square_level` define in `initialize.py` and if `mk_`value
    is 1 (buying signal) or -1 (selling signal)"""

    def __init__(self):
        super().__init__()

    def __call__(self):
        super().__call__()
        self.last_long = self.nb_data #last time we had a long signal
        self.last_short = self.nb_data  #last time we had a short signal
        self.trig_signal()

    def trig_signal(self):
        """Function that iterates through each data of the selected serie `self.series` to check if there is a
        signal.

        `mk_value` and `r_value` are the evaluated value to check if there is a signal. When there is a signal in a
        direction, the system needs to run through a minimum of `self.min_data` (defines or optimize in `initialize.py`)
        to enter in the market in the same direction.

        The function call the `exit_fibo.py` module anytime there is a signal which will then try to enter and exit the
        market. It could be set to another entry and exit types.

        Parameters
        ----------
        `self.r_square_level` : float
            If the current r2 is above this level, it means we have a trend. Important to set the good level, because
            it's one of the conditions that trigger a signal. It's set in `initialize.py`
        `self.min_data` : int
            If there is a signal, it's the minimum number of data needed before it can trigger another signal
            in the same direction

        Return
        ------
        The function doesn't return anything in itself, but it stores the trading entry and exit in dictionary
        `self.trades_track`
        """


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
            md.nan_list(md.pd_tolist(self.trades_track, self.entry_row))
        except:
            raise Exception("Nan value in entry row")

        try:
            md.nan_list(md.pd_tolist(self.trades_track, self.exit_row))
        except:
            raise Exception("Nan value in exit row")
