# File: app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# --- Load the NEW enhanced model ---
try:
    model = joblib.load('final_model_enhanced.pkl')
    print("Enhanced model loaded successfully.")
except FileNotFoundError:
    print("Error: 'final_model_enhanced.pkl' not found. Please train the new model first.")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    if model is None: return jsonify({'error': 'Model not loaded'}), 500
    
    data = request.get_json()
    try:
        # --- Updated to include all 6 features ---
        input_df = pd.DataFrame({
            'temperature_c': [float(data['temperature'])],
            'pressure_psi': [float(data['pressure'])],
            'speed_rpm': [float(data['speed'])],
            'viscosity_pas': [float(data['viscosity'])],
            'hours_since_maintenance': [float(data['maintenance'])],
            'cycle_time_s': [float(data['cycle_time'])]
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
        locked_params = data.get('locked_params', {})
    except Exception as e:
        return jsonify({'error': f'Invalid input data: {e}'}), 400

    num_samples = 10000
    candidates = {}

    # --- Updated search logic for all 6 features ---
    # Temperature
    if 'temperature' in locked_params:
        candidates['temperature_c'] = np.full(num_samples, float(locked_params['temperature']))
    else:
        candidates['temperature_c'] = np.random.uniform(130, 170, num_samples)
    # Pressure
    if 'pressure' in locked_params:
        candidates['pressure_psi'] = np.full(num_samples, float(locked_params['pressure']))
    else:
        candidates['pressure_psi'] = np.random.uniform(40, 60, num_samples)
    # Speed
    if 'speed' in locked_params:
        candidates['speed_rpm'] = np.full(num_samples, float(locked_params['speed']))
    else:
        candidates['speed_rpm'] = np.random.uniform(900, 1100, num_samples)
    # Viscosity
    if 'viscosity' in locked_params:
        candidates['viscosity_pas'] = np.full(num_samples, float(locked_params['viscosity']))
    else:
        candidates['viscosity_pas'] = np.random.uniform(12, 18, num_samples)
    # Maintenance
    if 'maintenance' in locked_params:
        candidates['hours_since_maintenance'] = np.full(num_samples, float(locked_params['maintenance']))
    else:
        candidates['hours_since_maintenance'] = np.random.uniform(0, 500, num_samples)
    # Cycle Time
    if 'cycle_time' in locked_params:
        candidates['cycle_time_s'] = np.full(num_samples, float(locked_params['cycle_time']))
    else:
        candidates['cycle_time_s'] = np.random.uniform(25, 35, num_samples)

    candidates_df = pd.DataFrame(candidates)
    predictions = model.predict(candidates_df)
    
    candidates_df['abs_diff'] = np.abs(predictions - target_quality)
    best_candidate = candidates_df.loc[candidates_df['abs_diff'].idxmin()]

    result = {
        'best_parameters': {
            'temperature': round(best_candidate['temperature_c'], 2),
            'pressure': round(best_candidate['pressure_psi'], 2),
            'speed': round(best_candidate['speed_rpm'], 2),
            'viscosity': round(best_candidate['viscosity_pas'], 2),
            'maintenance': round(best_candidate['hours_since_maintenance'], 2),
            'cycle_time': round(best_candidate['cycle_time_s'], 2),
        },
        'achieved_quality': round(predictions[best_candidate.name], 2)
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)