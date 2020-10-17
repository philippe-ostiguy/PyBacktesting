import alpha_vantage.foreignexchange as fx
import pandas as pd
import os

api_key = os.environ.get('ALPHAVANTAGE_API_KEY')
api_key_ = os.environ.get('FINHUB_API_KEY')

from_symbol = 'EUR'
to_symbol = 'USD'
size = 'full'

class AlphaVantage():
    """
    Class to get the data from alphavantage
    """

    @classmethod
    def intraday_fx(cls):

        # Submit our API and create a session
        alpha_fx = fx.ForeignExchange(key=api_key, output_format='pandas',)


        data_, _ = alpha_fx.get_currency_exchange_intraday(from_symbol = from_symbol, to_symbol = to_symbol, \
                                                          interval='5min',outputsize=size)


        # Convert the index to datetime.
        data_.index = pd.to_datetime(data_.index)
        data_.columns = ['Open', 'High', 'Low', 'Close']
        return data_

av_ = AlphaVantage()
data_ = av_.intraday_fx()
t = 5