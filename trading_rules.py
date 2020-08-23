import indicator as ind
import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk

nb_data=100
date_debut='2007-01-20'
date_fin='2010-04-20'
asset="MSFT"

#ind.Indicator
class TradingRules(ind.Indicator):

    def __init__(self):

        super().__init__(nb_data=nb_data,date_debut=date_debut,date_fin=date_fin,asset=asset)

        """
        self.nb_data=nb_data
        self.date_debut=date_debut
        self.date_fin=date_fin
        self.asset=asset
        """

        #self.Indicator = Indicator

    def _next(self):

        rg = lr.RegressionSlopeStrenght(nb_data=nb_data, asset=asset, date_debut=date_debut, date_fin=date_fin)
        mk_ = mk.MannKendall(nb_data=nb_data, asset=asset, date_debut=date_debut, date_fin=date_fin)
        indicators = {'slope': rg, 'r_square': rg, 'mk': mk_}
        odf = ind.Indicator(**indicators)
        odf.calcul_indicator()


TradingRules()._next()

