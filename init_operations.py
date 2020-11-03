"""Class with functions that initialize the program"""

from initialize import Initialize
from manip_data import ManipData as md
import pandas as pd

class InitOp(Initialize):

    def __init__(self):
        super().__init__()

    def __call__(self):
        super().__call__()
        self.reset_value()
        self.init_series()

    def reset_value(self):
        """Value that must be reseted if we run optimization"""
        self.trades_track = pd.DataFrame(columns=[self.entry_row, self.entry_level, self.exit_row, self.exit_level, \
                                                  self.trade_return])

    def init_series(self):
        """Function to get the data as Dataframe"""

        self.series = md.csv_to_pandas(self.date_name, self.date_debut, self.date_fin, self.name,self.directory,
                                self.asset, ordinal_name=self.date_ordinal_name, is_fx=self.is_fx, dup_col = self.dup_col)

        if self.is_detrend:
            self.series_test = md.de_trend(self.series,self.period, self.p_value,self.date_name,
                                           self.date_ordinal_name,self.default_data)
        else :
            self.series_test = self.series.copy()