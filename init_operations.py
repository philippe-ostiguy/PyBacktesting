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

"""Module to easily reinitiliaze values when needed """

from initialize import Initialize
from manip_data import ManipData as md
import pandas as pd

class InitOp(Initialize):

    def __init__(self):
        super().__init__()
        super().__call__()

    def __call__(self):
        self.reset_value()

    def reset_value(self):
        """Function to reset the dictionary that contains the trading journal (entry, exit, return) in
        `self.trades_track`

         We need to do that when we optimize, ie when `self.is_walkfoward` is `True`

         """

        self.trades_track = pd.DataFrame(columns=[self.entry_row, self.entry_level, self.exit_row, self.exit_level, \
                                                  self.trade_return])

    def init_series(self):
        """Function that extract the data from csv to a pandas Dataframe `self.series`

        It actually is the data that we are using for the strategy """

        self.series = md.csv_to_pandas(self.date_name, self.start_date, self.end_date, self.name, self.directory,
                            self.asset, ordinal_name=self.date_ordinal_name, is_fx=self.is_fx, dup_col = self.dup_col)

        """
        if self.is_detrend:
            self.series_test = md.de_trend(self.series,self.period, self.p_value,self.date_name,
                                           self.date_ordinal_name,self.default_data)
        else :
            self.series_test = self.series.copy()
        """