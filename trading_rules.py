import indicator as ind

nb_data=100
date_debut='2007-01-20'
date_fin='2010-04-20'
asset="MSFT"

class TradingRules(ind.Indicator):

    def __int__(self,**Indicator):
        super().__init__()
        self.nb_data=nb_data
        self.date_debut=date_debut
        self.date_fin=date_fin
        self.asset=asset
        self.series=self.ordinal_date()
        self.Indicator = Indicator


    def next(self):
        print(self.point_data)

tr=TradingRules()
tr.next()

"""
rg=lr.RegressionSlopeStrenght(nb_data=nb_data,asset=asset,date_debut=date_debut,date_fin=date_fin)
mk_=mk.MannKendall(nb_data=nb_data,asset=asset,date_debut=date_debut,date_fin=date_fin)
indicators={'slope':rg,'r_square':rg,'mk':mk_}
odf= Indicator(**indicators)
odf.next()
"""