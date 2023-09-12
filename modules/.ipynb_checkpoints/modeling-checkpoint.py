# modeling.py

# Import libraries
from modules.config import features
from pandas.tseries.offsets import DateOffset
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn import svm
from imblearn.under_sampling import RandomUnderSampler

def train_model(signals_df, offset_value):
    ### Setup Train and Test Sets for and Features

    # Make sure we have a sufficient training period
    training_begin = str(signals_df.index.min())
    training_end = str(signals_df.index.min() + DateOffset(months=offset_value))
        
    ### Split the data into training and testing sets.
    
    # Choose if you want features
    X = signals_df[features]
    
    # 1 means a buy would've produced a profit (hit target/win), -1 means a sale would've produced a profit (hit stop/loss)
    y = signals_df["Exit"]
    
    # Splitting into Train and Test sets
    X_train = X.loc[training_begin: training_end]
    y_train = y.loc[training_begin: training_end]
    
    # Generate the X_test and y_test DataFrames
    X_test = X.loc[training_end:]
    y_test = y.loc[training_end:]
    
    # Scale the data
    scaler = StandardScaler()
    X_scaler = scaler.fit(X_train)
    X_train_scaled = X_scaler.transform(X_train)
    X_test_scaled = X_scaler.transform(X_test)    
    
    # Undersample the data
    rus = RandomUnderSampler(random_state=1)
    undersampled_X_train_scaled, undersampled_y_train = rus.fit_resample(X_train_scaled, y_train)
    

    ### Support Vector Machine (SVC) Model
    
    # Create the classifier model
    model = svm.SVC(probability=True, random_state=1)
     
    # Fit the model to the data using undersampled_X_train_scaled and undersampled_y_train
    model = model.fit(undersampled_X_train_scaled, undersampled_y_train)
    
    return model, undersampled_X_train_scaled, X_test_scaled, undersampled_y_train, y_test, X_test.index
