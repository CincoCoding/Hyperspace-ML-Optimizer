# visualization.py

import pandas as pd
import matplotlib.pyplot as plt 

def plot_results(signals_df, testing_signal_predictions, testing_probability_estimates, X_test_index):
    # Create a predictions DataFrame
    
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
    
    # Calculate cumulative returns for the algorithmic trading strategy
    buy_signals_df["Cumulative Algo Returns"] = (1 + buy_signals_df["trading_algorithm_returns"]).cumprod()
    
    # Calculate cumulative returns for the actual stock returns
    predictions_df["Cumulative Actual Returns"] = (1 + predictions_df["actual_returns"]).cumprod()
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(buy_signals_df.index, buy_signals_df["Cumulative Algo Returns"], label="Algorithm Returns (Buy Signals)")
    plt.plot(predictions_df.index, predictions_df["Cumulative Actual Returns"], label="Actual Returns")
    plt.xlabel("Date") 
    plt.ylabel("Cumulative Returns")
    plt.title("Cumulative Returns of Algorithm vs. Actual Returns")
    plt.legend()
    plt.grid(True)
    plt.show()
