import csv
import pandas as pd
import datetime as dt
import initialize as init

class InputDataframe(init.Initialize):
    """
    Class to treat dataframe before manipulate them in indicators
    """

    def __init__(self):

        super().__init__()

        #No need to change them here
        self.__name_tempor = "_tempo"

        self.series=self.ordinal_date()

    def reverse_csv(self):
        """
        fonction pour inverse l'ordre des lignes dans un csv (dernière devient la première), etc.
        la première ligne qui contient le nom des colonnes n'est pas touchée
        """

        with open(self.asset + ".csv") as fr, open(self.asset + __name_tempor + ".csv","w") as fw:
            cr = csv.reader(fr,delimiter=",")
            cw = csv.writer(fw,delimiter=",")
            cw.writerow(next(cr))  # write title as-is
            cw.writerows(reversed(list(cr)))

    def __data_frame(self):
        """
         fonction pour retourner le csv sous forme de data frame selon le range désiré avec une colonne
         numérique pour les dates
         Le csv est un format standard Date,Open,High,Low,Close,Adj Close,Volume
         par défaut retourne le close seulement, mais on pourrait changer la possibilité avec usecols
         (4 est pour le close)
        """

        __series = pd.read_csv('/Users/philippeostiguy/Desktop/Trading/Programmation_python/Trading/'
                                  + self.asset + '.csv', usecols=[0,4],names=[__date_name,__close_name],header=0)
        self.series=__series.loc[(__series[__date_name] >= self.__date_debut) & (__series[date_name]
                                                                                        <= self.__date_fin)]

        self.series=self.series.reset_index(drop=True)
        return self.series

    def ordinal_date(self):
        """
        dataframe pour ajouter une colonne avec les dates en numérique (pas timestamp), ce qui rend plus facile dans
        le calcul des indicateurs
        """
        
        self.series=self.__data_frame()
        self.series.Date=pd.to_datetime(self.series.Date)
        self.series[__date_ordinal_name] = pd.to_datetime(self.series[self.__date_name]).map(dt.datetime.toordinal)

        return self.series

    def sous_series_(self,point_data=0):
        """
        Retourne la serie selon la qté de données nécessaires pour la calcul de l'indicateur (itération)
        """

        self.sous_series=self.series.iloc[point_data:point_data+self.nb_data,:]

        if self.nb_data > len(self.series):
            raise Exception("Nombre de données pour calcul de l'indicateur plus grand que le nb de données dispo")
        return self.sous_series