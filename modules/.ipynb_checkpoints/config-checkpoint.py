# config.py

features = ["open", "high", "low", "close", "volume", "trade_count", "vwap", "9EMA", "20EMA", "50EMA", "200SMA", "ATR", "RSI", "BB_UPPER", "BB_LOWER", "MACD"]
# Define a range of values for risk and reward
risk_values = range(1, 11)  # Example risk values
reward_values = range(1, 11)  # Example reward values
ticker_values = ["SPY", "META", "AAPL", "AMZN", "NFLX", "GOOGL", "TSLA"]
# create a dictionary of timeframe values with corresponding date
timeframe_values = [["1min","2023-04-01", 3], ["5min", "2022-01-01", 14], ["15min", "2018-08-01", 42], ["30min", "2015-12-01", 60], ["1hour", "2015-12-01", 60], ["2hour", "2015-12-01", 60], ["4hour", "2015-12-01", 60]]

features = ["volume", "trade_count"]
# Define a range of values for risk and reward
risk_values = range(1, 3)  # Example risk values
reward_values = range(1, 3)  # Example reward values
ticker_values = ["SPY", "META"]
# create a dictionary of timeframe values with corresponding date
timeframe_values = [["1min","2023-04-01", 3], ["5min", "2022-01-01", 14]]