import matplotlib.pyplot as plt
import pandas as pd
import initialize as init

class Charting():

    @classmethod
    def __init__(cls, series, column_price, series_test = None, column_date=0, **indicator):

        cls.indicator=indicator
        cls.indicator_dict = {}
        cls.series = series
        cls.series_test = series_test
        cls.column_price = column_price
        cls.column_date = column_date
        if series_test != None:
            cls.date_name = series_test.columns[cls.column_date]
        
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
    def chart_marker(cls, marker_name = 'Default', **marker):
        """
        Method to plot a chart with marker
        """
        fig = plt.figure()
        candle.plot(cls.date_name, cls.column_price, markevery=marker, marker="o", data=cls.series)

        for key, _ in cls.marker.items():
            candle.plot(cls.date_name, cls.column_price, markevery=marker, marker="o", data=cls.series)

            cls.indicator_dict[key] = fig.add_axes((0, cls.height_chart - cls.divider * count, 1, 0.2), sharex=candle)
            count += 1



init_ = init.Initialize()

init_.trades_track = init_.trades_track.append({init_.entry_row: 5,
                                              init_.exit_row: 10}, ignore_index=True)



mark_up = init_.trades_track.loc[init_.entry_row].index.tolist()
mark_down = init_.trades_track.loc[init_.exit_row].index.tolist()

test =  {'marker_entry':{init_.marker_name : '^',init_.color_mark : 'g',init_.marker_entry : mark_up},
         'marker_exit':{init_.marker_name : 'v',init_.color_mark : 'r',init_.marker_exit : mark_down}}


cht_ = Charting(init_.series,init_.default_data).chart_marker(init_.trades_track, marker_name=init_.marker_name,**test)
t = 5