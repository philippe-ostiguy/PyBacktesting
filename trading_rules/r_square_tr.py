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
        self._signal=False #no signal entry

    def indicator_signal(self,**kwargs):
        """
        Take 2 key-word args : r2 level to triger a signal + minimum nb of data between each signal before
        trigerring a new signal
        """
        self._r_square_level=list(kwargs.values())[0]
        self._min_data=list(kwargs.values())[1]

        for (curr_data + self.nb_data) in range(len(self.series)):
            pass





