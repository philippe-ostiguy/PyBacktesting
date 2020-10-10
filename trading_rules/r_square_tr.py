import indicator as ind
import entry.entry_fibo as enf
import exit.exit_fibo as exf

"""
Tell us if we should entry market. For now, it checked if r2 is above the desired level 
and then depending if the price's slope is negative or positive,
it trigers a signal to get long (slope is positive) or to get short (slope is negative)
"""

class RSquareTr(ind.Indicator):


    def __init__(self):
        super().__init__()
        self.last_long = self.nb_data #last time we had a long signal
        self.last_short = self.nb_data  #last time we had a short signal

    def signal_trig(self):

        """
        Take 2 key-word args : r2 level to triger a signal + minimum nb of data (self.min_data) between each
        signal before trigerring a new signal telling us to try to enter in the market. It gives the signal
        on each row (data), so we enter or exit in the market on the next row (data)

        """

        buy_signal = False
        sell_signal = False

        for row in range(len(self.series)-self.nb_data+1):
            curr_row=row + self.nb_data-1

            slope_value=self.series.loc[curr_row, self.slope_key]
            r_value=self.series.loc[curr_row,self.r_square_key]

            #Buy signal

            if slope_value > 0 :
                if r_value > self.r_square_level:
                    if self.last_long >= self.min_data :
                        buy_signal = True
                        self.last_short = self.min_data
                        exf.ExitFibo(curr_row=curr_row,buy_signal=buy_signal).__call__()
                    self.last_long = 0

            #Sell signal
            if slope_value < 0 :
                if r_value > self.r_square_level:
                    self.last_short -= 1
                    if self.last_short >= self.min_data :
                        sell_signal=True
                        self.last_long = self.min_data
                        exf.ExitFibo(curr_row=curr_row,sell_signal=sell_signal).__call__()
                    self.last_short=0

            buy_signal = False
            sell_signal = False

            self.last_long += 1
            self.last_short += 1