[WIP] Library to find trend (using regression analysis and Mann-Kendall), then buy/sell setback using Fibonacci retracements and extension

class Main(Optimize):

    def __init__(self):
        super().__init__()
        super().__call__()
        self.cht_ = cht.Charting(self.series, self.date_name,
                                 self.default_data, series_test=self.series, **self.indicator)
        t = 5
