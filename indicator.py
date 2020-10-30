"""
Return the values of indicator of our choice through the desired timeframe, lenght test
"""

import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import data_init as di
import initialize as init
import numpy as np
from manip_data import ManipData as md

class Indicator(di.DataInit):

    def __init__(self):

        super().__init__()
        super().__call__()
        rg = lr.RegressionSlopeStrenght(self.series_test)
        mk_ = mk.MannKendall(self.series_test)
        self.indicator = {'slope': rg, 'r_square': rg, 'mk': mk_}
        self.point_data=0
        self.slope_key=list(self.indicator.keys())[0]
        self.r_square_key=list(self.indicator.keys())[1]

    def __call__(self):

        """
        Function that return the value of an indicator through desired period, lenght calculation of the
        indicator

        The indicator always take into account the value of price for the same row. Ex: We are at row 99, the indicator
        will take into account the data for row 99 then write the value on row 99. Basically, we have to enter or exit
        the market (or exit) on the next row (value)
        """
        nb_columns=len(self.series_test.columns)

        for key,value in self.indicator.items():
            self.series_test[key] = np.nan
            value.point_data = 0

            for row in range(len(self.series_test.index)-self.nb_data+1):
                value.sous_series = md.sous_series_(self.series_test,self.nb_data,point_data=value.point_data)
                value_ = getattr(value,key)()
                self.series_test.loc[self.series_test.index[row]+self.nb_data-1,key]=value_
                value.point_data+=1