# evaluation.py

# imports
import pandas as pd


def record_sim_trades(signals_df, testing_signal_predictions, testing_probability_estimates, X_test_index, prob):
    # Create a predictions DataFrame for SVM
    predictions_df = pd.DataFrame(index=X_test_index)
    
    predictions_df["predicted_signal"] = testing_signal_predictions
    
    predictions_df["actual_returns"] = signals_df["close"].pct_change()
    
    #####################
    
    predictions_df[["Entry Price", "Entry Time", "Exit Price", "Exit Time"]] = signals_df[["Entry Price", "Entry Time", "Exit Price", "Exit Time"]]
    
    ####################
    
    predictions_df["algo_returns"] = (signals_df["Exit Price"] - signals_df["Entry Price"])/signals_df["Entry Price"]
    
    predictions_df["trading_algorithm_returns"] = predictions_df.pop("algo_returns") * predictions_df["predicted_signal"]
    
    predictions_df["probability_estimates"] = testing_probability_estimates[:, 1]
    
    # Initialize buy_signals_df
    buy_signals_df = pd.DataFrame()
    buy_signals_df = pd.concat([buy_signals_df, predictions_df.iloc[[0]]])
    
    # Loop to execute one buy trade at a time
    # Initialize the last trade exit time with the first row's exit time
    last_trade_exit_time = predictions_df["Exit Time"].iloc[0]
    
    # Iterate through the DataFrame to find entry points for buy trades
    for j in range(1, predictions_df.shape[0]):
        # Get the entry time and exit signal for the current row
        entry_time = predictions_df["Entry Time"].iloc[j]
        exit_signal = predictions_df["predicted_signal"].iloc[j]
        # Check if the current entry time is before or equal to the last trade's exit time
        # or if the exit signal is -1; if so, skip this iteration
        if entry_time <= last_trade_exit_time or exit_signal == -1:
            continue
        else:
            # Concatenate the current row to the buy_signals_df DataFrame
            buy_signals_df = pd.concat([buy_signals_df, predictions_df.iloc[[j]]])
            # Update the last trade exit time with the current row's exit time
            last_trade_exit_time = predictions_df["Exit Time"].iloc[j]
    
    # # Filter rows where the predicted signal is 1 and the probability estimate is >= prob
    buy_signals_df = buy_signals_df[(buy_signals_df["probability_estimates"] >= (prob/100))]
    
    # Calculate cumulative returns for both strategies
    cumulative_algo_returns = buy_signals_df.loc[:, "trading_algorithm_returns"]
    cumulative_algo_returns = 1 + cumulative_algo_returns
    buy_signals_df.loc[:, "Cumulative Algo Returns"] = cumulative_algo_returns.cumprod()

    cumulative_actual_returns = predictions_df.loc[:, "actual_returns"]
    cumulative_actual_returns = 1 + cumulative_actual_returns
    buy_signals_df.loc[:, "Cumulative Actual Returns"] = cumulative_actual_returns.cumprod()

    return buy_signals_df
    
    
    
