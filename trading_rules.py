import indicator as ind
import indicators.regression.linear_regression as lr
import indicators.regression.mann_kendall as mk
import data_manip.input_dataframe as idf
import charting as cht

#ind.Indicator
class TradingRules(ind.Indicator):

    def __init__(self,nb_data,date_debut,date_fin,asset):
        super().__init__(nb_data=nb_data,date_debut=date_debut,date_fin=date_fin,asset=asset)

    def indicator_signal(self):
        """
            Tell us if we should entry market
        """
        pass