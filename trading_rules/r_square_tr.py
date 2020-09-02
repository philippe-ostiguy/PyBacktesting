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


    def __init__(self,nb_data,date_debut,date_fin,asset,**kwargs):
        super().__init__(nb_data=nb_data,date_debut=date_debut,date_fin=date_fin,asset=asset,**kwargs)
        self.r_square_key=list(self.indicator.keys())[1]

    def indicator_signal(self,**kwargs):
        """
        Take 2 key-word args : r2 level to triger a signal + minimum nb of data between each signal before
        trigerring a new signal
        """
        self.__r_square_level=list(kwargs.values())[0]
        self.__r_square_level = list(kwargs.values())[0]
        self.__min_data=list(kwargs.values())[1]
        __buy_signal=False #Tells if there is a buy signal entry. No signal entry by default
        __sell_signal=False #Tells if there is a sell signal entry. No signal entry by default

        nb_data_signal=0 #nb of data between a signal
        for row in range(len(self.series)-self.nb_data):
            if self.series.loc[row+self.nb_data-1,self.r_square_key]>self.__r_square_level and


            pass