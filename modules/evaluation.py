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