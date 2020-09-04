import matplotlib.pyplot as plt


class Charting():

    @classmethod
    def __init__(cls, **indicator):

        cls.indicator=indicator
        cls.indicator_dict = {}
        count = len(cls.indicator)
        cls.divider = .24
        cls.height_chart = cls.divider * (count)

        fig = plt.figure()
        fig.set_size_inches((40, 32))
        cls.candle = fig.add_axes((0, cls.height_chart, 1, 0.25))


        count2 = 1
        for key, _ in cls.indicator.items():
            cls.indicator_dict[key]=fig.add_axes((0, cls.height_chart-cls.divider*count2, 1, 0.2), sharex=cls.candle)
            count2 += 1

    @classmethod
    def chart(cls,r_square_name, series,column_price, column_date=0, r_square_level=.8):

        date_name = series.columns[column_date]

        #When r2 is higher than desired level, we have a mark on chart
        first_index = series.first_valid_index()
        tempo_mark=[]
        tempo_mark= series.loc[series[r_square_name]>r_square_level].index.tolist()
        mark_= [i - first_index for i in tempo_mark]

        cls.candle.plot(date_name, column_price, markevery =mark_, marker = "o",data = series)

        for key, _ in cls.indicator.items():
            cls.indicator_dict[key].plot(date_name, key, data=series)