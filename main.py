import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import charting as cht
import trading_rules as tr
import pandas as pd


class Main(tr.RSquareTr):

    def __init__(self):

        super().__init__()
        self.calcul_indicator()
        self.signal_trig()

    def next_main(self):

        cht.Charting(list(self.indicator.keys())[1],self.series,self.series_test,self.default_data,
                     r_square_level=self.r_square_level, **self.indicator).chart_()

if __name__ == '__main__':

    Main().next_main()
    t=5