import pandas as pd
import ta
import numpy as np

# File paths
input_file_path = 'DOGEUSDT-1m-2021-02.csv'  # Replace with your input file path
output_file_path = 'FebruaryDogeModified.csv'  # Replace with your desired output file path

# Define the headers
headers = [
    "open-time", "open", "high", "low", "close", "volume",
    "close-time", "quote-volume", "count", "taker-buy-volume",
    "taker-buy-quote-volume", "ignore"
]

# Read the CSV file
data = pd.read_csv(input_file_path, header=None, names=headers)

# Calculate RSI
# You can adjust the window period (14 is standard for RSI)
rsi_window = 14
data['RSI'] = ta.momentum.RSIIndicator(data['close'], window=rsi_window).rsi()

# Calculate MACD
macd = ta.trend.MACD(data['close'])
data['MACD'] = macd.macd()
data['MACD_Signal'] = macd.macd_signal()
data['MACD_Diff'] = macd.macd_diff()  # This is the MACD histogram

# Calculate Aroon
aroon_window = 25  # Default window for Aroon
aroon_indicator = ta.trend.AroonIndicator(data['high'], data['low'], window=aroon_window)
data['Aroon_Up'] = aroon_indicator.aroon_up()
data['Aroon_Down'] = aroon_indicator.aroon_down()

# Ichimoku Cloud Calculation
try:
    ichimoku = ta.trend.IchimokuIndicator(high=data['high'], low=data['low'])
    data['Ichimoku_A'] = ichimoku.ichimoku_a()
    data['Ichimoku_B'] = ichimoku.ichimoku_b()
    data['Ichimoku_Base_Line'] = ichimoku.ichimoku_base_line()
    data['Ichimoku_Conversion_Line'] = ichimoku.ichimoku_conversion_line()
except TypeError as e:
    print("Error initializing IchimokuIndicator:", e)

# Dynamic Fibonacci Retracement Levels
window_size = 60  # Define your window size for high and low (120 default, I reduced it to 60 in order to catch smaller trends)

def find_fibonacci_levels(data):
    highs = data['high'].rolling(window=window_size).max()
    lows = data['low'].rolling(window=window_size).min()
    diff = highs - lows
    data['Fib_23.6'] = highs - diff * 0.236
    data['Fib_38.2'] = highs - diff * 0.382
    data['Fib_61.8'] = highs - diff * 0.618
    data['Fib_78.6'] = highs - diff * 0.786
    return data

data = find_fibonacci_levels(data)

# Write the data with RSI to a new CSV file
data.to_csv(output_file_path, index=False)

print("CSV file with RSI has been processed and saved as:", output_file_path)
