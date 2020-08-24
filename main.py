import indicator as ind
import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import data_manip.input_dataframe as idf
import charting as cht
import trading_rules as tr

nb_data=100
date_debut='2007-01-20'
date_fin='2008-01-20'
asset="MSFT"
r_square_level=.8


class Main(tr.TradingRules):

    def __init__(self):
        rg = lr.RegressionSlopeStrenght(nb_data=nb_data, asset=asset, date_debut=date_debut, date_fin=date_fin)
        mk_ = mk.MannKendall(nb_data=nb_data, asset=asset, date_debut=date_debut, date_fin=date_fin)
        self.indicator = {'slope': rg, 'r_square': rg, 'mk': mk_}
        super().__init__(nb_data=nb_data,date_debut=date_debut,date_fin=date_fin,
                         asset=asset,r_square_level=r_square_level,**self.indicator)

    def next_main(self):

        cht.Charting(**self.indicator).chart(r_square_level=r_square_level,series=self.series)

        t=5

if __name__ == '__main__':
    Main().next_main()


