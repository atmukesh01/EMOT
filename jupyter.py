import pandas as pd
import numpy as np

# Set a seed for reproducibility
np.random.seed(42)

# Define the number of data points (batches)
num_records = 1000

# --- Generate Feature Data ---
# Temperature (normally around 150°C, with some variance)
temp = np.random.normal(loc=150, scale=10, size=num_records)

# Pressure (normally around 50 psi, with some variance)
pressure = np.random.normal(loc=50, scale=5, size=num_records)

# Rotational Speed (normally around 1000 RPM)
speed = np.random.normal(loc=1000, scale=50, size=num_records)

# --- Generate the Target Variable (Product Quality) ---
# Let's assume ideal quality is a score of 100
# Quality is mainly affected by being close to ideal temp (152°C) and pressure (51 psi)
# We add some noise to make it realistic

quality_score = 100 - (0.1 * np.abs(temp - 152)**2) - (0.05 * np.abs(pressure - 51)**2) - (0.001 * np.abs(speed - 1000)**2)
# Add random noise
quality_score += np.random.normal(loc=0, scale=2, size=num_records)

# Ensure quality score does not go below a certain threshold (e.g., 50)
quality_score = np.clip(quality_score, 50, 100)


# --- Create a DataFrame ---
df = pd.DataFrame({
    'temperature_c': temp,
    'pressure_psi': pressure,
    'speed_rpm': speed,
    'quality_score': quality_score
})

# --- Save to CSV ---
file_path = 'D:\PROJECTS- 2026\EMOT\EMOT/manufacturing_data.csv'
df.to_csv(file_path, index=False)

print(f"Successfully created synthetic dataset at: {file_path}")
print("First 5 rows of the dataset:")
print(df.head())