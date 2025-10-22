import joblib
import pandas as pd
import numpy as np
import os
from PIL import Image
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUALITY_MODEL_PATH = os.path.join(BASE_DIR, 'final_model_enhanced.pkl')
GATEKEEPER_MODEL_PATH = os.path.join(BASE_DIR, 'plastic_gatekeeper_model.keras') 
IDENTIFIER_MODEL_PATH = os.path.join(BASE_DIR, 'plastic_image_classifier.keras') 
CLASS_NAMES_PATH = os.path.join(BASE_DIR, 'plastic_class_names.txt')

try:
    quality_model = joblib.load(QUALITY_MODEL_PATH)
    print("✅ Quality prediction model loaded.")
except Exception as e:
    quality_model = None; print(f"❌ Error loading quality model: {e}")

try:
    gatekeeper_model = tf.keras.models.load_model(GATEKEEPER_MODEL_PATH)
    print("✅ Gatekeeper model loaded.")
except Exception as e:
    gatekeeper_model = None; print(f"❌ Error loading gatekeeper model: {e}")

try:
    identifier_model = tf.keras.models.load_model(IDENTIFIER_MODEL_PATH)
    with open(CLASS_NAMES_PATH, 'r') as f:
        identifier_class_names = f.read().strip().split(',')
    print(" Plastic identifier model loaded.")
except Exception as e:
    identifier_model = None; identifier_class_names = []; print(f" Error loading identifier model: {e}")


def run_full_image_pipeline(image_file):
    
    if not gatekeeper_model or not identifier_model:
        return "Model(s) not loaded", 0.0, None

    try:
        img = Image.open(image_file).convert('RGB').resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)

        gatekeeper_pred = gatekeeper_model.predict(img_array)[0][0]
        
      
        if gatekeeper_pred < 0.7: 
            return "Not a plastic item", gatekeeper_pred, "not_plastic"

      
        identifier_preds = identifier_model.predict(img_array)[0]
        confidence = np.max(identifier_preds)
        predicted_class_index = np.argmax(identifier_preds)
        plastic_type = identifier_class_names[predicted_class_index]

        return plastic_type, confidence, "plastic"
        
    except Exception as e:
        print(f"Error during full image pipeline: {e}")
        return "Error", 0.0, None


def get_quality_prediction(params):
    if quality_model is None: return None
    try:
        input_df = pd.DataFrame([params])
        training_column_order = ['temperature_c', 'pressure_psi', 'speed_rpm', 'viscosity_pas', 'hours_since_maintenance', 'cycle_time_s']
        input_df_ordered = input_df[training_column_order]
        prediction = quality_model.predict(input_df_ordered)
        return prediction[0]
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

def find_best_parameters(target_quality, locked_params={}):
    if quality_model is None: return None
    num_samples = 10000; candidates = {}; param_configs = { 'temperature': ('temperature_c', 130, 170), 'pressure': ('pressure_psi', 40, 60), 'speed': ('speed_rpm', 900, 1100), 'viscosity': ('viscosity_pas', 12, 18), 'maintenance': ('hours_since_maintenance', 0, 500), 'cycle_time': ('cycle_time_s', 25, 35) }
    for param, (col, low, high) in param_configs.items():
        if param in locked_params and locked_params.get(param):
            candidates[col] = np.full(num_samples, float(locked_params[param]))
        else:
            candidates[col] = np.random.uniform(low, high, num_samples)
    candidates_df = pd.DataFrame(candidates)
    training_column_order = ['temperature_c', 'pressure_psi', 'speed_rpm', 'viscosity_pas', 'hours_since_maintenance', 'cycle_time_s']
    candidates_df_ordered = candidates_df[training_column_order]
    predictions = quality_model.predict(candidates_df_ordered)
    candidates_df['abs_diff'] = np.abs(predictions - target_quality); best_candidate = candidates_df.loc[candidates_df['abs_diff'].idxmin()]
    return { 'best_parameters': {p: round(best_candidate[c], 2) for p, (c, _, _) in param_configs.items()}, 'achieved_quality': round(predictions[best_candidate.name], 2) }