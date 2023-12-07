import pandas as pd
import ta
import numpy as np

# File paths
input_file_path = 'DOGEUSDT-1m-2021-02.csv'  # Replace with your input file path
output_file_path = 'LFTData.csv'  # Replace with your desired output file path

# Define the headers
headers = [
    "open-time", "open", "high", "low", "close", "volume",
    "close-time", "quote-volume", "count", "taker-buy-volume",
    "taker-buy-quote-volume", "ignore"
]

# Read the CSV file
data = pd.read_csv(input_file_path, header=None, names=headers)

# MOMENTUM INDICATORS

# Calculate RSI
# You can adjust the window period (14 is standard for RSI)
rsi_window = 18 # 7 for hft 18 for lft
data['RSI'] = ta.momentum.RSIIndicator(data['close'], window=rsi_window).rsi()

# Stochastic Oscillator
stoch_window = 18 # 7 for hft 18 for lft (also smooth window 4 for lft)
stoch = ta.momentum.StochasticOscillator(high=data['high'], low=data['low'], close=data['close'], window=stoch_window, smooth_window=3)
data['Stoch_%K'] = stoch.stoch()
data['Stoch_%D'] = stoch.stoch_signal()

# Commodity Channel Index (CCI)
cci_window = 30 # 13 for hft 30 for lft
data['CCI'] = ta.trend.CCIIndicator(high=data['high'], low=data['low'], close=data['close'], window=cci_window).cci()

# VOLUME INDICATORS

# Accumulation/Distribution Line (ADL)
data['ADL'] = ta.volume.AccDistIndexIndicator(high=data['high'], low=data['low'], close=data['close'], volume=data['volume']).acc_dist_index()

# Money Flow Index (MFI)
mfi_window = 18 # 7 for hft 18 for lft
data['MFI'] = ta.volume.MFIIndicator(high=data['high'], low=data['low'], close=data['close'], volume=data['volume'], window=mfi_window).money_flow_index()

# Chaikin Money Flow (CMF)
cmf_window = 30 # 7 for hft 30 for lft
data['CMF'] = ta.volume.ChaikinMoneyFlowIndicator(high=data['high'], low=data['low'], close=data['close'], volume=data['volume'], window=cmf_window).chaikin_money_flow()

# VOLATILITY INDICATORS

# Bollinger Bands
bollinger_window = 20 # 10 for hft 20 for lft
bollinger_std_dev = 2
bollinger = ta.volatility.BollingerBands(close=data['close'], window=bollinger_window, window_dev=bollinger_std_dev)
data['Bollinger_Mavg'] = bollinger.bollinger_mavg()
data['Bollinger_Hband'] = bollinger.bollinger_hband()
data['Bollinger_Lband'] = bollinger.bollinger_lband()
data['Bollinger_Hband_Indicator'] = bollinger.bollinger_hband_indicator()
data['Bollinger_Lband_Indicator'] = bollinger.bollinger_lband_indicator()

# Average True Range (ATR)
atr_window = 18 # 8 for hft 18 for lft
data['ATR'] = ta.volatility.AverageTrueRange(high=data['high'], low=data['low'], close=data['close'], window=atr_window).average_true_range()


# TREND INDICATORS

# Calculate MACD
macd = ta.trend.MACD(data['close'])
data['MACD'] = macd.macd()
data['MACD_Signal'] = macd.macd_signal()
data['MACD_Diff'] = macd.macd_diff()  # This is the MACD histogram

# Calculate Aroon
aroon_window = 25  # 12 for hft 25 for lft
aroon_indicator = ta.trend.AroonIndicator(data['high'], data['low'], window=aroon_window)
data['Aroon_Up'] = aroon_indicator.aroon_up()
data['Aroon_Down'] = aroon_indicator.aroon_down()

# Ichimoku Cloud Calculation

ichimoku = ta.trend.IchimokuIndicator(high=data['high'], low=data['low'])
data['Ichimoku_A'] = ichimoku.ichimoku_a()
data['Ichimoku_B'] = ichimoku.ichimoku_b()
data['Ichimoku_Base_Line'] = ichimoku.ichimoku_base_line()
data['Ichimoku_Conversion_Line'] = ichimoku.ichimoku_conversion_line()


# OTHER INDICATORS

# Calculate Cumulative Returns
data['Cumulative_Return'] = data['close'].pct_change().fillna(0).add(1).cumprod().sub(1)




# Write the data with RSI to a new CSV file
data.to_csv(output_file_path, index=False)

print("CSV file with RSI has been processed and saved as:", output_file_path)
