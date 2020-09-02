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

class Indicator(idf.InputDataframe):


    def __init__(self,nb_data,date_debut,date_fin,asset):

        super().__init__(nb_data=nb_data,date_debut=date_debut,date_fin=date_fin,asset=asset)

    def calcul_indicator(self,**indicator):

        """
        Function that return the value of an indicator through desired period, lenght calculation of the
        indicator
        """
        nb_columns=len(self.series.columns)

        for key,value in indicator.items():
            self.series[key] = np.nan
            value.point_data = 0
            value.sous_series = self.sous_series_()
            value_ = getattr(value,key)()

            for row in range(len(self.series.index)-self.nb_data+1):
                self.series.loc[self.series.index[row]+self.nb_data-1,key]=value_
                value.point_data+=1
                value.sous_series = self.sous_series_(point_data=value.point_data)
                value_ = getattr(value,key)()

        t=5
