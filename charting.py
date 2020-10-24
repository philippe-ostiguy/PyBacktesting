import matplotlib.pyplot as plt
import pandas as pd

class Charting():

    @classmethod
    def __init__(cls, r_square_name, series, series_test, column_price, column_date=0, r_square_level=.8, **indicator):

        cls.indicator=indicator
        cls.indicator_dict = {}
        cls.r_square_name = r_square_name
        cls.series = series
        cls.series_test = series_test
        cls.column_price = column_price
        cls.column_date = column_date
        cls.r_square_level = r_square_level
        cls.date_name = cls.series_test.columns[cls.column_date]
        
        count = len(cls.indicator)
        cls.divider = .24
        cls.height_chart = cls.divider * (count)

    @classmethod
    def chart_signal(cls):
        """
        Marks the signals on a chart
        """


        #When r2 is higher than desired level, we have a mark on chart
        first_index = cls.series_test.first_valid_index()
        tempo_mark=[]
        tempo_mark= cls.series_test.loc[cls.series_test[cls.r_square_name] >cls.r_square_level].index.tolist()
        cls.mark_= [i - first_index for i in tempo_mark]


        def _plot(series_):
            """
            Nested function to plot series
            """
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


