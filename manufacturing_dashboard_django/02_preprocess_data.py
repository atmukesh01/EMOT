# File: 02_preprocess_data.py

import pandas as pd
from sklearn.model_selection import train_test_split

def preprocess_data(input_path='manufacturing_data_enhanced.csv'):
    """
    Loads enhanced data, separates features and target, splits into
    training and testing sets, and saves them.
    """
    df = pd.read_csv(input_path)
    print("Enhanced dataset loaded successfully.")

    # Update the feature list to include new columns
    features = [
        'temperature_c', 'pressure_psi', 'speed_rpm', 
        'viscosity_pas', 'hours_since_maintenance', 'cycle_time_s'
    ]
    X = df[features]
    y = df['quality_score']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print("Data split into training and testing sets.")

    # Save the processed data
    X_train.to_csv('X_train_enhanced.csv', index=False)
    X_test.to_csv('X_test_enhanced.csv', index=False)
    y_train.to_csv('y_train_enhanced.csv', index=False)
    y_test.to_csv('y_test_enhanced.csv', index=False)
    print("Processed enhanced data files saved successfully.")

if __name__ == '__main__':
    preprocess_data()