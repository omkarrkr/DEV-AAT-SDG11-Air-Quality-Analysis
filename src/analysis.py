"""
analysis.py — Standalone Statistical Analysis Script
=====================================================
Project : SDG 11 — Analysis of Air Quality in Indian Cities
Subject : Data Exploration and Visualization (23CS5PCDEV)

Run from project root:
    python src/analysis.py

Reads the cleaned dataset and prints a full statistical summary.
Saves all summary tables to outputs/tables/ and outputs/statistics/.
"""

import pandas as pd
import numpy as np
import os

# ─── Path setup ───────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DATA_PATH  = os.path.join(PROJECT_ROOT, 'dataset', 'processed', 'city_day_cleaned.csv')
TABLE_DIR  = os.path.join(PROJECT_ROOT, 'outputs', 'tables')
STATS_DIR  = os.path.join(PROJECT_ROOT, 'outputs', 'statistics')

os.makedirs(TABLE_DIR, exist_ok=True)
os.makedirs(STATS_DIR, exist_ok=True)

# ─── Load ─────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH, parse_dates=['Date'])
print(f"Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns\n")

# ─── 1. Full descriptive statistics ───────────────────────────
print("=" * 60)
print("1. DESCRIPTIVE STATISTICS")
print("=" * 60)
key_cols = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'AQI']
desc = df[key_cols].describe().round(2)
print(desc.to_string())
desc.to_csv(os.path.join(STATS_DIR, 'descriptive_statistics.csv'))

# ─── 2. City-wise AQI summary ─────────────────────────────────
print("\n" + "=" * 60)
print("2. CITY-WISE AQI STATISTICS")
print("=" * 60)
city_stats = df.groupby('City')['AQI'].agg(['mean','median','std','min','max','count']).round(1)
city_stats.columns = ['Mean','Median','StdDev','Min','Max','Records']
city_stats = city_stats.sort_values('Mean', ascending=False)
print(city_stats.to_string())
city_stats.to_csv(os.path.join(TABLE_DIR, 'city_aqi_statistics.csv'))

# ─── 3. Year-wise AQI summary ─────────────────────────────────
print("\n" + "=" * 60)
print("3. YEAR-WISE AQI STATISTICS")
print("=" * 60)
year_stats = df.groupby('Year')['AQI'].agg(['mean','median','std','count']).round(1)
year_stats.columns = ['Mean','Median','StdDev','Records']
print(year_stats.to_string())
year_stats.to_csv(os.path.join(TABLE_DIR, 'year_aqi_statistics.csv'))

# ─── 4. Monthly AQI summary ───────────────────────────────────
print("\n" + "=" * 60)
print("4. MONTHLY AQI STATISTICS")
print("=" * 60)
month_order = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']
month_stats = df.groupby('Month')['AQI'].agg(['mean','median','std']).round(1)
month_stats = month_stats.reindex(month_order)
month_stats.columns = ['Mean','Median','StdDev']
print(month_stats.to_string())
month_stats.to_csv(os.path.join(TABLE_DIR, 'monthly_aqi_statistics.csv'))

# ─── 5. Correlation matrix ────────────────────────────────────
print("\n" + "=" * 60)
print("5. CORRELATION MATRIX")
print("=" * 60)
corr_cols = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'AQI']
corr = df[corr_cols].corr().round(3)
print(corr.to_string())
corr.to_csv(os.path.join(STATS_DIR, 'correlation_matrix.csv'))

# ─── 6. PM2.5 severity distribution ──────────────────────────
print("\n" + "=" * 60)
print("6. PM2.5 SEVERITY DISTRIBUTION")
print("=" * 60)
sev_counts = df['PM2.5_Severity'].value_counts()
for cat, cnt in sev_counts.items():
    print(f"  {cat:<22s}: {cnt:5,}  ({cnt/len(df)*100:.1f}%)")
sev_counts.to_csv(os.path.join(TABLE_DIR, 'pm25_severity_distribution.csv'))

# ─── 7. City-wise pollutant averages ──────────────────────────
print("\n" + "=" * 60)
print("7. CITY-WISE POLLUTANT AVERAGES")
print("=" * 60)
city_poll = df.groupby('City')[['PM2.5','PM10','NO2','SO2','CO','O3','AQI']].mean().round(2)
city_poll = city_poll.sort_values('AQI', ascending=False)
print(city_poll.to_string())
city_poll.to_csv(os.path.join(TABLE_DIR, 'city_pollutant_averages.csv'))

print("\n✓ Analysis complete. All tables saved.")
