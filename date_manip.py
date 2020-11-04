from dateutil.relativedelta import relativedelta
from datetime import datetime
import collections

class DateManip():
    """Class to manipulate date"""

    @classmethod
    def __init__(cls,date):

        cls.date_ = date

    @classmethod
    def date_dict(cls,begin_date, end_date,**kwargs):
        """ Create a dictionary of dictionary containing start and end date between 2 periods

            Contain subdates depending on how many different subcategories we want and the lenght of the original
            data

        Parameters
        ----------
        `begin_date` : datetime
            Must be in datetime format, it's the first date of the original serie

        `end_date` : datetime
            Must be in datetime format, it's the last date of the original serie

        `**kwargs` : kw argument
            Contain the lenght of subseries (date) we want to create

        Returns
        ----------
        `dict_date_` : dictionary of n keys in **kwargs
            containing the beginning and ending date of subseries dependin
        """
        _months = 0
        for value in kwargs.values():
            _months+=value

        _test_end = begin_date + relativedelta(months = _months)
        _date = begin_date
        _count = 0
        _dict_date = collections.defaultdict(dict)
        while (_test_end < end_date):
            for key, value in kwargs.items():
                _end_date = _date + relativedelta(months =kwargs[key])
                _dict_date[_count][key] = [_date, _end_date]
                _date = _end_date
            _count +=1
            _test_end = _test_end + relativedelta(months = _months)
        return _dict_date

    @classmethod
    def end_format(cls,format_):
        """Return a datetime to the desired TimeStamp in str

        Parameters
        ----------
        `format_` : str
            Format code in which we want to return the datetime
        """
        return cls.date_.strftime(format_)

