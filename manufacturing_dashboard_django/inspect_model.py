# File: inspect_model.py
import joblib

# Load the model you want to inspect
# Make sure to provide the correct path from where you run the script
model_path = 'predictor/plastic_identifier_model.pkl' 

try:
    model = joblib.load(model_path)
    print(f"Successfully loaded model from: {model_path}\n")

    # Print the type of model
    print(f"Model Type: {type(model)}\n")

    # For RandomForest models, we can see some of its settings (hyperparameters)
    if hasattr(model, 'n_estimators'):
        print("--- Model Settings ---")
        print(f"Number of trees (n_estimators): {model.n_estimators}")
        print(f"Max depth of trees (max_depth): {model.max_depth}")
        print(f"Number of features considered: {model.n_features_in_}")

except FileNotFoundError:
    print(f"Error: Model file not found at '{model_path}'. Make sure the path is correct.")
except Exception as e:
    print(f"An error occurred: {e}")