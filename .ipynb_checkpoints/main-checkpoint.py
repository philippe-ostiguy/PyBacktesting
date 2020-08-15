#coding=utf-8
"""
Module principal :
- qui va chercher les données sur les données sur AlphaV Vantage grâce à l'API
- test la stratégie de trading grâces au package backtrader
- Si on veut changer les valeurs de range pour une stratégie, ce sera dans le module strategies --> les params

N.B. Ce module est pour tester le forex seulement. Si on veut tester sur d'autres actifs (stock par exemple),
il faut changer la manière d'aller chercher les données (dans la fonction def alpha_eod) ainsi que certains paramètres
que l'on va aller chercher comme le volume, ie rajout le volume dans data.columns (fonction def alpha_eod)

"""
"""
import sys
sys.path.extend([WORKING_DIR_AND_PYTHON_PATHS])
"""
import sys

sys.path.insert(1, '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages')


import numpy as np
import importlib as lib
import backtrader as bt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
import pandas as pd
import numpy as np
from datetime import datetime
from strategies import *
import csv
import pdb

"""
    Variables to declare
"""

Apikey = 'LH73HGZGW450E7DZ'
symbol_list = ['AUDUSD']
strategy_to_test = RSI #Stratégie à tester
optimize = True #dire si on optimise ou pas
date_debut = [2012, 4, 20]  # date debut in_sample
date_fin = [2014, 11, 7]  # date fin in sample
initial_cash = 10000  # cash départ dans backtrader
stake_ = 3000  # grosseur des trades as size does indeed matter



"""
Ici on incorpore la base de données dans la liste data à partir du package alpha-vantage
La fonction est faite pour importer les données Forex, mais peut être modifiée pour importer d'autres catégories
d'actifs
"""

"""

def alpha_vantage_eod(symbol_list,compact=False, debug=False, *args, **kwargs):
    '''
    Helper function to download Alpha Vantage Data.

    This will return a nested list with each entry containing:
        [0] pandas dataframe
        [1] the name of the feed.

     Params asset_type is for the asset type (currency, stock, etc.), MUST RIGHT AVAILABLE LIST HERE
    '''
    data_list = list()
    size = 'compact' if compact else 'full'

    for symbol in symbol_list:


        if debug:
            print('Downloading: {}, Size: {}'.format(symbol, size))


        # Submit our API and create a session = pour les devises
        ts = ForeignExchange(key=Apikey, output_format='pandas')
        data, _ = ts.get_currency_exchange_daily(from_symbol=symbol[0:3], to_symbol=symbol[3:6], outputsize=size)


        data.index = pd.to_datetime(data.index)
        data = data[::-1]
        data.columns = ['Open', 'High', 'Low', 'Close']

        if debug:
            print(data)

        data_list.append((data, symbol))

    return data_list


data_list = alpha_vantage_eod(
    symbol_list,
    compact=False,
    debug=False)


for i in range(len(data_list)):

    data = bt.feeds.PandasData(
                dataname=data_list[i][0], # This is the Pandas DataFrame
                name=data_list[i][1], # This is the symbol
                timeframe=bt.TimeFrame.Days,
                compression=1,
                fromdate=datetime(date_debut[0],date_debut[1],date_debut[2]),
                todate=datetime(date_fin[0],date_fin[1],date_fin[2]),
                )


#Add the data to Cerebro

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    # Add a strategy (si on optimise)
    if optimize :
        RSI.params.printlog=False
        strats = cerebro.optstrategy(
            strategy_to_test,
            period=st.params.period_range,
            lowerband=st.params.lowerband_range,
            upperband=st.params.upperband_range,
            )
    # Add a strategy (si on n'optimise pas)
    else:
        RSI.params.printlog = True
        cerebro.addstrategy(strategy_to_test)

    cerebro.broker.setcash(initial_cash)

    # Add the data to Cerebro
    cerebro.adddata(data)

    # Default position size,
    cerebro.addsizer(bt.sizers.SizerFix, stake=stake_)

    cerebro.broker.setcommission(commission=0.001)

    # Run Cerebro Engine
    start_portfolio_value = cerebro.broker.getvalue()

    end_portfolio_value = cerebro.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value
    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    if optimize:
        cerebro.run(maxcpus=1)
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    else:
        cerebro.run()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.plot(volume=False) #le plot ne fonctionnne pas si on optimise
    # Print out the final result

"""
