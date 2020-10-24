import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import charting as cht
import trading_rules as tr
import pandas as pd


class Main(tr.RSquareTr):

    def __init__(self):

        super().__init__()

    def next_main(self):

        self.calcul_indicator()
        self.signal_trig()
        cht.Charting(self.series,self.default_data, series_test=self.series_test,**self.indicator).\
            chart_rsquare(list(self.indicator.keys())[1],r_square_level=self.r_square_level)

if __name__ == '__main__':

    Main().next_main()
    t=5