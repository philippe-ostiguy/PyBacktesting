""" Read data, clean them and store them in csv"""
import initialize as init
from manip_data import ManipData as md
from statsmodels.tsa.stattools import adfuller
import pandas as pd
import matplotlib.pyplot as plt

class DataInit(init.Initialize):

    def __init__(self):
        super().__init__()
        super().__call__()

        self.name = pd.DataFrame(self.name_col)
        self.date_ordinal_name = 'Ordinal Date'



    def __call__(self, *args, **kwargs):
        self.series = md.data_frame(self.date_name, self.date_debut, self.date_fin, self.name,
                                    self.directory, self.asset, ordinal_name=self.date_ordinal_name, is_fx=self.is_fx)

        self.series_test = self.series.copy()
        if self.is_detrend:
            self.de_trend(self.period, self.p_value)



    def de_trend(self):
        """Remove the trend from the series by different with the last value. First value is set to 0 to avoid error"""

        self.series_diff = self.series.copy()
        self.series_diff.drop([self.date_name, self.date_ordinal_name], axis=1, inplace=True)
        self.series_diff = self.series_diff.diff(periods=self.period)  # differentiate with previous row
        self.series_diff.loc[:(self.period - 1), :] = 0
        self.series_diff.insert(0, self.date_name, self.series[self.date_name])
        self.series_diff[self.date_ordinal_name] = self.series[self.date_ordinal_name]
        self.series_test = self.series_diff
        if adfuller(self.series_diff[self.default_data])[1] > self.p_value:
            raise Exception("The differentiated series is not stationary")

    def plot_diff(self):
        """Plotting the differentiated series"""
        plt.plot(self.series_diff[self.date_name], self.series_diff[self.default_data])
        plt.ion()
        plt.show()
