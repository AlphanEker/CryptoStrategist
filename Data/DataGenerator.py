import pandas as pd
import ta

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

# Write the data with RSI to a new CSV file
data.to_csv(output_file_path, index=False)

print("CSV file with RSI has been processed and saved as:", output_file_path)
