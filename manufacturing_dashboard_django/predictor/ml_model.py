import joblib
import pandas as pd
import numpy as np
import os
from scipy.signal import savgol_filter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUALITY_MODEL_PATH = os.path.join(BASE_DIR, 'final_model_enhanced.pkl')
IDENTIFIER_MODEL_PATH = os.path.join(BASE_DIR, 'plastic_identifier_model.pkl')

try:
    quality_model = joblib.load(QUALITY_MODEL_PATH)
    print("✅ Quality prediction model loaded successfully.")
except FileNotFoundError:
    quality_model = None
    print(f"❌ Error: Quality model not found at {QUALITY_MODEL_PATH}")

try:
    identifier_model = joblib.load(IDENTIFIER_MODEL_PATH)
    print("✅ Plastic identifier model loaded successfully.")
except FileNotFoundError:
    identifier_model = None
    print(f"❌ Error: Identifier model not found at {IDENTIFIER_MODEL_PATH}")

def get_quality_prediction(params):
    if quality_model is None:
        return None
    try:
        input_df = pd.DataFrame([params])
        training_column_order = [
            'temperature_c', 'pressure_psi', 'speed_rpm',
            'viscosity_pas', 'hours_since_maintenance', 'cycle_time_s'
        ]
        input_df_ordered = input_df[training_column_order]
        prediction = quality_model.predict(input_df_ordered)
        return prediction[0]
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

def find_best_parameters(target_quality, locked_params={}):
    if quality_model is None: return None
    num_samples = 10000
    candidates = {}
    param_configs = {
        'temperature': ('temperature_c', 130, 170),
        'pressure': ('pressure_psi', 40, 60),
        'speed': ('speed_rpm', 900, 1100),
        'viscosity': ('viscosity_pas', 12, 18),
        'maintenance': ('hours_since_maintenance', 0, 500),
        'cycle_time': ('cycle_time_s', 25, 35)
    }

    for param, (col, low, high) in param_configs.items():
        if param in locked_params and locked_params.get(param):
            candidates[col] = np.full(num_samples, float(locked_params[param]))
        else:
            candidates[col] = np.random.uniform(low, high, num_samples)

    candidates_df = pd.DataFrame(candidates)
    
    training_column_order = [
        'temperature_c', 'pressure_psi', 'speed_rpm',
        'viscosity_pas', 'hours_since_maintenance', 'cycle_time_s'
    ]
    candidates_df_ordered = candidates_df[training_column_order]
    
    predictions = quality_model.predict(candidates_df_ordered)
    
    candidates_df['abs_diff'] = np.abs(predictions - target_quality)
    best_candidate = candidates_df.loc[candidates_df['abs_diff'].idxmin()]

    result = {
        'best_parameters': {p: round(best_candidate[c], 2) for p, (c, _, _) in param_configs.items()},
        'achieved_quality': round(predictions[best_candidate.name], 2)
    }
    return result

def generate_mock_spectrum():
    num_points = 200; wavelengths = np.linspace(900, 1700, num_points); base_spectrum = np.zeros(num_points)
    for _ in range(3):
        center = 900 + np.random.rand() * 800; intensity = np.random.rand() * 0.8 + 0.2; width = np.random.rand() * 500 + 400
        base_spectrum += intensity * np.exp(-((wavelengths - center)**2) / width)
    noise = np.random.normal(0, 0.03, num_points)
    return base_spectrum + noise

def _preprocess_spectra(spectra_data):
    spectra_data = np.array(spectra_data).reshape(1, -1)
    smoothed = savgol_filter(spectra_data, window_length=11, polyorder=2, axis=1)
    mean_centered = smoothed - np.mean(smoothed, axis=1, keepdims=True)
    std_dev = np.std(mean_centered, axis=1, keepdims=True)
    normalized = np.divide(mean_centered, std_dev, out=np.zeros_like(mean_centered), where=std_dev!=0)
    return normalized

def identify_plastic(spectrum_data):
    if identifier_model is None: return "Error: Model not loaded"
    processed_data = _preprocess_spectra(spectrum_data)
    prediction = identifier_model.predict(processed_data)
    return prediction[0]