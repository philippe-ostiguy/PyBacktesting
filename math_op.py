"""
Basic math operations
"""
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class MathOp():
    """
    Class to provide mathematical operation support
    """

    @classmethod
    def __init__(cls,series,default_col):
        cls.series = series
        cls.default_col=default_col

    @classmethod
    def local_extremum(cls,start_point,end_point,window = 6,min_= 'min',max_='max',index_ = 'index'):
        """ Function to find local extremum (min and max) on a Dataframe

        Parameters
        ----------
        start_point : int
            the first data (index) to check in the Dataframe
        end_point : int
            the last data (index) to check in the Dataframe
        window : int
            the number of the data the method check before and after to determine the local extremum (default is 6)
        min_ : str
            Name given to min data column
        max_ : str
            Name given to max data column


        Return
        ------
        DataFrame list : Return a pandas dataframe `cls.series` with the none empty min or max value
            (if both are empty, nothing is returned. If one of
            them has a value, return the local min or max with index no)
        """

        cls.series=cls.series.loc[start_point:end_point,cls.default_col]
        cls.series=pd.DataFrame({cls.default_col: cls.series})

        cls.series[min_] = cls.series.iloc[argrelextrema(cls.series.values, np.less_equal,
                                                          order=window)[0]][cls.default_col]
        cls.series[max_] = cls.series.iloc[argrelextrema(cls.series.values, np.greater_equal,
                                                          order=window)[0]][cls.default_col]
        cls.series[index_] = cls.series.index

        # Plot results - to get ride when the project is done. Only as a guideline at the moment

        """
        plt.scatter(cls.series.index, cls.series[min_], c='r')
        plt.scatter(cls.series.index, cls.series[max_], c='g')
        
        plt.plot(cls.series.index, cls.series[cls.default_col])
        plt.ion()
        plt.show()
        """

        #Filter nan value for min or max out
        cls.series=cls.series.loc[(cls.series[min_].isna())==False | (cls.series[max_].isna() == False)]

        return cls.series

    @classmethod
    def nan_list(cls,list_):
        """
        Check if a list has one empty value

        Return
        ------
        Bool : `True` or `False`
            Return `True` if at least one value in the list is `nan` and `False otherwise
        """

        return True if True in np.isnan(list_) else False

    @classmethod
    def pd_tolist(cls,pd_, row_name):
        """
        Transform a pandas column to a list. It makes sure it is an integer
        """
        pd__ = pd_.loc[:, row_name].tolist()
        return [int(i) for i in pd__]

