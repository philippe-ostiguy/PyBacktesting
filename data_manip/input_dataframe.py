import csv
import pandas as pd
import datetime as dt


class InputDataframe():
    """
    Class to treat dataframe before manipulate them in indicators
    """

    name_tempo = "_tempo"
    #date_debut = '' # date debut in_sample
    #date_fin = ''  # date fin in sample
    #asset = ""  # De type csv et dans le répertoires (scope) du projet
    date_name = 'Date'
    close_name = 'Close'
    date_ordinal_name = 'date_ordinal'
    #nb_data=0 #nb données pour tester l'indicateur
    point_data=0 #rendu où dans les données

    def __init__(self):

        self.name_tempor = self.name_tempo
        #self.date_debut = self.date_debut
        #self.date_fin = self.date_fin
        #self.asset = self.asset
        self.date_name=self.date_name
        self.close_name=self.close_name
        self.date_ordinal_name=self.date_ordinal_name
        #self.nb_data=self.nb_data
        self.series=[]
        self.sous_series=[]
        self.point_data=self.point_data

    def reverse_csv(self):
        """
        fonction pour inverse l'ordre des lignes dans un csv (dernière devient la première), etc.
        la première ligne qui contient le nom des colonnes n'est pas touchée
        """

        with open(self.asset + ".csv") as fr, open(self.asset + self.name_tempor + ".csv","w") as fw:
            cr = csv.reader(fr,delimiter=",")
            cw = csv.writer(fw,delimiter=",")
            cw.writerow(next(cr))  # write title as-is
            cw.writerows(reversed(list(cr)))

    def data_frame(self):
        """
         fonction pour retourner le csv sous forme de data frame selon le range désiré avec une colonne numérique pour les
         dates
         Le csv est un format standard Date,Open,High,Low,Close,Adj Close,Volume
         par défaut retourne le close seulement, mais on pourrait changer la possibilité avec usecols (4 est pour le close)
        """

        self.series = pd.read_csv('/Users/philippeostiguy/Desktop/Trading/Programmation_python/Trading/' +self.asset + '.csv',
                             usecols=[0,4],names=[self.date_name,self.close_name],header=0)
        self.series=self.series.loc[(self.series[self.date_name] >= self.date_debut) & (self.series[self.date_name] <= self.date_fin)]
        return self.series

    def ordinal_date(self):
        """
        dataframe pour ajouter une colonne avec les dates en numérique (pas timestamp), ce qui rend plus facile dans
        le calcul des indicateurs
        """
        
        self.series=self.data_frame()
        self.series.Date=pd.to_datetime(self.series.Date)
        self.series[self.date_ordinal_name] = pd.to_datetime(self.series[self.date_name]).map(dt.datetime.toordinal)
        return self.series

    def sous_series_(self,point_data=0):
        """
        Retourne la serie selon la qté de données nécessaires pour la calcul de l'indicateur
        """

        self.sous_series=self.series.iloc[point_data:point_data+self.nb_data,:]

        if self.nb_data > len(self.series):
            raise Exception("Nombre de données pour calcul de l'indicateur plus grand que le nb de données dispo")
        return self.sous_series