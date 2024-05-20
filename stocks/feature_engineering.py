# feature_engineering.py

# imports
from finta import TA
import pandas as pd
import warnings
from multiprocessing import Pool

def add_features(signals_df, reward, risk): 

    # Ignore FutureWarnings related to Pandas data type compatibility
    warnings.filterwarnings("ignore", category=FutureWarning)
    # Disable the chained_assignment warning
    pd.options.mode.chained_assignment = None  # "None" suppresses the warning
    
    longest_MA_window = 200
    signals_df["9EMA"] = TA.EMA(signals_df, 9)
    signals_df["20EMA"] = TA.EMA(signals_df, 20)
    signals_df["50EMA"] = TA.EMA(signals_df, 50)
    signals_df["200SMA"] = TA.SMA(signals_df, longest_MA_window)
    signals_df["ATR"] = TA.ATR(signals_df)
    bbands_df = TA.BBANDS(signals_df)
    macd_df = TA.MACD(signals_df)
    signals_df["RSI"] = TA.RSI(signals_df)
    bbands_df = pd.concat([bbands_df, macd_df], axis=1)
    signals_df = pd.concat([signals_df, bbands_df], axis=1)
    signals_df.drop(columns=["SIGNAL", "BB_MIDDLE"], inplace=True)
    
    signals_df["Entry Price"] = float(0)
    signals_df["Entry Time"] = pd.Timestamp(0)
    signals_df["Exit Price"] = float(0)
    signals_df["Exit Time"] = pd.Timestamp(0)
    signals_df["Exit"] = 0
    
    nyse_opening_time = pd.Timestamp("09:30:00")
    nyse_closing_time = pd.Timestamp("16:00:00")
    signals_df = signals_df.between_time(nyse_opening_time.time(), nyse_closing_time.time())
    
    num_rows_in_df = signals_df.shape[0]
    
    # reward:risk ratio
    reward = reward
    risk = risk
    
    rows = [(j, signals_df["close"].iloc[j], signals_df.index[j], signals_df["ATR"].iloc[j], signals_df, num_rows_in_df, risk, reward) for j in range(longest_MA_window, num_rows_in_df)]
    
    # Number of processes
    num_processes = 4  # Adjust according to your system resources
    
    # Create a pool of processes
    pool = Pool(num_processes)
    
    # Parallelize the processing of rows and collect results
    results = pool.map(process_row, rows)

    
    # Close the pool
    pool.close()
    pool.join()
    
    ### FAST VERSION WIP
    # # Merge results back into signals_df
    # for result in results:
    #     j, entry_price, entry_time, exit_price, exit_signal, exit_time = result
    #     signals_df.at[j, "Entry Price"] = entry_price
    #     signals_df.at[j, "Entry Time"] = entry_time
    #     signals_df.at[j, "Exit Price"] = exit_price
    #     signals_df.at[j, "Exit"] = exit_signal
    #     signals_df.at[j, "Exit Time"] = exit_time
        
    # Merge results back into signals_df
    for result in results:
        j, entry_price, entry_time, exit_price, exit_signal, exit_time = result
        signals_df["Entry Price"].iloc[j] = entry_price
        signals_df["Entry Time"].iloc[j] = entry_time
        signals_df["Exit Price"].iloc[j] = exit_price
        signals_df["Exit"].iloc[j] = exit_signal
        signals_df["Exit Time"].iloc[j] = exit_time
        
    print(signals_df)
    return signals_df

    
def process_row(row):
    j, entry_price, entry_time, atr, signals_df, num_rows_in_df, risk, reward = row
    
    exit_price = 0
    exit_signal = 0
    exit_time = pd.Timestamp(0)
    
    stop = entry_price - (risk * atr)
    target = entry_price + (reward * atr)
    
    for k in range(j + 1, num_rows_in_df):
        curr_low = signals_df["low"].iloc[k]
        curr_high = signals_df["high"].iloc[k]
        if curr_low <= stop:
            exit_price = stop
            exit_signal = -1
            exit_time = signals_df.index[k]
            # print("stop")
            break
        elif curr_high >= target:
            exit_price = target
            exit_signal = 1
            exit_time = signals_df.index[k]
            # print("target")
            break
    
    return (j, entry_price, entry_time, exit_price, exit_signal, exit_time)

    
def clean_data(signals_df):
    ## Data Cleaning

    # remove all unwanted zeros from the exit column
    signals_df = signals_df.loc[signals_df["Exit"] != 0]
    # signals_df = signals_df[signals_df["volume"] >= signals_df["volume"].mean()]
    return signals_df