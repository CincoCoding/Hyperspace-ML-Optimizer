# main.py

# import libraries
import pandas as pd
from modules import config
from modules import dependencies

# import functions and classes
from modules.data_processing import download_data, read_data
from modules.feature_engineering import add_features, clean_data
from modules.modeling import train_model
from modules.evaluation import evaluate_model
from modules.simulate import record_sim_trades
from modules.metrics import record_sim_metrics

def main():
    
    # Define a range of values for risk and reward
    risk_values = range(1, 11)  # Example risk values
    reward_values = range(1, 11)  # Example reward values
    ticker_values = ["SPY", "META", "AAPL", "AMZN", "NFLX", "GOOGL", "TSLA"]

    # create a dictionary of timeframe values with corresponding date
    timeframe_values = ["1min", "5min", "15min", "30min", "1hour", "2hour", "4hour"]
    start_time_values = ["2023-04-01", "2022-01-01", "2018-08-01", "2015-12-01", "2015-12-01", "2015-12-01", "2015-12-01"]
    timeframe_dict = dict(zip(timeframe_values, start_time_values))

    results = []

    for ticker in ticker_values:
        for timeframe in timeframe_dict:
            download_data(ticker, timeframe, timeframe_dict[timeframe])
            for reward in reward_values:
                for risk in risk_values:
                           
                    # Your program's main logic here
                    print(f"read_data(), Reward = {reward}, Risk = {risk}")
                    data = read_data(ticker, timeframe)
    
                    print(f"add_features(), Reward = {reward}, Risk = {risk}")
                    data_with_features = add_features(data, reward, risk)
    
                    print(f"clean_data(), Reward = {reward}, Risk = {risk}")
                    cleaned_data = clean_data(data_with_features)
    
                    print(f"train_model(), Reward = {reward}, Risk = {risk}")
                    model, X_train, X_test, y_train, y_test, X_test_index = train_model(cleaned_data)
                    
                    print(f"evaluate_model(), Reward = {reward}, Risk = {risk}")
                    predictions, prediction_probabilities = evaluate_model(model, X_train, X_test, y_train, y_test)
    
                    print(f"record_sim_trades(), Reward = {reward},  Risk = {risk}")
                    buy_signals_df = record_sim_trades(cleaned_data, predictions, prediction_probabilities, X_test_index)
    
                    print(f"record_sim_metrics(), Reward = {reward}, Risk = {risk}")
                    results = record_sim_metrics(buy_signals_df, ticker, timeframe, reward, risk, results)
    
                    print(results, len(results))
            
            results_df = pd.DataFrame(results)
            results_df.to_csv(f"{ticker}_{timeframe}_results_df.csv")



if __name__ == "__main__":
    main()
    