import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import charting as cht
import pandas as pd
import pnl

class Main(pnl.PnL):

    def __init__(self):
        super().__init__()
        super().__call__()

    def next_main(self):

        cht.Charting(self.series,self.default_data, series_test=self.series_test,**self.indicator).\
            chart_rsquare(list(self.indicator.keys())[1],r_square_level=self.r_square_level)
        t = 5

if __name__ == '__main__':

    Main().next_main()
    t=5