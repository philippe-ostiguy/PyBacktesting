import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import charting as cht
import trading_rules as tr



class Main(tr.RSquareTr):

    def __init__(self):

        super().__init__()
        super().calcul_indicator()
        super().indicator_signal()


    def next_main(self):

        cht.Charting(**self.indicator).chart(r_square_level=self.r_square_level,series=self.series)


if __name__ == '__main__':
    Main().next_main()


