import indicator as ind
import entry.entry_fibo as ef

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

        self.ef_=ef.EntFibo(series=self.series)


    def signal_trig(self):

        """
        Take 2 key-word args : r2 level to triger a signal + minimum nb of data between each signal before
        trigerring a new signal telling us to try to enter in the market. It gives the signal on each row (data),
        so we enter or exit in the market on the next row (data)
        """

        buy_signal = False #Tells if there is a buy signal entry. No signal entry by default
        sell_signal = False #Tells if there is a sell signal entry. No signal entry by default

        for row in range(len(self.series)-self.nb_data+1):
            curr_row=row + self.nb_data-1

            slope_value=self.series.loc[curr_row, self.slope_key]
            r_value=self.series.loc[curr_row,self.r_square_key]

            #Buy signal
            if slope_value > 0 :
                if r_value > self.r_square_level:
                    if self.last_long >= self.nb_data :
                        buy_signal = True
                        self.last_short = self.nb_data
                        self.ef_(curr_row=curr_row,buy_signal = buy_signal)
                    self.last_long = 0

            #Sell signal
            if slope_value < 0 :
                if r_value > self.r_square_level:
                    self.last_short -= 1
                    if self.last_short >= self.nb_data :
                        sell_signal=True
                        self.last_long = self.nb_data
                        self.ef_(curr_row=curr_row,sell_signal=sell_signal)

                    self.last_short=0

            self.last_long += 1
            self.last_short += 1