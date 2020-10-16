"""
Return the values of indicator of our choice through the desired timeframe, lenght test
"""

import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import initialize as init
import numpy as np


class Indicator(init.Initialize):


    def __init__(self):

        super().__init__()

        rg = lr.RegressionSlopeStrenght(self.series_diff)
        mk_ = mk.MannKendall(self.series_diff)
        self.indicator = {'slope': rg, 'r_square': rg, 'mk': mk_}

        self.slope_key=list(self.indicator.keys())[0]
        self.r_square_key=list(self.indicator.keys())[1]


    def calcul_indicator(self):

        """
        Function that return the value of an indicator through desired period, lenght calculation of the
        indicator

        The indicator always take into account the value of price for the same row. Ex: We are at row 99, the indicator
        will take into account the data for row 99 then write the value on row 99. Basically, we have to enter or exit
        the market (or exit) on the next row (value)
        """
        nb_columns=len(self.series_diff.columns)

        for key,value in self.indicator.items():
            self.series_diff[key] = np.nan
            value.point_data = 0

            for row in range(len(self.series_diff.index)-self.nb_data+1):
                value.sous_series = self.sous_series_(self.series_diff,point_data=value.point_data)
                value_ = getattr(value,key)()
                self.series_diff.loc[self.series_diff.index[row]+self.nb_data-1,key]=value_
                value.point_data+=1