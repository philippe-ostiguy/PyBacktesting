from scipy import stats
import initialize as init
import data_manip.input_dataframe as idf
import matplotlib.pyplot as plt


class RegressionSlopeStrenght(init.Initialize):
    """
    Indicateur qui évalue si la "slope" est différente de 0 pour une régression linéaire
    Valeurs retournées sont 1 (pente positive), -1 (pente négative) et 0 (neutre)
    Prendre en considération que cette technique viole des principes statistiques, ie l'autocorrélation des données qui fait
    que les erreurs ne suivent pas une loi normale
    + la trend (saisonnalité aussi dans certains cas) qui font que les données ne sont pas indépendantes
    """


    def __init__(self):
        super().__init__()

        idf_ = idf.InputDataframe()
        self.sous_series=idf_.sous_series_()

    def __store_stat(self):

        """
        Function to return stat in a list
        """

        return stats.linregress(self.sous_series[self.date_ordinal_name],
                                self.sous_series[self.adj_close_name])

    def slope(self):
        """
        La pente est la 1ième valeur retournée dans cette stats.linregress, d'où le [0]
        """

        return self.__store_stat()[0]

    def r_square(self):

        """
        La corrélation est la 3ième valeur retournée dans cette stats.linregress, d'où le [2]
        """

        return (self.__store_stat()[2])**2