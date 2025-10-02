# File: 04_evaluate_model.py

import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

def evaluate_model(model_path='final_model.pkl', X_test_path='X_test.csv', y_test_path='y_test.csv'):
    """
    Loads a trained model and test data, makes predictions,
    and prints evaluation metrics.
    """
    # Load the model and test data
    model = joblib.load(model_path)
    X_test = pd.read_csv(X_test_path)
    y_test = pd.read_csv(y_test_path).squeeze()
    print("Model and test data loaded.")

    # Make predictions
    predictions = model.predict(X_test)

    # Calculate and print performance metrics
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    print("\n--- Final Model Performance on Test Data ---")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"R-squared (R²): {r2:.2f}")

if __name__ == '__main__':
    evaluate_model()