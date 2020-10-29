import csv

class DateManip():
    """Class to manipulate date"""

    def __init__(self):
        pass

    @classmethod
    def date_dict(cls, dict_date_, begin_date, end_date,**kwargs):
        """ Create a dictionary of dictionary containing start and end date between 2 periods

            Contain subdates depending on how many different subcategories we want and the lenght of the original
            data

        Parameters
        ----------
        `begin_date` : str
            Must be in datetime format, it's the first date of the original serie

        `end_date` : str
            Must be in datetime format, it's the last date of the original serie

        `**kwargs` : kw argument
            Contain the lenght of subseries (date) we want to create

        Returns
        ----------
        `dict_date_` : dictionary of n keys in **kwargs
            containing the beginning and ending date of subseries dependin
        """

        count = 0

        for key, item in kwargs.items():
            dict_date_.append{keys:{count:}}
            count +=1

            writer.writerow([key, item])
