import indicator as ind
import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import data_manip.input_dataframe as idf
import charting as cht

nb_data=100
date_debut='2007-01-20'
date_fin='2010-04-20'
asset="MSFT"

def main():
    pass

if __name__ == '__main__':
    main()

rg = lr.RegressionSlopeStrenght(nb_data=nb_data, asset=asset, date_debut=date_debut, date_fin=date_fin)
mk_ = mk.MannKendall(nb_data=nb_data, asset=asset, date_debut=date_debut, date_fin=date_fin)
indicators = {'slope': rg, 'r_square': rg, 'mk': mk_}
ind.Indicator.calcul_indicator(self, **indicators)
cht.Charting(**indicators).chart(series=self.series)