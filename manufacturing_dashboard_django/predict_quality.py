import pandas as pd
import joblib

def predict_new_data(input_data):
    """
    Loads the trained model and makes a prediction on new input data.

    Args:
        input_data (dict): A dictionary with keys 'temperature_c',
                           'pressure_psi', and 'speed_rpm'.

    Returns:
        float: The predicted quality score.
    """
    try:
        model = joblib.load('final_model.pkl')
    except FileNotFoundError:
        print("Error: Model file 'final_model.pkl' not found.")
        print("Please run the '03_train_model.py' script first.")
        return None

    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)
    return prediction[0]

if __name__ == '__main__':
    try:
        # --- Get User Inputs ---
        print("--- Enter New Process Parameters ---")
        temp = float(input("Enter Temperature (°C): "))
        pressure = float(input("Enter Pressure (psi): "))
        speed = float(input("Enter Speed (rpm): "))

        # --- Assemble Input for Prediction ---
        new_parameters = {
            'temperature_c': temp,
            'pressure_psi': pressure,
            'speed_rpm': speed
        }

        # Get the predicted quality score
        predicted_score = predict_new_data(new_parameters)

        # Print the result
        if predicted_score is not None:
            print("\n--- Prediction Result ---")
            print(f"Predicted Quality Score: {predicted_score:.2f}")

    except ValueError:
        print("\nInvalid input. Please enter valid numbers for all parameters.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")