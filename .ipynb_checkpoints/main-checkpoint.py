# main.py

# import libraries
from modules import config
from modules import dependencies

# import functions and classes
from modules.data_processing import download_data, read_data
from modules.feature_engineering import add_features, clean_data
from modules.modeling import train_model
from modules.evaluation import evaluate_model
from modules.visualization import record_metrics

def main():
    
    # Define a range of values for risk and reward
    risk_values = [1.0, 1.5, 2.0]  # Example risk values
    reward_values = [1.0, 1.5, 2.0]  # Example reward values
    
    results = []
    
    for reward in reward_values:
        for risk in risk_values:
            # Your program's main logic here
            data = read_data()
            
            print(f"read_data(), Reward = {reward}, Risk = {risk}")
            data_with_features = add_features(data, reward, risk)
            print(f"add_features(), Reward = {reward}, Risk = {risk}")
            cleaned_data = clean_data(data_with_features)
            print(f"clean_data(), Reward = {reward}, Risk = {risk}")
            model, X_train, X_test, y_train, y_test, X_test_index = train_model(cleaned_data)
            print(f"train_model(), Reward = {reward}, Risk = {risk}")
            predictions, prediction_probabilities = evaluate_model(model, X_train, X_test, y_train, y_test)
            print(f"evaluate_model(), Reward = {reward}, Risk = {risk}")
            results = record_metrics(data_with_features, predictions, prediction_probabilities, X_test_index, reward, risk, results)
            print(results)



if __name__ == "__main__":
    main()