# main.py

# import libraries
import pandas as pd
from modules import config
from modules import dependencies

# import functions and classes
from modules.modeling import train_model
from modules.evaluation import evaluate_model
from modules.prob_simulate import record_sim_trades
from modules.prob_metrics import record_sim_metrics

def main():
    
    # Define a range of values for risk and reward
    reward = 10
    risk = 8

    probability_range = range(50, 78)
    
    results = []

    # Load the DataFrame from a CSV file
    cleaned_data = pd.read_csv('./notebook/AAPL_time_series.csv', index_col="timestamp")
    cleaned_data = cleaned_data.iloc[ : , 1: ]
    
    # Convert the first column (assuming it contains datetime-like values) to DatetimeIndex
    cleaned_data.index = pd.to_datetime(cleaned_data.index)
    
    for prob in probability_range:
        # Your program's main logic here
        print(f"train_model(), Reward = {reward}, Risk = {risk}")
        model, X_train, X_test, y_train, y_test, X_test_index = train_model(cleaned_data)
        
        print(f"evaluate_model(), Reward = {reward}, Risk = {risk}")
        predictions, prediction_probabilities = evaluate_model(model, X_train, X_test, y_train, y_test)
        
        # print(f"record_trades_and_metrics(), Reward = {reward}, Risk = {risk}")
        # results = record_trades_and_metrics(data_with_features, predictions, prediction_probabilities, X_test_index, reward, risk, results)
        
        print(f"record_sim_trades(), Reward = {reward},  Risk = {risk}")
        buy_signals_df = record_sim_trades(cleaned_data, predictions, prediction_probabilities, X_test_index, prob)
        
        print(f"record_sim_metrics(), Reward = {reward}, Risk = {risk}")
        results = record_sim_metrics(buy_signals_df, reward, risk, results, prob)
        
        print(results, len(results))

    
    results_df = pd.DataFrame(results)
    results_df.to_csv("./results_df_AAPL_prob.csv")



if __name__ == "__main__":
    main()
    