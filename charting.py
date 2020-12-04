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

""" Module with chart functions"""

import matplotlib.pyplot as plt

class Charting():

    @classmethod
    def __init__(cls, series, x_axis, y_axis,**indicator):
        cls.series = series
        cls.x_axis = x_axis  # x_axis name
        cls.y_axis = y_axis  # y_axis name

        cls.indicator = indicator
        cls.indicator_dict = {}
        count = len(cls.indicator)
        cls.divider = .25
        cls.height_chart = cls.divider * (count)

    @classmethod
    def chart_rsquare(cls, r_square_name, r_square_level=.8):
        """
        Marks the signals on a chart when r2 is above a certain level
        """

        # When r2 is higher than desired level, we have a mark on chart
        first_index = cls.series.first_valid_index()
        tempo_mark = []
        tempo_mark = cls.series.loc[cls.series[r_square_name] > r_square_level].index.tolist()
        cls.mark_ = [i - first_index for i in tempo_mark]

        def _plot(series_):
            """
            Nested function to plot series
            """

            # Main axe
            fig = plt.figure()
            fig.set_size_inches((40, 32))
            candle = fig.add_axes((0, cls.height_chart, 1, 0.5))

            count = 1
            for key, _ in cls.indicator.items():
                cls.indicator_dict[key] = fig.add_axes((0, cls.height_chart - cls.divider * count, 1, 0.2),
                                                       sharex=candle)
                count += 1

            candle.plot(cls.x_axis, cls.y_axis, markevery=cls.mark_, marker="o", data=series_)
            for key, _ in cls.indicator.items():
                cls.indicator_dict[key].plot(cls.x_axis, key, data=cls.series)

        _plot(cls.series)
        t = 5


    @classmethod
    def chart_marker(cls, marker_signal, marker_, color_mark, **marker):
        """
        Method to plot a chart with marker
        Parameters
        ----------
        **marker : keyword arguments
            contains the place we want mark, the color of the mark and the type of mark
        """

        cls.series.set_index(cls.x_axis, inplace=True)
        fig = plt.figure()

        plt.plot(cls.series.index, cls.y_axis, color='b', data=cls.series)
        for key, _ in marker.items():
            plt.plot(cls.series.index, cls.y_axis, markevery=marker[key][marker_signal], marker= \
                marker[key][marker_], markersize=10, markerfacecolor=marker[key][color_mark], data=cls.series)

        plt.plot(cls.series.index, cls.y_axis, color='b', data=cls.series)