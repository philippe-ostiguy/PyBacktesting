import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import charting as cht
import trading_rules as tr


class Main(tr.RSquareTr):

    def __init__(self):

        super().__init__()
        super().calcul_indicator()
        super().signal_trig()

    def next_main(self):

        cht.Charting(**self.indicator).chart(r_square_name=list(self.indicator.keys())[1],
                                             column_price=self.default_data,series=self.series,
                                             r_square_level=self.r_square_level )

if __name__ == '__main__':
    Main().next_main()
    t=5