"""Return the values of the indicator of our choice through the desired timeframe and interval"""

import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import numpy as np
from manip_data import ManipData as md
from init_operations import InitOp

class Indicator(InitOp):

    def __init__(self):
        super().__init__()

    def __call__(self):
        super().__call__()

    def calcul_indicator(self):
        """Function that return the value of an indicator through desired period and the calculation lenght of the
        indicator

        The indicator always take into account the value of the price for the same row.
        Ex: We are at row 99, the indicator will take into account the data for row 99 then write the value on row 99.
        Basically, we have to enter or exit the market (or exit) on the next row (value)

        The function iterate through the indicators in `self.indicator` and through the range of `self.series`,defined
        in `init_operations.py` and function `init_series()`. Then it calculates the value of the indicator using
        the subseries `self.sous_series`.
        """

        super().__call__()
        rg = lr.RegressionSlopeStrenght(self.series,self)
        mk_ = mk.MannKendall(self.series,self)
        self.indicator = {'slope': rg, 'r_square': rg, 'mk': mk_}
        self.point_data=0
        self.slope_key=list(self.indicator.keys())[0]
        self.r_square_key=list(self.indicator.keys())[1]
        self.mk_key = list(self.indicator.keys())[2]

        self.point_data = 0
        nb_columns=len(self.series.columns)

        for key,value in self.indicator.items():
            self.series[key] = np.nan
            value.point_data = 0

            for row in range(len(self.series.index)-self.nb_data+1):
                value.sous_series = md.sous_series_(self.series,self.nb_data,point_data=value.point_data)
                value_ = getattr(value,key)()
                self.series.loc[self.series.index[row]+self.nb_data-1,key]=value_
                value.point_data+=1