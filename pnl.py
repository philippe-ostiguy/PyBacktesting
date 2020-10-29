import trading_rules as tr
import numpy as np
import math
from manip_data import ManipData as md

class PnL(tr.RSquareTr):

    def __init__(self):
        super().__init__()
        super().__call__()
        self.start_date_ = self.series.iloc[0, self.series.columns.get_loc(self.date_name)]
        self.end_date_ = self.series.iloc[-1, self.series.columns.get_loc(self.date_name)]

    def __call__(self):
        self.diff_ = ((self.end_date_ - self.start_date_).days / 365) #diff in term of year with decimal
        self.pnl_dict[self.ann_return_] = self.ann_return()
        self.pnl_dict[self.ann_vol_] = self.ann_vol()
        self.pnl_dict[self.sharpe_ratio_] = self.sharpe_ratio()
        self.pnl_dict[self.max_draw_] = self.max_draw()
        self.pnl_dict[self.pour_win_] = self.pour_win()
        md.write_data(self.dir_output, self.name_out,add_doc=self.doc_name_[self.training_name_],
                      is_walkfoward=self.is_walkfoward, **self.pnl_dict)

    def annualized_(func):
        """Decorator to return annualized value"""
        def wrap_diff(self):
            return ((1+func(self))**(1/self.diff_)-1)
        return wrap_diff

    @annualized_
    def ann_return(self):
        """Calculate the annualized return"""
        return_ = 0
        for index_ in self.trades_track.index:
            return_ = (1+return_)*(1+self.trades_track.loc[index_,self.trade_return]) - 1
        return return_

    def ann_vol(self):
        """Calculate annualized vol
        """

        vol_ = self.trades_track[self.trade_return].std()
        if not np.isnan(vol_):
            return (vol_ *  math.sqrt(1/self.diff_))
        else :
            return None

    def sharpe_ratio(self):
        """Sharpe ratio

        Not using the risk-free rate has it doesn't change the final result
        """
        if self.pnl_dict[self.ann_vol_] == None:
            return None

        elif ((self.pnl_dict[self.ann_vol_] == 0) | np.isnan(self.pnl_dict[self.ann_vol_])):
            return None
        else :
            return (self.pnl_dict[self.ann_return_] /self.pnl_dict[self.ann_vol_])

    def max_draw(self):
        """Return lowest value """

        return self.trades_track[self.trade_return].min()

    def pour_win(self):
        """Return the pourcentage of winning trades
        """

        total_trade = self.trades_track.shape[0]
        pour_win_ = self.trades_track[self.trades_track[self.trade_return] >= 0].shape[0]
        return (pour_win_ / total_trade)