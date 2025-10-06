# File: 04_evaluate_model.py

import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np

def evaluate_model(model_path='final_model_enhanced.pkl', 
                   X_test_path='X_test_enhanced.csv', 
                   y_test_path='y_test_enhanced.csv'):
    """
    Loads a trained enhanced model and test data, and prints evaluation metrics.
    """
    model = joblib.load(model_path)
    X_test = pd.read_csv(X_test_path)
    y_test = pd.read_csv(y_test_path).squeeze()
    print("Enhanced model and test data loaded.")

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("\n--- Final Enhanced Model Performance ---")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"R-squared (R²): {r2:.2f}")

if __name__ == '__main__':
    evaluate_model()