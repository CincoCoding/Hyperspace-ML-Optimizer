# evaluation.py

# imports
import pandas as pd


def record_sim_trades(signals_df, testing_signal_predictions, testing_probability_estimates, X_test_index):
    # Create a predictions DataFrame for SVM
    predictions_df = pd.DataFrame(index=X_test_index)
    
    predictions_df["predicted_signal"] = testing_signal_predictions
    
    predictions_df["actual_returns"] = signals_df["close"].pct_change()
    
    predictions_df["algo_returns"] = (signals_df["Exit Price"] - signals_df["close"])/signals_df["close"]
    
    
    predictions_df["trading_algorithm_returns"] = (
        predictions_df["algo_returns"] * predictions_df["predicted_signal"]
    )
    
    predictions_df = predictions_df.drop(columns=["algo_returns"])
    
    predictions_df["probability_estimates"] = testing_probability_estimates[:, 1]
    
    # Filter rows where the predicted signal is 1 and the probability estimate is >= 0.60
    buy_signals_df = predictions_df[(predictions_df["predicted_signal"] == 1) & (predictions_df["probability_estimates"] >= 0.50)]
    
    # Calculate cumulative returns for both strategies
    cumulative_algo_returns = buy_signals_df.loc[:, "trading_algorithm_returns"]
    cumulative_algo_returns = 1 + cumulative_algo_returns
    buy_signals_df.loc[:, "Cumulative Algo Returns"] = cumulative_algo_returns.cumprod()

    cumulative_actual_returns = predictions_df.loc[:, "actual_returns"]
    cumulative_actual_returns = 1 + cumulative_actual_returns
    buy_signals_df.loc[:, "Cumulative Actual Returns"] = cumulative_actual_returns.cumprod()

    return buy_signals_df
    
    
    
