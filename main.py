import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import charting as cht
import trading_rules as tr

nb_data=100
date_debut='2005-01-20'
date_fin='2008-01-20'
asset="MSFT"


class ParamsIndicators():
    """
    Class to define the values of the indicator's parameters
    """
    value = {'r_square_value': .8, 'min_data': 100}

class Main(tr.RSquareTr):

    def __init__(self):
        rg = lr.RegressionSlopeStrenght(nb_data=nb_data, asset=asset, date_debut=date_debut, date_fin=date_fin)
        mk_ = mk.MannKendall(nb_data=nb_data, asset=asset, date_debut=date_debut, date_fin=date_fin)
        self.indicator = {'slope': rg, 'r_square': rg, 'mk': mk_}

        super().__init__(nb_data=nb_data,date_debut=date_debut,date_fin=date_fin,
                         asset=asset)
        super().calcul_indicator(**self.indicator)
        super().indicator_signal(**ParamsIndicators.value)


    def next_main(self):

        cht.Charting(**self.indicator).chart(r_square_level=r_square_level,series=self.series)
        t=5


if __name__ == '__main__':
    Main().next_main()


