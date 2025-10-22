# File: train_plastic_identifier.py

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from scipy.signal import savgol_filter
import joblib
import os

def generate_plastic_spectrum(plastic_type, num_points=200):
    wavelengths = np.linspace(900, 1700, num_points)
    base_spectrum = np.zeros(num_points)
    
    if plastic_type == 'PET':
        base_spectrum += 0.8 * np.exp(-((wavelengths - 1100)**2) / 500) + 0.6 * np.exp(-((wavelengths - 1450)**2) / 800)
    elif plastic_type == 'HDPE':
        base_spectrum += 0.9 * np.exp(-((wavelengths - 1215)**2) / 600) + 0.5 * np.exp(-((wavelengths - 1550)**2) / 700)
    elif plastic_type == 'PVC':
        base_spectrum += 0.7 * np.exp(-((wavelengths - 1050)**2) / 400) + 0.8 * np.exp(-((wavelengths - 1600)**2) / 900)
    elif plastic_type == 'LDPE':
        base_spectrum += 0.85 * np.exp(-((wavelengths - 1210)**2) / 550) + 0.6 * np.exp(-((wavelengths - 1580)**2) / 750)
    elif plastic_type == 'PP':
        base_spectrum += 0.95 * np.exp(-((wavelengths - 1150)**2) / 450) + 0.5 * np.exp(-((wavelengths - 1400)**2) / 600)
    elif plastic_type == 'PS':
        base_spectrum += 0.6 * np.exp(-((wavelengths - 1120)**2) / 300) + 0.9 * np.exp(-((wavelengths - 1680)**2) / 500)
    elif plastic_type == 'PC':
        base_spectrum += 0.5 * np.exp(-((wavelengths - 950)**2) / 400) + 0.9 * np.exp(-((wavelengths - 1300)**2) / 700)
    elif plastic_type == 'ABS':
        base_spectrum += 0.8 * np.exp(-((wavelengths - 1000)**2) / 500) + 0.7 * np.exp(-((wavelengths - 1500)**2) / 800)
        
    noise = np.random.normal(0, 0.03, num_points)
    return base_spectrum + noise

def create_dataset(num_samples_per_type=200):
    plastic_types = ['PET', 'HDPE', 'PVC', 'LDPE', 'PP', 'PS', 'PC', 'ABS']
    data, labels = [], []
    for plastic in plastic_types:
        for _ in range(num_samples_per_type):
            data.append(generate_plastic_spectrum(plastic))
            labels.append(plastic)
    return np.array(data), np.array(labels)

def preprocess_spectra(spectra_data):
    smoothed_spectra = savgol_filter(spectra_data, window_length=11, polyorder=2, axis=1)
    mean_centered = smoothed_spectra - np.mean(smoothed_spectra, axis=1, keepdims=True)
    normalized_spectra = mean_centered / np.std(mean_centered, axis=1, keepdims=True)
    return normalized_spectra

if __name__ == "__main__":
    X, y = create_dataset()
    X_processed = preprocess_spectra(X)
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.25, random_state=42, stratify=y)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    print("\n--- Evaluating Model ---")
    predictions = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {accuracy:.2%}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, predictions))
    
    output_path = os.path.join('predictor', 'plastic_identifier_model.pkl')
    joblib.dump(model, output_path)
    print(f"\nPlastic identification model saved to: {output_path}")