# File: app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Load the trained model
try:
    model = joblib.load('final_model.pkl')
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Error: Model file 'final_model.pkl' not found. Please train the model first.")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    """Receives input data, makes a prediction, and returns it."""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    # Get data from the POST request
    data = request.get_json()
    
    try:
        # Create a DataFrame from the input
        input_data = {
            'temperature_c': [float(data['temperature'])],
            'pressure_psi': [float(data['pressure'])],
            'speed_rpm': [float(data['speed'])]
        }
        input_df = pd.DataFrame(input_data)
        
        # Make a prediction
        prediction = model.predict(input_df)
        
        # Return the prediction as JSON
        return jsonify({'predicted_quality': prediction[0]})
        
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({'error': f'Invalid input data: {e}'}), 400

if __name__ == '__main__':
    # Run the app on port 5000
    app.run(debug=True, port=5000)