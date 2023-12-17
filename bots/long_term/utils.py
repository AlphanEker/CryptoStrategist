import os
import math
import logging

import pandas as pd
import numpy as np

import keras.backend as K

# Formats Position
format_position = lambda price: ('-$' if price < 0 else '+$') + '{0:.2f}'.format(abs(price))

# Formats Currency
format_currency = lambda price: '${0:.2f}'.format(abs(price))


def show_train_result(result, val_position, initial_offset):
    """ Displays training results
    """
    if val_position == initial_offset or val_position == 0.0:
        logging.info('Episode {}/{} - Train Position: {}  Val Position: USELESS  Train Loss: {:.4f}'
                     .format(result[0], result[1], format_position(result[2]), result[3]))
    else:
        logging.info('Episode {}/{} - Train Position: {}  Val Position: {}  Train Loss: {:.4f})'
                     .format(result[0], result[1], format_position(result[2]), format_position(val_position),
                             result[3], ))


def show_eval_result(model_name, profit, initial_offset):
    """ Displays eval results
    """
    if profit == initial_offset or profit == 0.0:
        logging.info('{}: USELESS\n'.format(model_name))
    else:
        logging.info('{}: {}\n'.format(model_name, format_position(profit)))


def get_stock_data(stock_file):
    """Reads stock data from csv file and returns a 2D array with selected columns."""
    df = pd.read_csv(stock_file)

    # Specify the columns you want to include
    selected_columns = ['close', 'high', 'low', 'volume', 'count', 'RSI', 'Stoch_%K', 'Stoch_%D', 'CCI', 'ADL', 'MFI',
                        'CMF', 'Bollinger_Mavg', 'Bollinger_Hband', 'Bollinger_Lband', 'Bollinger_Hband_Indicator',
                        'Bollinger_Lband_Indicator', 'ATR', 'MACD', 'MACD_Signal', 'MACD_Diff', 'Aroon_Up',
                        'Aroon_Down', 'Ichimoku_A', 'Ichimoku_B', 'Ichimoku_Base_Line', 'Cumulative_Return']

    # Check if all selected columns are present in the DataFrame
    for col in selected_columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in the stock data")

    # Return the data as a 2D array (numpy array)
    return df[selected_columns].values

