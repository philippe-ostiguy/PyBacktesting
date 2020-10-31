from scipy import stats
from initialize import Initialize
from manip_data import ManipData as md

class RegressionSlopeStrenght(Initialize):
    """
    Indicateur qui évalue si la "slope" est différente de 0 pour une régression linéaire
    Valeurs retournées sont 1 (pente positive), -1 (pente négative) et 0 (neutre)
    Prendre en considération que cette technique viole des principes statistiques, ie l'autocorrélation des données qui fait
    que les erreurs ne suivent pas une loi normale
    + la trend (saisonnalité aussi dans certains cas) qui font que les données ne sont pas indépendantes
    """


    def __init__(self,series_):
        super().__init__()
        super().__call__()

        #init_ = init.Initialize()
        self.sous_series=md.sous_series_(series_,self.nb_data)

    def __store_stat(self):

        """
        Function to return stat in a list
        """

        return stats.linregress(self.sous_series[self.date_ordinal_name],
                                self.sous_series[self.default_data])

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