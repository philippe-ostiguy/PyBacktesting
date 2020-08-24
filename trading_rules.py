import indicator as ind
import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import data_manip.input_dataframe as idf
import charting as cht

"""
Tell us if we should entry market. For now, it checked if r2 is above the desired level and then depending if slope
is negative or positive, it tries to enter in the market.
"""

class TradingRules(ind.Indicator):

    def __init__(self,nb_data,date_debut,date_fin,asset,r_square_level):
        super().__init__(nb_data=nb_data,date_debut=date_debut,date_fin=date_fin,asset=asset)
        self.r_square_level=r_square_level
        self.buy_signal=False
        self.sell_signal=False

    def indicator_signal(self):
        for len(range(series)):



        pass

