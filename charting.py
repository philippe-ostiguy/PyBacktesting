import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Charting():

    @classmethod
    def __init__(cls, series, column_price, series_test = None, column_date=0, **indicator):

        cls.indicator=indicator
        cls.indicator_dict = {}
        cls.series = series
        cls.series_test = series_test
        cls.column_price = column_price
        cls.column_date = column_date
        cls.date_name = cls.series.columns[cls.column_date]
        count = len(cls.indicator)
        cls.divider = .24
        cls.height_chart = cls.divider * (count)

    @classmethod
    def chart_rsquare(cls,r_square_name,r_square_level = .8):
        """
        Marks the signals on a chart when r2 is higher than a certain level
        """

        #When r2 is higher than desired level, we have a mark on chart
        first_index = cls.series_test.first_valid_index()
        tempo_mark=[]
        tempo_mark= cls.series_test.loc[cls.series_test[r_square_name] >r_square_level].index.tolist()
        cls.mark_= [i - first_index for i in tempo_mark]

        def _plot(series_):
            """
            Nested function to plot series
            """

            #Main axe
            fig = plt.figure()
            fig.set_size_inches((40, 32))
            candle = fig.add_axes((0, cls.height_chart, 1, 0.25))

            count = 1
            for key, _ in cls.indicator.items():
                cls.indicator_dict[key]=fig.add_axes((0, cls.height_chart-cls.divider*count, 1, 0.2), sharex=candle)
                count += 1

            candle.plot(cls.date_name, cls.column_price, markevery = cls.mark_, marker = "o", data = series_)
            for key, _ in cls.indicator.items():
                cls.indicator_dict[key].plot(cls.date_name, key, data = cls.series_test)

        _plot(cls.series_test)
        if not (cls.series[cls.column_price] == cls.series_test[cls.column_price]).all():
            _plot(cls.series)

    @classmethod
    def chart_marker(cls, marker_signal, marker_, color_mark, **marker):
        """
        Method to plot a chart with marker

        Parameters
        ----------
        **marker : keyword arguments
            contains the place we want mark, the color of the mark and the type of mark
        """
        cls.series.set_index(cls.date_name,inplace = True)
        fig = plt.figure()

        plt.plot(cls.series.index, cls.column_price, color ='b', data=cls.series)
        for key, _ in marker.items():
            plt.plot(cls.series.index, cls.column_price, markevery = marker[key][marker_signal],marker = \
            marker[key][marker_], markersize = 10, markerfacecolor = marker[key][color_mark], data=cls.series)

        plt.plot(cls.series.index,  cls.column_price, color ='b', data=cls.series)
