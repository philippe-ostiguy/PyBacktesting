import indicator as ind
import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import data_manip.input_dataframe as idf
import charting as cht

"""
Tell us if we should entry market. For now, it checked if r2 is above the desired level 
and then depending if the price's slope is negative or positive,
it trigers a signal to get long (slope is positive) or to get short (slope is negative)
"""

class RSquareTr(ind.Indicator):


    def __init__(self,nb_data,date_debut,date_fin,asset):
        super().__init__(nb_data=nb_data,date_debut=date_debut,date_fin=date_fin,asset=asset)
        self.r_square_level=args[0]
        self.buy_signal=False
        self.sell_signal=False

    def indicator_signal(self,**indicator):

        for curr_data in len(range(self.series)):
            pass





