# evaluation.py

# imports
from sklearn import svm
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

def evaluate_model(model, undersampled_X_train_scaled, X_test_scaled, undersampled_y_train, y_test):
    # Use the trained model to predict the trading signals for the training data
    training_signal_predictions = model.predict(undersampled_X_train_scaled)
    training_probability_estimates = model.predict_proba(undersampled_X_train_scaled)
    
    # Evaluate the model using a classification report
    training_report = classification_report(undersampled_y_train, training_signal_predictions)
    print(f"Training Report \n {training_report}")
    
    # Use the trained model to predict the trading signals for the testing data.
    testing_signal_predictions = model.predict(X_test_scaled)
    testing_probability_estimates = model.predict_proba(X_test_scaled)
    
    # Evaluate the model's ability to predict the trading signal for the testing data
    testing_report = classification_report(y_test, testing_signal_predictions)
    print(f"Testing Report \n {testing_report}")
    
    return testing_signal_predictions, testing_probability_estimates


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
    
    
    
