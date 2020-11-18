"""Module to easily reinitiliaze values when needed """

from initialize import Initialize
from manip_data import ManipData as md
import pandas as pd

class InitOp(Initialize):

    def __init__(self):
        super().__init__()
        super().__call__()

    def __call__(self):
        self.reset_value()

    def reset_value(self):
        """Function to reset the dictionary that contains the trading journal (entry, exit, return) in
        `self.trades_track`

         We need to do that when we optimize, ie when `self.is_walkfoward` is `True`

         """

        self.trades_track = pd.DataFrame(columns=[self.entry_row, self.entry_level, self.exit_row, self.exit_level, \
                                                  self.trade_return])

    def init_series(self):
        """Function that extract the data from csv to a pandas Dataframe `self.series`

        It actually is the data that we are using for the strategy """

        self.series = md.csv_to_pandas(self.date_name, self.start_date, self.end_date, self.name, self.directory,
                            self.asset, ordinal_name=self.date_ordinal_name, is_fx=self.is_fx, dup_col = self.dup_col)

        """
        if self.is_detrend:
            self.series_test = md.de_trend(self.series,self.period, self.p_value,self.date_name,
                                           self.date_ordinal_name,self.default_data)
        else :
            self.series_test = self.series.copy()
        """