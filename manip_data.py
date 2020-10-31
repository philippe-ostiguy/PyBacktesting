import csv
import pandas as pd
import datetime as dt
from functools import wraps
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt


def plot_diff(func):
    """Decorator to plot the differentiated series"""
    @wraps(func)
    def wrap_diff(cls, series, period, p_value, date_name, date_ordinal_name, default_data):
        series_diff = func(cls, series, period, p_value, date_name, date_ordinal_name, default_data)
        plt.plot(series_diff[date_name], series_diff[default_data])
        plt.ion()
        plt.show()
        return series_diff
    return wrap_diff

def ordinal_date(function):
        """Wrapper to add an ordinal date"""
        @wraps(function)
        def wrapper(cls,date_name,date_debut,date_fin, name_,directory,asset, ordinal_name,is_fx):
            series_ = function(cls,date_name,date_debut,date_fin, name_,directory,asset, ordinal_name,is_fx)
            series_.Date = pd.to_datetime(series_.Date)
            series_[ordinal_name] = pd.to_datetime(series_[date_name]).map(dt.datetime.toordinal)
            return series_

        return wrapper

class ManipData():
    """Class to manipulate data"""

    def __init__(self):
        pass

    @classmethod
    def write_data(cls, dir_output, name_out, add_doc = "", is_walkfoward = False, **kwargs):
        """ Write data to a csv

        Parameters
        ----------
        dir_output : str
            directory where we want our data to be written
        name_out : str
            name of the file name
        is_walkfoward : bool
            says if we are doing a walkfoward analyis. If `True`, we have to create a separate training and test file
        **kwargs : keyword param
            dictionary with keys and items to be written
        """

        if is_walkfoward :
            write_type = 'a'
            func = 'writer.writerow'
        else :
            write_type = 'w'
            func = 'str'

        with open(dir_output + name_out + add_doc + ".csv" , write_type, newline='') as f:
            writer = csv.writer(f)
            eval(func)('')
            for key, item in kwargs.items():
                writer.writerow([key,item])

    def col_numb(cls, asset, name_):
        """Determine if column name exist in csv"""

        with open(asset + ".csv") as file:
            reader = csv.reader(file, delimiter=",")
            col_name = next(reader)

        for col_number in range(len(name_.columns)):
            for col_number_ in range(len(col_name)):
                if name_.columns[col_number] == col_name[col_number_]:
                    name_.loc[0, name_.columns[col_number]] = int(col_number_)
                    break

            if name_[name_.columns[col_number]].empty:
                raise Exception('Column name "{}" does not exist in database'.format(name_.columns[col_number]))

    @classmethod
    @ordinal_date
    def data_frame(cls,date_name,date_debut,date_fin, name_,directory,asset, ordinal_name = '',is_fx = False):
        """Return the csv to a dataframe"""

        if is_fx:
            dateparse = lambda x: dt.datetime.strptime(x, '%d.%m.%Y %H:%M:%S')
        else :
            dateparse = None
        series_ = pd.DataFrame()
        _series = pd.read_csv(directory
                               + asset + '.csv', usecols=list(name_.columns),parse_dates=[date_name],
                              date_parser=dateparse)
        series_ =_series.loc[(_series[date_name] >= date_debut) & (_series[date_name] < date_fin)]
        if series_.empty:
            raise Exception("Desired range date not available in the current files or not able to read the csv")
        series_=series_.reset_index(drop=True)
        return series_

    @classmethod
    def sous_series_(cls,series_,nb_data,point_data=0):
        """Returns a sub-series to calculate the value of the indicator with in a precise
        """

        cls.sous_series=series_.iloc[point_data:point_data + nb_data,:]
        if nb_data > len(series_):
            raise Exception("Number of necessary data to calculate the indicator lower than available data")
        return cls.sous_series


    @classmethod
    @plot_diff
    def de_trend(cls, series, period, p_value, date_name, date_ordinal_name, default_data):
        """Remove the trend from the series by different with the last value. First value is set to 0 to avoid error"""

        series_diff = series.copy()
        series_diff.drop([date_name, date_ordinal_name], axis=1, inplace=True)
        series_diff = series_diff.diff(periods=period)  # differentiate with previous row
        series_diff.loc[:(period - 1), :] = 0
        series_diff.insert(0, date_name, series[date_name])
        series_diff[date_ordinal_name] = series[date_ordinal_name]
        if adfuller(series_diff[default_data])[1] > p_value:
            raise Exception("The differentiated series is not stationary")
        return series_diff
