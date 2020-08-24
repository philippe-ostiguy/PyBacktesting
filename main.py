import indicator as ind
import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import data_manip.input_dataframe as idf
import charting as cht
from trading_rules import TradingRules

nb_data=100
date_debut='2007-01-20'
date_fin='2008-01-20'
asset="MSFT"
r_square_level=.8
indicators = {'slope': rg, 'r_square': rg, 'mk': mk_}

def main():
    rg = lr.RegressionSlopeStrenght(nb_data=nb_data, asset=asset, date_debut=date_debut, date_fin=date_fin)
    mk_ = mk.MannKendall(nb_data=nb_data, asset=asset, date_debut=date_debut, date_fin=date_fin)
    ind_=ind.Indicator(**indicators,nb_data=nb_data, asset=asset, date_debut=date_debut, date_fin=date_fin)
    series= ind_.calcul_indicator()
    cht.Charting(**indicators).chart(r_square_level=r_square_level,series=series)
    tr = TradingRules(nb_data=nb_data, asset=asset, date_debut=date_debut,
                      date_fin=date_fin, r_square_level=r_square_level)
    t=5

if __name__ == '__main__':
    main()

