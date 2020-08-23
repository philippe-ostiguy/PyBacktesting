import matplotlib.pyplot as plt


class Charting():

    def __init__(self, **indicator):

        self.indicator=indicator
        self.indicator_dict = {}
        count = len(self.indicator)
        self.divider = .24
        self.height_chart = self.divider * (count)

        fig = plt.figure()
        fig.set_size_inches((40, 32))
        self.candle = fig.add_axes((0, self.height_chart, 1, 0.25))


        count2 = 1
        for key, _ in self.indicator.items():
            self.indicator_dict[key]=fig.add_axes((0, self.height_chart-self.divider*count2, 1, 0.2), sharex=self.candle)
            count2 += 1

        """ 
            ax_slope = fig.add_axes((0, 0.48, 1, 0.2), sharex=ax_candle)
            ax_r2 = fig.add_axes((0, 0.24, 1, 0.2), sharex=ax_candle)
            ax_mk = fig.add_axes((0, 0, 1, 0.2), sharex=ax_candle)
        """

    def chart(self, series, column_date=0, column_price='Close'):

        date_name = series.columns[column_date]


        first_index = series.first_valid_index()
        tempo_mark=[]
        tempo_mark= series.loc[series['r_square']>.8].index.tolist()
        mark_= [i - first_index for i in tempo_mark]

        self.candle.plot(date_name, column_price, markevery =mark_, marker = "o",data = series)

        for key, _ in self.indicator.items():
            self.indicator_dict[key].plot(date_name, key, data=series)