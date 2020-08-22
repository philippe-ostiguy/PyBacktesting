"""
Return the values of indicator of our choice through the desired timeframe, lenght test
"""

import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import data_manip.input_dataframe as idf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import charting as cht
from abc import abstractmethod,ABCMeta


class Indicator(idf.InputDataframe):

    #__metaclass__ = ABCMeta

    #@abstractmethod
    def __init__(self,**Indicator):
        #super().__init__()

        #self.series=self.ordinal_date()
        #self.Indicator = Indicator

    def next(self):

        """
        Function that iterate to get the value of the indicator through the desired period.
        """
        nb_columns=len(self.series.columns)

        for key,value in self.Indicator.items():
            self.series[key] = np.nan
            value.point_data = 0
            value.sous_series = self.sous_series_()
            value_ = getattr(value,key)()

            for row in range(len(self.series.index)-self.nb_data+1):
                self.series.loc[self.series.index[row]+self.nb_data-1,key]=value_
                value.point_data+=1
                value.sous_series = self.sous_series_(point_data=value.point_data)
                value_ = getattr(value,key)()

        cht.Charting(**self.Indicator).chart(series=self.series)
        fin=0
""" 
rg=lr.RegressionSlopeStrenght(nb_data=nb_data,date_debut=date_debut,date_fin=date_fin)
mk_=mk.MannKendall(nb_data=nb_data,date_debut=date_debut,date_fin=date_fin)
indicators={'slope':rg,'r_square':rg,'mk':mk_}
odf= Indicator(**indicators)
odf.next()
"""