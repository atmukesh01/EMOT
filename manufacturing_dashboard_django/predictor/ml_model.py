# File: manufacturing_dashboard_django/predictor/ml_model.py

import joblib
import pandas as pd
import os

# Build the path to the model file
# This makes sure the path is correct, no matter where you run the server from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'final_model.pkl')

# Load the trained model
try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully from ml_model.py")
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_PATH}")
    model = None

def predict_quality(temperature, pressure, speed):
    """
    Takes process parameters and returns a predicted quality score.
    """
    if model is None:
        return None

    # Create a DataFrame from the input for the model
    input_data = pd.DataFrame({
        'temperature_c': [temperature],
        'pressure_psi': [pressure],
        'speed_rpm': [speed]
    })
    
    # Make a prediction
    prediction = model.predict(input_data)
    
    return prediction[0]