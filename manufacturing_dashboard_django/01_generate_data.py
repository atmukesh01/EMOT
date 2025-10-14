import pandas as pd
import numpy as np

def generate_data(num_records=1000, file_path='manufacturing_data_enhanced.csv'):
    np.random.seed(42)
    temp = np.random.normal(loc=150, scale=10, size=num_records)
    pressure = np.random.normal(loc=50, scale=5, size=num_records)
    speed = np.random.normal(loc=1000, scale=50, size=num_records)
    viscosity = np.random.normal(loc=15, scale=2, size=num_records)
    maintenance = np.random.uniform(low=0, high=500, size=num_records)
    cycle_time = np.random.normal(loc=30, scale=3, size=num_records)

    quality_score = 100 
    quality_score -= (0.1 * np.abs(temp - 152)**2)
    quality_score -= (0.05 * np.abs(pressure - 51)**2)
    quality_score -= (0.001 * np.abs(speed - 1000)**2)
    quality_score -= (0.2 * np.abs(viscosity - 15)**2)
    quality_score -= (0.01 * maintenance)
    quality_score -= (0.1 * np.abs(cycle_time - 30)**2)
    
    quality_score += np.random.normal(loc=0, scale=2, size=num_records)
    quality_score = np.clip(quality_score, 40, 100)

    df = pd.DataFrame({
        'temperature_c': temp, 'pressure_psi': pressure, 'speed_rpm': speed,
        'viscosity_pas': viscosity, 'hours_since_maintenance': maintenance,
        'cycle_time_s': cycle_time, 'quality_score': quality_score
    })

    df.to_csv(file_path, index=False)
    print(f"Successfully created dataset: {file_path}")

if __name__ == '__main__':
    generate_data()