

"""
Trying to enter the market with fibonacci retracement and extension. 3 types:
    1- Retracement from last wave
    2- Retracement from beginning of the trend
    3- Extension from a previous wave (largest one in the trend)

Basically, it will try to fin the peak from a trend if we are trying to buy (or a peak if we are trying to sell)
"""

class EntFibo():


    def __init__(cls,series,last_retracement = True, first_retracement = True, extension = True):

        """

        PARAMS:
            - last_retracement is to say if we try to retrace from last wave
            - first_retracement is to say if we try to retrace from the beginning of the trend
            - extenstion is to say if we try to buy by extending largest setback from the trend
        """

        cls.series=series
        cls.last_retracement = last_retracement
        cls.first_retracement = first_retracement
        cls.extension=extension


    @classmethod
    def ent_fibo(cls,row,nb_data,buy_signal=False,sell_signal=False):

        cls.buy_signal = buy_signal
        cls.sell_signal = sell_signal
        cls.curr_row = row + nb_data
        if buy_signal and sell_signal :
            raise Exception('Cannot have a buy and sell signal at the same time')

        if cls.buy_signal :
            pass

    @classmethod
    def __retracement(cls):


        pass



