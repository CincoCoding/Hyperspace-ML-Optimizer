# data_processing.py

# imports
import alpaca_trade_api as tradeapi
import pandas as pd 


def download_data():
    # THE FOLLOWING IS TO REQUEST IN DATA USING THE ALPACA_API
    # API credentials
    API_KEY = 'PKETI0Q5C8PPUXVNHJFJ'
    SECRET_KEY = 'WQxmEpBCoMXydCCg0G8cUe6hGLpgaAfrvedZ09Fy'
    API_BASE_URL = "https://paper-api.alpaca.markets"
    
    # Create a connection to the API 
    api = tradeapi.REST(API_KEY, SECRET_KEY, API_BASE_URL, api_version="v2")
        
    # Set the ticket symbol and the number of shares to buy
    ticker = "AAPL"
    
    # Make API call
    signals_df = api.get_bars(ticker, "5Min", "2022-01-01", "2023-08-30", adjustment='raw').df
    
#     # Save the DataFrame with the date index
#     signals_df.to_csv('signals_df.csv')
    
    print(signals_df.head())
    
    return signals_df



def read_data():
# Load the DataFrame from a CSV file
    signals_df = pd.read_csv('./data/signals_df.csv', index_col="timestamp")
    
    # Convert the first column (assuming it contains datetime-like values) to DatetimeIndex
    signals_df.index = pd.to_datetime(signals_df.index)
    
    return signals_df
    