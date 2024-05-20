# main.py

# import libraries
import pandas as pd

from stocks import stocks_config
from shared import dependencies
from shared.time_it import time_it

# import functions and classes
from stocks.data_processing import download_data, read_data
from stocks.feature_engineering import parallel_process_features, clean_data, add_features
from stocks.modeling import train_model
from shared.evaluation import evaluate_model
from stocks.simulate import record_sim_trades
from shared.metrics import record_sim_metrics

def main():

    results = []

    for ticker in stocks_config.ticker_values:
        for timeframe in stocks_config.timeframe_values:
            results = []
            print(f"Results = [{results}]")
      
            # print(f"download_data(ticker={ticker}, timeframe={timeframe[0]}, start={timeframe[1]})")
            # download_data(ticker, timeframe[0], timeframe[1])
            
            for reward in stocks_config.reward_values:
                for risk in stocks_config.risk_values:
                           
                    # Your program's main logic here
                    print(f"read_data(), Reward = {reward}, Risk = {risk}")
                    timed_read_data = time_it(read_data)
                    data = timed_read_data(ticker, timeframe[0])
    
                    # print(f"add_features(), Reward = {reward}, Risk = {risk}")
                    
                    timed_add_features = time_it(parallel_process_features)
                    for i in range(1, 13):
                        print(f"num_processes = ", i)
                        data_with_features = timed_add_features(data, reward, risk, i)
    
                    print(f"clean_data(), Reward = {reward}, Risk = {risk}")
                    timed_clean_data = time_it(clean_data)
                    cleaned_data = timed_clean_data(data_with_features)
    
                    print(f"train_model(), Reward = {reward}, Risk = {risk}")
                    timed_train_model = time_it(train_model)
                    model, X_train, X_test, y_train, y_test, X_test_index = timed_train_model(cleaned_data, timeframe[2])
                    
                    print(f"evaluate_model(), Reward = {reward}, Risk = {risk}")
                    timed_evaluate_model = time_it(evaluate_model)
                    predictions, prediction_probabilities = timed_evaluate_model(model, X_train, X_test, y_train, y_test)
    
                    print(f"record_sim_trades(), Reward = {reward},  Risk = {risk}")
                    timed_record_sim_trades = time_it(record_sim_trades)
                    buy_signals_df = timed_record_sim_trades(cleaned_data, predictions, prediction_probabilities, X_test_index)
    
                    print(f"record_sim_metrics(), Reward = {reward}, Risk = {risk}")
                    timed_record_sim_metrics = time_it(record_sim_metrics)
                    results = timed_record_sim_metrics(buy_signals_df, ticker, timeframe, reward, risk, results)
    
                    print(results, len(results))
            
            results_df = pd.DataFrame(results)
            results_df.to_csv(f"./data/{ticker}/{ticker}_{timeframe[0]}_results_df.csv", index=False)



if __name__ == "__main__":
    main()
    