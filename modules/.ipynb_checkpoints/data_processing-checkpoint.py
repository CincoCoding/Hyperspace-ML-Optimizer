# data_processing.py

# imports
import alpaca_trade_api as tradeapi
import pandas as pd 


def download_data(ticker, timeframe, start_date):
    # THE FOLLOWING IS TO REQUEST IN DATA USING THE ALPACA_API
    # API credentials
    API_KEY = 'PKD98H4EZF8YRDLUZ5I2'
    SECRET_KEY = 'b5ZbNnx35m3uaB6vRnrU7TLQlgEfDw0bKf1Y8Zsm'
    API_BASE_URL = "https://paper-api.alpaca.markets"
    
    # Create a connection to the API 
    api = tradeapi.REST(API_KEY, SECRET_KEY, API_BASE_URL, api_version="v2")
        
    # Set the ticket symbol and the number of shares to buy
    ticker = ticker
    
    # Make API call
    signals_df = api.get_bars(ticker, {timeframe}, {start_date}, "2023-08-30", adjustment='raw').df
    
    # Save the DataFrame with the date index
    signals_df.to_csv(f'./data/{ticker}/{ticker}_{timeframe}_time_series_df.csv')
    
    print(signals_df.head())
    
    return signals_df



    