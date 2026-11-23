import pandas as pd
import numpy as np


df = pd.read_csv('city_day.csv')



print("Dataset Shape:", df.shape)
print("\nData Summary:")
print(df.info())
print("\nMissing Values Count:")
print(df.isnull().sum())

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Sort chronologically by City and Date
df = df.sort_values(by=['City', 'Date']).reset_index(drop=True)

# Check for exact duplicate rows
duplicate_count = df.duplicated().sum()
print(f"Total duplicate rows: {duplicate_count}")

# Drop duplicates if present
df = df.drop_duplicates()

# Drop columns with excessive missing data (>50%)
df_cleaned = df.drop(columns=['Xylene'])

# Time-series forward fill grouped by city for pollutant readings
pollutant_cols = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene']

for col in pollutant_cols:
    # Forward fill then backward fill within each city group
    df_cleaned[col] = df_cleaned.groupby('City')[col].transform(lambda group: group.ffill().bfill())
    # Fill any remaining NaNs with overall column median
    df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())

# Drop rows where critical target columns (AQI / AQI_Bucket) are missing
df_cleaned = df_cleaned.dropna(subset=['AQI', 'AQI_Bucket']).reset_index(drop=True)

# Bin PM2.5 into standard health impact severity categories
pm25_bins = [0, 30, 60, 90, 120, 250, 1000]
pm25_labels = ['Good', 'Satisfactory', 'Moderately Polluted', 'Poor', 'Very Poor', 'Severe']

df_cleaned['PM2.5_Severity'] = pd.cut(df_cleaned['PM2.5'], bins=pm25_bins, labels=pm25_labels)

# Inspect distribution across bins

print(df_cleaned['PM2.5_Severity'].value_counts())




# Data Derivation: Extract temporal features
df_cleaned['Year'] = df_cleaned['Date'].dt.year
df_cleaned['Month'] = df_cleaned['Date'].dt.month_name()

# Data Aggregation: City-wise annual average AQI and PM2.5 levels
city_annual_summary = df_cleaned.groupby(['City', 'Year'])[['PM2.5', 'PM10', 'AQI']].mean().reset_index()

print("\nCity Annual AQI Aggregation Summary:")
print(city_annual_summary.head())


df_cleaned.to_csv('city_day_cleaned.csv', index = False)
