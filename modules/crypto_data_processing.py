# data_processing.py

# imports
import alpaca_trade_api as tradeapi
import pandas as pd 
from datetime import datetime
import alpaca
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from dateutil.relativedelta import relativedelta



def download_data(ticker, timeframeValue, start_date):
    # THE FOLLOWING IS TO REQUEST IN DATA USING THE ALPACA_API
    # API credentials
    API_KEY = 'PKD98H4EZF8YRDLUZ5I2'
    SECRET_KEY = 'b5ZbNnx35m3uaB6vRnrU7TLQlgEfDw0bKf1Y8Zsm'
    API_BASE_URL = "https://paper-api.alpaca.markets"
    
    ticker = ticker
    time_diff = datetime.now() - relativedelta(months=start_date)
    
    # Alpaca Market Data Client
    data_client = CryptoHistoricalDataClient()
    
    # Defining Bar data request parameters
    request_params = CryptoBarsRequest(
        symbol_or_symbols=[ticker],
        timeframe=TimeFrame(timeframeValue, alpaca.data.timeframe.TimeFrameUnit.Minute),
        start=time_diff
    )
    
    # Get the bar data from Alpaca
    signals_df = data_client.get_crypto_bars(request_params).df
    
    signals_df.reset_index(level='symbol', inplace=True)
    signals_df.drop(columns=["symbol"], inplace=True)

    # Save the DataFrame with the date index
    signals_df.to_csv(f'./data/ETH/ETH_{timeframeValue}_time_series_df.csv')
    
    return signals_df


def read_data(ticker, timeframe):
# Load the DataFrame from a CSV file
    signals_df = pd.read_csv(f'./data/ETH/ETH_{timeframe}_time_series_df.csv', index_col="timestamp")
    
    # Convert the first column (assuming it contains datetime-like values) to DatetimeIndex
    signals_df.index = pd.to_datetime(signals_df.index)
    
    return signals_df
    