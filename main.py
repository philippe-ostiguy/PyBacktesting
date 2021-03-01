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

""" This is the main module which execute the program """

import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import charting as cht
import pandas as pd
from optimize_ import Optimize
from manip_data import ManipData as md

class Main(Optimize):

    def __init__(self):
        super().__init__()
        super().__call__()
        self.cht_ = cht.Charting(self.series, self.date_name,
                                 self.default_data, **self.indicator)

    def chart_signal(self):
        """Marks signal on chart (no entry, only when the indicators trigger a signal)"""
        self.cht_.chart_rsquare(list(self.indicator.keys())[0],r_square_level=self.r_square_level)

    def chart_trigger(self):
        """Marks entry and exit level on chart"""

        mark_up = md.pd_tolist(self.trades_track, self.entry_row)
        mark_down = md.pd_tolist(self.trades_track, self.exit_row)
        marks_ = {'marker_entry': {self.marker_: '^', self.color_mark: 'g', self.marker_signal: mark_up},
                'marker_exit': {self.marker_: 'v', self.color_mark: 'r', self.marker_signal: mark_down}}

        self.cht_.chart_marker(self.marker_signal, self.marker_, self.color_mark,**marks_)

if __name__ == '__main__':
    main_ = Main()
    #main_.chart_signal()
    main_.chart_trigger()
    t= 5