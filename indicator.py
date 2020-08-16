"""
Module to write the output from the indicators into a Dataframe data structure


"""

import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import data_manip.input_dataframe as idf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import charting as cht

nb_data=50
date_debut='2006-10-20'
date_fin='2007-04-20'
asset="MSFT"

class OutputDataframe(idf.InputDataframe):


    def __init__(self,**Indicator):

        super().__init__()
        self.nb_data=nb_data
        self.point_data=self.point_data
        self.date_debut=date_debut
        self.date_fin=date_fin
        self.asset=asset
        self.series=self.ordinal_date()
        self.Indicator = Indicator

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

        chart_= cht.Charting(**self.Indicator).chart(series=self.series)
        fin=0

rg=lr.RegressionSlopeStrenght(nb_data=nb_data,asset=asset,date_debut=date_debut,date_fin=date_fin)
mk_=mk.MannKendall(nb_data=nb_data,asset=asset,date_debut=date_debut,date_fin=date_fin)
indicators={'slope':rg,'r2':rg,'mk':mk_}
odf= OutputDataframe(**indicators)
odf.next()
