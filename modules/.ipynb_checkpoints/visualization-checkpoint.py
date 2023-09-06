# visualization.py

import pandas as pd
import matplotlib.pyplot as plt 

def record_metrics(signals_df, testing_signal_predictions, testing_probability_estimates, X_test_index, reward, risk, results):

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
    
    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################
    
    # Calculate the time period for which you want to calculate the frequency (e.g., in days)
    start_date = buy_signals_df.index.min()
    end_date = buy_signals_df.index.max()
    time_period_days = (end_date - start_date).days + 1  # Adding 1 to include both start and end dates
    
    # Filter the winning, losing, and total trades
    winning_trades = buy_signals_df[buy_signals_df['trading_algorithm_returns'] > 0]
    losing_trades = buy_signals_df[buy_signals_df['trading_algorithm_returns'] < 0]
    total_trades = buy_signals_df["trading_algorithm_returns"]
    
    # Calculate gross profit (positive returns) and gross loss (negative returns)
    gross_profit = buy_signals_df[buy_signals_df['trading_algorithm_returns'] > 0]['trading_algorithm_returns'].sum() * 100
    gross_loss = buy_signals_df[buy_signals_df['trading_algorithm_returns'] < 0]['trading_algorithm_returns'].sum() * 100
    
    # Calculate the average return of your trading strategy
    average_return = buy_signals_df['trading_algorithm_returns'].mean()
    
    # Calculate the risk-free rate (e.g., Treasury bill rate)
    # You need to specify an appropriate risk-free rate for your analysis
    risk_free_rate = 0.02  # Replace with the risk-free rate you want to use (e.g., 2% for a Treasury bill)
    
    # Calculate downside returns (negative returns)
    downside_returns = buy_signals_df['trading_algorithm_returns'][buy_signals_df['trading_algorithm_returns'] < 0]
    
    # Calculate the downside deviation (standard deviation of negative returns)
    downside_deviation = (downside_returns * 100).std()
    
    # Calculate the Risk:Reward Ratio
    risk_reward_ratio= reward/risk
    
    # Calculate the win rate (if you haven't already)
    win_rate = len(winning_trades) / len(total_trades)
    
    # Calculate the profit factor
    profit_factor = abs(gross_profit / gross_loss)
    
    # Calculate the Sortino Ratio
    sortino_ratio = (average_return - risk_free_rate) / downside_deviation
    
    # Calculate the average profit per winning trade
    average_profit_per_winning_trade = winning_trades['trading_algorithm_returns'].mean()
    
    # Calculate the average loss per losing trade
    average_loss_per_losing_trade = losing_trades['trading_algorithm_returns'].mean()
    
    # Calculate the trade frequency (trades per day)
    trade_frequency_per_day = len(total_trades) / time_period_days
    
    # Calculate the volatility of your trading strategy's returns
    algo_volatility = buy_signals_df['trading_algorithm_returns'].std()
    
    # Calculate cumulative returns for the algorithmic trading strategy
    cumulative_returns = (1 + buy_signals_df["trading_algorithm_returns"]).cumprod()[-1]
    
    # Create a dictionary to hold the model;s metrics
    metrics_dict = {
    "Risk": risk,
    "Reward": reward,
    "Win Rate (%)": win_rate * 100,
    "Profit Factor": profit_factor,
    "Cumulative Returns": cumulative_returns,
    "Sortino Ratio": sortino_ratio,
    "Average Profit per Winning Trade (%)": average_profit_per_winning_trade * 100,
    "Average Loss per Losing Trade (%)": average_loss_per_losing_trade * 100,
    "Average Return (%)": average_return * 100,
    "Trade Frequency (Trades per Day)": trade_frequency_per_day,
    "Downside Deviation": downside_deviation,
    "Volatility (Standard Deviation of Algo Returns)": algo_volatility,
    "Gross Profit (%)": gross_profit,
    "Gross Loss (%)": gross_loss,
    "Total Number of Winning Trades": len(winning_trades),
    "Total Number of Trades": len(total_trades),
    "Risk-Free Rate (%)": risk_free_rate * 100,
    "Risk:Reward Ratio": risk_reward_ratio,
}
    
    results.append(metrics_dict)

    return results
        
