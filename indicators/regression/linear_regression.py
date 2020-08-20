from scipy import stats
import data_manip.input_dataframe as idfm
import matplotlib.pyplot as plt

class RegressionSlopeStrenght(idfm.InputDataframe):
    """
    Indicateur qui évalue si la "slope" est différente de 0 pour une régression linéaire
    Valeurs retournées sont 1 (pente positive), -1 (pente négative) et 0 (neutre)
    Prendre en considération que cette technique viole des principes statistiques, ie l'autocorrélation des données qui fait
    que les erreurs ne suivent pas une loi normale
    + la trend (saisonnalité aussi dans certains cas) qui font que les données ne sont pas indépendantes
    """


    def __init__(self,null_hypothesis = 0,nb_data=300,date_debut='2006-10-20', date_fin='2009-04-20',asset="MSFT"):
        super().__init__()
        self.null_hypothesis = null_hypothesis
        self.point_data=self.point_data
        self.nb_data=nb_data #Nombre de données pour évaluer la trend (ou pas trend selon le cas)
        self.date_debut = date_debut  # date debut in_sample
        self.date_fin = date_fin  # date fin in sample
        self.asset = asset # De type csv et dans le répertoires (scope) du projet
        self.series=super().ordinal_date()
        self.sous_series=super().sous_series_()

    def store_stat(self):

        """
        Function to return stat in a list
        """

        return stats.linregress(self.sous_series[super().date_ordinal_name],
                         self.sous_series[super().close_name])

    def slope(self):
        """
        La pente est la 1ième valeur retournée dans cette stats.linregress, d'où le [0]
        """

        return self.store_stat()[0]

    def r_square(self):

        """
        La corrélation est la 3ième valeur retournée dans cette stats.linregress, d'où le [2]
        """

        return (self.store_stat()[2])**2

    def plot_(self):
        self.series.plot(x=super().date_name, y=super().close_name)
        plt.show()