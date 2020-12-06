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

"""
Module for mathematical operation support
"""
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class MathOp():
    """
    Class to provide mathematical operation support
    """

    @classmethod
    def __init__(cls,series,default_col):
        cls.series = series
        cls.default_col=default_col

    @classmethod
    def local_extremum(cls,start_point,end_point,window = 6,min_= 'min',max_='max',index_ = 'index'):
        """ Function to find local extremum (min and max) on a Dataframe.

        It checks if the values for a number of points on each side (`window`) are greater or lesser and then
        determine the local extremum.

        Parameters
        ----------
        start_point : int
            the first data (index) to check in the Dataframe
        end_point : int
            the last data (index) to check in the Dataframe
        window : int
            the number of the data the method check before and after to determine the local extremum. Default is 6.
            Recommended values are between 5 and 7.
        min_ : str
            Name given to min data column
        max_ : str
            Name given to max data column

        Return
        ------
        DataFrame list : Return a pandas dataframe `cls.series` with the none empty min or max value
            (if both are empty, nothing is returned. If one of
            them has a value, return the local min or max with index no)
        """

        cls.series=cls.series.loc[start_point:end_point,cls.default_col]
        cls.series=pd.DataFrame({cls.default_col: cls.series})

        cls.series[min_] = cls.series.iloc[argrelextrema(cls.series.values, np.less_equal,
                                                          order=window)[0]][cls.default_col]
        cls.series[max_] = cls.series.iloc[argrelextrema(cls.series.values, np.greater_equal,
                                                          order=window)[0]][cls.default_col]
        cls.series[index_] = cls.series.index

        # Plot results - to get ride when the project is done. Only as a guideline at the moment

        """
        plt.scatter(cls.series.index, cls.series[min_], c='r')
        plt.scatter(cls.series.index, cls.series[max_], c='g')
        
        plt.plot(cls.series.index, cls.series[cls.default_col])
        plt.ion()
        plt.show()
        """

        #Filter nan value for min or max out
        cls.series=cls.series.loc[(cls.series[min_].isna())==False | (cls.series[max_].isna() == False)]

        return cls.series