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

    def __init__(self):
        super().__init__()
        self.curr_row=0 #current row

    def signal_trig(self):

        """
        Take 2 key-word args : r2 level to triger a signal + minimum nb of data between each signal before
        trigerring a new signal telling us to try to enter in the market. It
        """

        __buy_signal = False #Tells if there is a buy signal entry. No signal entry by default
        __sell_signal = False #Tells if there is a sell signal entry. No signal entry by default

        for row in range(len(self.series)-self.nb_data-self.curr_row):
            if self.nb_data >= self.curr_row:
                if self.series.loc[row+self.nb_data-1,self.r_square_key]>self.r_square_level:
                    self.curr_row += 1
                    if self.series.loc[row + self.nb_data - 1, self.slope_key] > 0:
                        __buy_signal=True
                    if self.series.loc[row + self.nb_data - 1, self.slope_key] < 0:
                        __sell_signal=True
            else :
                self.curr_row-=1