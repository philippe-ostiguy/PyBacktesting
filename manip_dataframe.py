import pandas as pd
import datetime as dt


"""
 fonction pour retourner le csv sous forme de data frame selon le range désiré avec une colonne numérique pour les
 dates
 Le csv est un format standard Date,Open,High,Low,Close,Adj Close,Volume
 par défaut retourne le close seulement, mais on pourrait changer la possibilité avec usecols (4 est pour le close)
"""

class ManipulateDataframe():
    name_tempo = "_tempo"
    date_debut = '2009-04-01' # date debut in_sample
    date_fin = '2016-10-20'  # date fin in sample
    asset = "MSFT"  # De type csv et dans le répertoires (scope) du projet
    date_name = 'Date'
    close_name = 'Close'
    date_ordinal_name = 'date_ordinal'

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries

        self.date_debut = self.date_debut
        self.date_fin = self.date_fin
        self.asset = self.asset
        self.date_name=self.date_name
        self.close_name=self.close_name
        self.date_ordinal_name=self.date_ordinal_name


    def data_frame(self):
        series = pd.read_csv(self.asset + '.csv', usecols=[0, 4], names=[self.date_name, self.close_name], header=0)
        series = series.loc[(series[self.date_name] > self.date_debut) & (series[self.date_name] < self.date_fin)]
        return series

        # dataframe pour ajouter une colonne avec les dates en numérique (pas timestamp)

    def ordinal_date(self):
        series = self.data_frame()
        series.Date = pd.to_datetime(series.Date)
        series[self.date_ordinal_name] = pd.to_datetime(series[self.date_name]).map(dt.datetime.toordinal)
        return series

