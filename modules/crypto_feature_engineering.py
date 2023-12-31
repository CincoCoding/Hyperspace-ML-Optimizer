# feature_engineering.py

# imports
from finta import TA
import pandas as pd 


def add_features(signals_df, reward, risk):
    
    import warnings
    # Ignore FutureWarnings related to Pandas data type compatibility
    warnings.filterwarnings("ignore", category=FutureWarning)
    # Disable the chained_assignment warning
    pd.options.mode.chained_assignment = None  # "None" suppresses the warning

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
    signals_df.drop(columns=["SIGNAL","BB_MIDDLE"], inplace=True)
    
    # Exit is the labeled target for ML, Exit Price is for use in Pnl Metrics
    signals_df["Entry Price"] = float(0)
    signals_df["Entry Time"] = pd.Timestamp(0)
    
    signals_df["Exit Price"] = float(0)
    signals_df["Exit Time"] = pd.Timestamp(0)
    signals_df["Exit"] = 0
    
    ### Add Discrete Features Columns to the DataFrame
        
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
        signals_df["Entry Price"].iloc[j] = entry
        signals_df["Entry Time"].iloc[j] = signals_df.index[j]
        # calculate volatility for each candle
        atr = signals_df["ATR"].iloc[j]
        # stop is entry price minus the average volatility for the entry period
        stop = entry - (risk * atr)
        # target is entry price plus the average volatility for the entry period times a multiplier
        target = entry + (reward * atr)
        # loop again thru the dataset to compare j entry price to future closing prices to see if we hit target or stop
        for k in range(j + 1, num_rows_in_df):
            # current low of the candle
            curr_low = signals_df["low"].iloc[k]
            # current high of the candle
            curr_high = signals_df["high"].iloc[k]
            # record and break if we hit stop or target, if not we check the next k period
            # if current low breaks our stop we should've sold: -1 in our "Exit" column
            if curr_low <= stop:
                signals_df["Exit Price"].iloc[j] = stop
                signals_df["Exit"].iloc[j] = -1
                # record exit time
                signals_df["Exit Time"].iloc[j] = signals_df.index[k] 
                # if we hit the stop break the inner loop to check the next row
                break
            # if current high breaks our target we should've sold: +1 in our "Exit" column
            elif curr_high >= target:
                signals_df["Exit Price"].iloc[j] = target
                signals_df["Exit"].iloc[j] = 1
                # record exit time
                signals_df["Exit Time"].iloc[j] = signals_df.index[k] 
                # if we hit the target break the inner loop to check the next row
                break
    
    # drop beginning columns to avoid NaN values from EMA/SMA calculations
    signals_df = signals_df[longest_MA_window:]
    
    # Re-enable all warnings to their default behavior
    warnings.resetwarnings()   
    
    return signals_df
    
    
def clean_data(signals_df):
    # Data Cleaning
    # remove all unwanted zeros from the exit column
    signals_df = signals_df.loc[signals_df["Exit"] != 0]
    
    # include only higher than 1 volume
    signals_df = signals_df.loc[signals_df["volume"] != 0]
    return signals_df