# File: 01_generate_data.py

import pandas as pd
import numpy as np

def generate_data(num_records=1000, file_path='manufacturing_data.csv'):
    """
    Generates a synthetic dataset for a manufacturing process
    and saves it to a CSV file.
    """
    # Set a seed for reproducibility
    np.random.seed(42)

    # Generate Feature Data
    temp = np.random.normal(loc=150, scale=10, size=num_records)
    pressure = np.random.normal(loc=50, scale=5, size=num_records)
    speed = np.random.normal(loc=1000, scale=50, size=num_records)

    # Generate the Target Variable (Product Quality)
    quality_score = 100 - (0.1 * np.abs(temp - 152)**2) - (0.05 * np.abs(pressure - 51)**2) - (0.001 * np.abs(speed - 1000)**2)
    quality_score += np.random.normal(loc=0, scale=2, size=num_records)
    quality_score = np.clip(quality_score, 50, 100)

    # Create a DataFrame
    df = pd.DataFrame({
        'temperature_c': temp,
        'pressure_psi': pressure,
        'speed_rpm': speed,
        'quality_score': quality_score
    })

    # Save to CSV
    df.to_csv(file_path, index=False)
    print(f"Successfully created synthetic dataset at: {file_path}")

if __name__ == '__main__':
    generate_data()