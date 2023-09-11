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
    
    results = []
    
    for reward in reward_values:
        for risk in risk_values:
            # Your program's main logic here
            print(f"read_data(), Reward = {reward}, Risk = {risk}")
            data = read_data()

            print(f"add_features(), Reward = {reward}, Risk = {risk}")
            data_with_features = add_features(data, reward, risk)

            print(f"clean_data(), Reward = {reward}, Risk = {risk}")
            cleaned_data = clean_data(data_with_features)

            print(f"train_model(), Reward = {reward}, Risk = {risk}")
            model, X_train, X_test, y_train, y_test, X_test_index = train_model(cleaned_data)
            
            print(f"evaluate_model(), Reward = {reward}, Risk = {risk}")
            predictions, prediction_probabilities = evaluate_model(model, X_train, X_test, y_train, y_test)

            # print(f"record_trades_and_metrics(), Reward = {reward}, Risk = {risk}")
            # results = record_trades_and_metrics(data_with_features, predictions, prediction_probabilities, X_test_index, reward, risk, results)

            print(f"record_sim_trades(), Reward = {reward},  Risk = {risk}")
            buy_signals_df = record_sim_trades(cleaned_data, predictions, prediction_probabilities, X_test_index)

            print(f"record_sim_metrics(), Reward = {reward}, Risk = {risk}")
            results = record_sim_metrics(buy_signals_df, reward, risk, results)

            print(results, len(results))

    
    results_df = pd.DataFrame(results)
    results_df.to_csv("results_df_spy.csv")



if __name__ == "__main__":
    main()
    