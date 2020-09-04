"""
Initialize default value
"""

class Initialize():
    """
    IMPORTANT NOTE
    Indicator to test are in the indicator.py file
    Could be improved to set them here in Initialize()
    """



    def __init__(self):

        #No need to change them
        self.date_name = 'Date'
        self.open_name = 'Open'
        self.high_name = 'High'
        self.low_name = 'Low'
        self.close_name = 'Close'
        self.adj_close_name = 'Adj Close'
        self.date_ordinal_name = 'date_ordinal'
        self.point_data=0

        # Set desired value to test the indicator
        self.date_debut = '2009-01-20'
        self.date_fin = '2010-01-20'
        self.asset = "MSFT"
        self.nb_data = 100  # nb of data on which data are tested

        # Indicator value to trigger a signal
        self.r_square_level = .8
        self.min_data = 100  # nb of data between a signal