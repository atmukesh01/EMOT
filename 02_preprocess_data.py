# File: 02_preprocess_data.py

import pandas as pd
from sklearn.model_selection import train_test_split

def preprocess_data(input_path='manufacturing_data.csv'):
    """
    Loads data, separates features and target, splits into
    training and testing sets, and saves them to CSV files.
    """
    # Load the dataset
    df = pd.read_csv(input_path)
    print("Dataset loaded successfully.")

    # Separate features (X) and target (y)
    X = df[['temperature_c', 'pressure_psi', 'speed_rpm']]
    y = df['quality_score']

    # Split the data into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print("Data split into training and testing sets.")

    # Save the processed data
    X_train.to_csv('X_train.csv', index=False)
    X_test.to_csv('X_test.csv', index=False)
    y_train.to_csv('y_train.csv', index=False)
    y_test.to_csv('y_test.csv', index=False)
    print("Processed data files saved successfully.")

if __name__ == '__main__':
    preprocess_data()