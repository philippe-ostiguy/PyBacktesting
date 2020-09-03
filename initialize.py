"""
Initialize default value
"""

class Initialize():

    def __init__(self):

        #No need to change them
        self.date_name = 'Date'
        self.close_name = 'Close'
        self.date_ordinal_name = 'date_ordinal'
        self.point_data=0

        # Set desired value to test the indicator
        self.date_debut = '2009-01-20'
        self.date_fin = '2011-01-20'
        self.asset = "MSFT"
        self.nb_data = 100  # nb of data on which data are tested

        # Indicator value to trigger a signal
        self.r_square_level = .8
        self.min_data = 100  # nb of data between a signal


        rg = lr.RegressionSlopeStrenght()
        mk_ = mk.MannKendall()
        self.indicator = {'slope': rg, 'r_square': rg, 'mk': mk_}

        self.slope_key=list(self.indicator.keys())[0]
        self.r_square_key=list(self.indicator.keys())[1]