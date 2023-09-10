# feature_engineering.py

# imports
from finta import TA
import pandas as pd 


def add_features(signals_df, reward, risk):
    ### Add Features (Techincal Analysis Indicators) to the DataFrame
    
    #  Setup EMAs for crosses
    longest_MA_window = 200
    signals_df["9EMA"] = TA.EMA(signals_df, 9)
    signals_df["20EMA"] = TA.EMA(signals_df, 20)
    signals_df["50EMA"] = TA.EMA(signals_df, 50)
    signals_df["200SMA"] = TA.SMA(signals_df, longest_MA_window)
    
    # Setup Indicators
    signals_df["ATR"] = TA.ATR(signals_df)
    bbands_df = TA.BBANDS(signals_df)
    macd_df = TA.MACD(signals_df)
    signals_df["RSI"] = TA.RSI(signals_df)
    
    # join macd and bbands Dataframes to signals_df
    bbands_df = pd.concat([bbands_df, macd_df], axis=1)
    signals_df = pd.concat([signals_df, bbands_df], axis=1)
    signals_df.drop(columns="SIGNAL", inplace=True)
    
    
    ### Add Discrete Features Columns to the DataFrame

    # discrete or continuous features (techinal indicators) may be used
    continuous_features = ["volume", "trade_count", "vwap", "9EMA", "20EMA", "50EMA", "200SMA", "ATR", "RSI", "BB_UPPER", "BB_LOWER", "MACD"]
    all_features = ["volume", "trade_count", "vwap", "9EMA", "20EMA", "50EMA", "200SMA", "ATR", "RSI", "BB_UPPER", "BB_MIDDLE", "BB_LOWER", "MACD", "Bollinger_Bands_Above_Upper_BB", "Bollinger_Bands_Below_Lower_BB", "9EMA/20EMA_Cross, 9EMA>20EMA", "9EMA/20EMA_Cross, 9EMA<20EMA", "50EMA/200SMA_Cross, 50EMA>200SMA", "50EMA/200SMA_Cross, 50EMA<200SMA", "RSI_Over_70", "RSI_Under_30", "VWAP_Cross_From_Above", "VWAP_Cross_From_Below"]
    
    # Exit is the labeled target for ML, Exit Price is for use in Pnl Metrics
    signals_df["Exit Price"] = float(0)
    signals_df["Exit"] = 0

    # # Define NYSE regular trading hours
    # nyse_opening_time = pd.Timestamp("09:30:00")
    # nyse_closing_time = pd.Timestamp("16:00:00")
    
    # # Filter the DataFrame to include only data within NYSE regular trading hours
    # signals_df = signals_df.between_time(nyse_opening_time.time(), nyse_closing_time.time())
       
        
    ### Create Volatility Based Targets and Stops

    # here we create the exit column, our "y", for use in supervised ML
    # How many rows are in the signals_df? for use in modifying DataFrame
    num_rows_in_df = signals_df.shape[0]
    
    # reward:risk ratio
    reward = reward
    risk = risk
    
    # we also figure out our exit price
    # hitting target price before the stop price signals a win and will be 1
    # hitting stop price before hitting the target price signals a loss and will be -1
    # loop thru the dataframe, from the longest_MA_window to the end (num_rows_in_df) to avoid NaN values
    for j in range(longest_MA_window, num_rows_in_df):
        # entries will be on candle close
        entry = signals_df["close"].iloc[j]
        # calculate volatility for each candle
        atr = signals_df["ATR"].iloc[j]
        # stop is entry price minus the average volatility for the entry period
        stop = float(entry - (risk * atr))
        # target is entry price plus the average volatility for the entry period times a multiplier
        target = float(entry + (reward * atr))
        # loop again thru the dataset to compare j entry price to future closing prices to see if we hit target or stop
        for k in range(j + 1, num_rows_in_df):
            # current low of the candle
            curr_low = signals_df["low"].iloc[k]
            # current high of the candle
            curr_high = signals_df["high"].iloc[k]
            # record and break if we hit stop or target, if not we check the next k period
            # if current low breaks our stop we should've sold: -1 in our "Exit" column
            if curr_low <= stop:
                signals_df.iloc[j, -2] = stop
                signals_df.iloc[j, -1] = -1
                # if we hit the stop break the inner loop to check the next row
                break
            # if current high breaks our target we should've sold: +1 in our "Exit" column
            elif curr_high >= target:
                signals_df.iloc[j, -2] = target
                signals_df.iloc[j, -1] = 1
                # if we hit the target break the inner loop to check the next row
                break
        
    # drop beginning columns to avoid NaN values from EMA/SMA calculations
    signals_df = signals_df[longest_MA_window:]
    
    return signals_df
    
    
    
def clean_data(signals_df):
    # Data Cleaning
    # remove all unwanted zeros from the exit column
    signals_df = signals_df.loc[signals_df["Exit"] != 0]
    
    # signals_df = signals_df[signals_df["volume"] >= signals_df["volume"].mean()]

    return signals_df