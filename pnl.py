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

"""Module to assess the trading strategy performance"""

import trading_rules as tr
import numpy as np
import math
from date_manip import DateManip

class PnL(tr.RSquareTr):

    def __init__(self):
        super().__init__()

    def pnl_(self):
        """Function that calculate the different metrics to evalute the trading strategy performance"""
        super().__call__()
        self.diff_ = ((self.end_date - self.start_date).days / 365) #diff in term of year with decimal
        self.pnl_dict[self.range_date_] = self.range_date()
        self.pnl_dict[self.ann_return_] = self.ann_return()
        self.pnl_dict[self.ann_vol_] = self.ann_vol()
        self.pnl_dict[self.sharpe_ratio_] = self.sharpe_ratio()
        self.pnl_dict[self.max_draw_] = self.max_draw()
        self.pnl_dict[self.pour_win_] = self.pour_win()
        self.pnl_dict[self.nb_trades_] = self.nb_trades()

        #Possible to have some trades but not real trades (0 return) when largest_extension is 0
        if (self.pnl_dict[self.nb_trades_] != None):
            if (self.pnl_dict[self.nb_trades_] > 0):
                if self.pnl_dict[self.sharpe_ratio_] is None or math.isnan(self.pnl_dict[self.sharpe_ratio_]):
                    self.pnl_dict = {}

    def annualized_(func):
        """Decorator to return annualized value"""
        def wrap_diff(self):
            return ((1+func(self))**(1/self.diff_)-1)
        return wrap_diff

    @annualized_
    def ann_return(self):
        """Calculate the annualized return"""
        return_ = 0
        for index_ in self.trades_track.index:
            return_ = (1+return_)*(1+self.trades_track.loc[index_,self.trade_return]) - 1
        return return_

    def ann_vol(self):
        """Calculate annualized vol
        """

        vol_ = self.trades_track[self.trade_return].std()
        if not np.isnan(vol_):
            return (vol_ *  math.sqrt(1/self.diff_))
        else :
            return None

    def sharpe_ratio(self):
        """Sharpe ratio

        Not using the risk-free rate has it doesn't change the final result. We could trade on margin and just
        totally distort the return. Also, depending on the time intervals, the return are larger or smaller
        (expected higher volatility on daily than hourly basis).
        """
        if not bool(self.pnl_dict):
            return None

        if self.pnl_dict[self.ann_vol_] == None:
            return None

        elif ((self.pnl_dict[self.ann_vol_] == 0) | np.isnan(self.pnl_dict[self.ann_vol_])):
            return None
        else :
            return (self.pnl_dict[self.ann_return_] /self.pnl_dict[self.ann_vol_])

    def max_draw(self):
        """Return lowest return value """

        return self.trades_track[self.trade_return].min()

    def nb_trades(self):
        """Return the number of trades"""
        return self.trades_track.shape[0]

    def range_date(self):
        """ Return the range date tested in a desired format

        Using "%Y-%m-%d" as Timestamp format
        """
        dm_begin_ = DateManip(self.start_date).end_format(self.end_format_)
        dm_end_ = DateManip(self.end_date).end_format(self.end_format_)
        return f"{dm_begin_} to {dm_end_}"

    def pour_win(self):
        """Return the percentage of winning trades
        """

        total_trade = self.nb_trades()
        pour_win_ = self.trades_track[self.trades_track[self.trade_return] >= 0].shape[0]
        return 0 if total_trade == 0 else (pour_win_ / total_trade)