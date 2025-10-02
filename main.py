import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('manufacturing_data.csv')

# Display the first few rows
print("First 5 rows:")
print(df.head())

# Get a statistical summary (mean, std, etc.)
print("\nStatistical Summary:")
print(df.describe())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())