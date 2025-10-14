import pandas as pd
from sklearn.model_selection import train_test_split

def preprocess_data(input_path='manufacturing_data_enhanced.csv'):
    df = pd.read_csv(input_path)
    
    # --- THIS IS THE CRITICAL PART ---
    # We must explicitly select ALL SIX features for training.
    features = [
        'temperature_c', 
        'pressure_psi', 
        'speed_rpm', 
        'viscosity_pas', 
        'hours_since_maintenance', 
        'cycle_time_s'
    ]
    # --- END OF CRITICAL PART ---
    
    X = df[features]
    y = df['quality_score']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    X_train.to_csv('X_train_enhanced.csv', index=False)
    X_test.to_csv('X_test_enhanced.csv', index=False)
    y_train.to_csv('y_train_enhanced.csv', index=False)
    y_test.to_csv('y_test_enhanced.csv', index=False)
    print("✅ Processed data files saved with all 6 features.")

if __name__ == '__main__':
    preprocess_data()