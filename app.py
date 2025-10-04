from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

try:
    model = joblib.load('final_model.pkl')
    print("Model loaded successfully.")
except FileNotFoundError:
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    if model is None: return jsonify({'error': 'Model not loaded'}), 500
    data = request.get_json()
    try:
        input_df = pd.DataFrame({
            'temperature_c': [float(data['temperature'])],
            'pressure_psi': [float(data['pressure'])],
            'speed_rpm': [float(data['speed'])]
        })
        prediction = model.predict(input_df)
        return jsonify({'predicted_quality': prediction[0]})
    except Exception as e:
        return jsonify({'error': f'Invalid input data: {e}'}), 400

@app.route('/find-parameters', methods=['POST'])
def find_parameters():
    if model is None: return jsonify({'error': 'Model not loaded'}), 500

    data = request.get_json()
    try:
        target_quality = float(data['target_quality'])
        # Get locked parameters, if they exist
        locked_params = data.get('locked_params', {})
    except (KeyError, TypeError, ValueError):
        return jsonify({'error': 'Invalid input data'}), 400

    num_samples = 10000
    candidates = {}

    # --- UPDATED SEARCH LOGIC ---
    # For each parameter, use the locked value or generate random values
    if 'temperature' in locked_params:
        candidates['temperature_c'] = np.full(num_samples, float(locked_params['temperature']))
    else:
        candidates['temperature_c'] = np.random.uniform(130, 170, num_samples)

    if 'pressure' in locked_params:
        candidates['pressure_psi'] = np.full(num_samples, float(locked_params['pressure']))
    else:
        candidates['pressure_psi'] = np.random.uniform(40, 60, num_samples)

    if 'speed' in locked_params:
        candidates['speed_rpm'] = np.full(num_samples, float(locked_params['speed']))
    else:
        candidates['speed_rpm'] = np.random.uniform(900, 1100, num_samples)
    
    candidates_df = pd.DataFrame(candidates)
    predictions = model.predict(candidates_df)
    
    candidates_df['abs_diff'] = np.abs(predictions - target_quality)
    best_candidate = candidates_df.loc[candidates_df['abs_diff'].idxmin()]

    result = {
        'best_parameters': {
            'temperature': round(best_candidate['temperature_c'], 2),
            'pressure': round(best_candidate['pressure_psi'], 2),
            'speed': round(best_candidate['speed_rpm'], 2),
        },
        'achieved_quality': round(predictions[best_candidate.name], 2)
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)