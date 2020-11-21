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

"""Module to run the program - use optimization tools if desired"""

from pnl import PnL
from manip_data import ManipData as md
from date_manip import DateManip as dm
from optimize.genetic_algorithm import GenAlgo as ga

class Optimize(PnL):

    def __init__(self):
        """Function that initializes stuff.

        It resets the `self.series` with `self.init_series()` and dictionary that track the pnl
        `self.trades_track` with `reset_value()` when we optimize.
        """
        super().__init__()
        self.init_series()
        self.reset_value()
        self.params = {}

    def __call__(self):
        """Function do different things dependent if we optimize or not"""

        if self.is_walkfoward:
            self.walk_foward()
        else :
            self.calcul_indicator()
            self.pnl_()
            md.write_csv_(self.dir_output, self.name_out, add_doc="", is_walkfoward=self.is_walkfoward, **self.pnl_dict)

    def walk_foward(self):
        """Function that do the walk-foward analysis (optimization).

        First it runs through the divided period (1 period interval for training and testing). We have to choose
        properly `self.start_date` and `self.end_date` as they set the numbers of period.

        Then the program runs through each training and testing period (in `self.dict_name_`). The program optimizes
        only in the training period `self.training_name_`. The results are store in the folder results and
        results_training for the training period and results_test for the testing period.

        Parameters
        ----------
        `self.start_date` : datetime object
            Set in `initialize.py`. Beginning date of training and testing.
        `self.end_date` : datetime object
            Set in `initialize.py`. End date of training and testing.

        """

        md_ = md

        _first_time = True
        self.dict_date_ = dm.date_dict(self.start_date, self.end_date,
                                       **self.dict_name_)

        if (len(self.dict_date_)) == 0:
            raise Exception("Total period not long enough for optimization")

        for key,_ in self.dict_date_.items():
            for key_, _ in self.dict_name_.items():
                self.start_date = self.dict_date_[key][key_][0]
                self.end_date = self.dict_date_[key][key_][1]
                if _first_time :
                    md_(self.dir_output,self.name_out,extension = key_).erase_content()
                self.init_series()
                self.calcul_indicator()
                if key_ == self.training_name_: #we only optimize for the training period
                    self.optimize_param()
                    self.pnl_dict,self.params = ga(self).__call__()
                else : #test period, we use the optimized parameters in the training period
                    self.assign_value()
                    self.pnl_()

                md.write_csv_(self.dir_output, self.name_out, add_doc=key_,
                              is_walkfoward=self.is_walkfoward, **self.pnl_dict)
                md.write_csv_(self.dir_output, self.name_out, add_doc=key_,
                              is_walkfoward=self.is_walkfoward, **self.params)

            _first_time = False

    def assign_value(self):
        """ Function to assign the value to each optimized parameters obtained in the optimization module.

        The `genetic_algorithm.py` return the dictionary with the value and when we test in `r_square_tr.py` they are
        in a different format"""

        for item in range(len(self.op_param)):
            if len(self.op_param[item]) > 1:
                self.op_param[item][0][self.op_param[item][1]] = self.params[self.op_param[item][1]]
            else:
                setattr(self, self.op_param[item][0], self.params[self.op_param[item][0]])