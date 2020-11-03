import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import charting as cht
import pandas as pd
from optimize_ import Optimize
from math_op import MathOp as mo

class Main(Optimize):

    def __init__(self):
        super().__init__()
        super().__call__()
        self.cht_ = cht.Charting(self.series, self.date_name,
                                 self.default_data, series_test=self.series_test, **self.indicator)
        t = 5
    def chart_signal(self):
        """Marks signal on chart"""
        self.cht_.chart_rsquare(list(self.indicator.keys())[1],r_square_level=self.r_square_level)

    def chart_trigger(self):
        """Marks entry and exit level on chart"""

        mark_up = mo.pd_tolist(self.trades_track, self.entry_row)
        mark_down = mo.pd_tolist(self.trades_track, self.exit_row)
        marks_ = {'marker_entry': {self.marker_: '^', self.color_mark: 'g', self.marker_signal: mark_up},
                'marker_exit': {self.marker_: 'v', self.color_mark: 'r', self.marker_signal: mark_down}}

        self.cht_.chart_marker(self.marker_signal, self.marker_, self.color_mark,**marks_)
        t = 5

if __name__ == '__main__':
    main_ = Main()
    #main_.chart_signal()
    #main_.chart_trigger()

