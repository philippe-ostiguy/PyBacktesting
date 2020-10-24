import matplotlib.pyplot as plt
import pandas as pd

class Charting():

    @classmethod
    def __init__(cls, series, column_price, series_test = None, column_date=0, **indicator):

        cls.indicator=indicator
        cls.indicator_dict = {}
        cls.series = series
        cls.series_test = series_test
        cls.column_price = column_price
        cls.column_date = column_date
        cls.date_name = cls.series_test.columns[cls.column_date]
        
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


