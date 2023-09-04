# main.py

# import libraries
from modules import config
from modules import dependencies

# import functions and classes
from modules.data_processing import download_data, read_data
from modules.feature_engineering import add_features, clean_data
from modules.modeling import train_model
from modules.evaluation import evaluate_model
from modules.visualization import plot_results

def main():
    # Your program's main logic here
    data = read_data()
    data_with_features = add_features(data)
    cleaned_data = clean_data(data_with_features)
    model, X_train, X_test, y_train, y_test, X_test_index = train_model(cleaned_data)
    predictions, prediction_probabilities = evaluate_model(model, X_train, X_test, y_train, y_test)
    plot_results(data_with_features, predictions, prediction_probabilities, X_test_index)

if __name__ == "__main__":
    main()