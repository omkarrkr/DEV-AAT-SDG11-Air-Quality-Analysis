"""
dfmodif.py — Data Cleaning & Preprocessing Script
===================================================
Project : SDG 11 — Analysis of Air Quality in Indian Cities
Subject : Data Exploration and Visualization (23CS5PCDEV)
College : B.M.S. College of Engineering, Bangalore

Run from project root:
    python src/dfmodif.py

Outputs:
    dataset/processed/city_day_cleaned.csv
    dataset/processed/city_annual_summary.csv
    outputs/statistics/data_quality_report.csv
"""

import pandas as pd
import numpy as np
import os
import sys

# ─────────────────────────────────────────────────────────────
# PATH SETUP  (script works whether run from root or src/)
# ─────────────────────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

RAW_PATH     = os.path.join(PROJECT_ROOT, "dataset", "raw",       "city_day.csv")
CLEAN_PATH   = os.path.join(PROJECT_ROOT, "dataset", "processed", "city_day_cleaned.csv")
SUMMARY_PATH = os.path.join(PROJECT_ROOT, "dataset", "processed", "city_annual_summary.csv")
QUALITY_PATH = os.path.join(PROJECT_ROOT, "outputs", "statistics", "data_quality_report.csv")

os.makedirs(os.path.dirname(CLEAN_PATH),   exist_ok=True)
os.makedirs(os.path.dirname(QUALITY_PATH), exist_ok=True)

# ─────────────────────────────────────────────────────────────
# STEP 1 — LOAD RAW DATASET
# ─────────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 1: Loading raw dataset")
print("=" * 60)

df = pd.read_csv(RAW_PATH)

print(f"Raw shape          : {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"Columns            : {df.columns.tolist()}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nMissing values per column (raw):")

raw_missing = df.isnull().sum()
raw_missing_pct = (raw_missing / len(df) * 100).round(1)
for col in df.columns:
    print(f"  {col:15s}: {raw_missing[col]:5d}  ({raw_missing_pct[col]}%)")

# ─────────────────────────────────────────────────────────────
# STEP 2 — FORMAT REVISION & STRING CLEANING
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2: Format revision and string cleaning")
print("=" * 60)

# Convert Date string → datetime
df['Date'] = pd.to_datetime(df['Date'])

# FIX: Strip leading/trailing whitespace from city names
# Without this, 'Delhi' and ' Delhi' would be treated as two different cities.
df['City'] = df['City'].str.strip()

# Sort chronologically within each city — required before time-series imputation
df = df.sort_values(by=['City', 'Date']).reset_index(drop=True)

print(f"Date column converted to datetime64.")
print(f"City names stripped of whitespace.")
print(f"Dataset sorted by City → Date.")

# ─────────────────────────────────────────────────────────────
# STEP 3 — DEDUPLICATION
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3: Deduplication")
print("=" * 60)

before = len(df)
df = df.drop_duplicates()
after  = len(df)
print(f"Duplicate rows removed : {before - after}")
print(f"Rows remaining         : {after:,}")

# Also check for duplicate City+Date combinations (a logical duplicate even if other fields differ)
city_date_dups = df.duplicated(subset=['City', 'Date']).sum()
print(f"Duplicate City+Date combinations: {city_date_dups}")

# ─────────────────────────────────────────────────────────────
# STEP 4 — DROP UNUSABLE COLUMN (XYLENE)
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4: Dropping Xylene column")
print("=" * 60)

xylene_missing_pct = df['Xylene'].isnull().mean() * 100
print(f"Xylene missing : {df['Xylene'].isnull().sum():,} / {len(df):,} rows ({xylene_missing_pct:.1f}%)")
print("Decision: Drop Xylene. 61.3% missing means imputation would manufacture data, not fill gaps.")

if 'Xylene' in df.columns:
    df = df.drop(columns=['Xylene'])

print(f"Columns after removal: {df.columns.tolist()}")

# ─────────────────────────────────────────────────────────────
# STEP 5 — MISSING VALUE IMPUTATION FOR POLLUTANTS
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 5: Pollutant imputation (forward fill → backward fill → median)")
print("=" * 60)

# LIMITATION NOTE:
# Forward fill carries the last known value forward across consecutive missing days.
# Backward fill covers gaps at the start of a city's monitoring period.
# If a sensor is offline for many days in a row, all those days get the same imputed value.
# These imputed values should not be treated as actual sensor readings — they are estimates.

pollutant_cols = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3',
                  'CO', 'SO2', 'O3', 'Benzene', 'Toluene']

before_impute = df[pollutant_cols].isnull().sum()

for col in pollutant_cols:
    # Forward fill within each city's time series
    df[col] = df.groupby('City')[col].transform(lambda x: x.ffill())
    # Backward fill for any remaining gaps (e.g. station started late)
    df[col] = df.groupby('City')[col].transform(lambda x: x.bfill())
    # Global median as last resort (cities with no readings at all for that column)
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].median())

after_impute = df[pollutant_cols].isnull().sum()

print(f"{'Column':<12} {'Before':>8} {'After':>8}")
print("-" * 32)
for col in pollutant_cols:
    print(f"{col:<12} {before_impute[col]:>8} {after_impute[col]:>8}")

# ─────────────────────────────────────────────────────────────
# STEP 6 — DROP ROWS WITH MISSING AQI / AQI_BUCKET
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 6: Removing rows with missing AQI or AQI_Bucket")
print("=" * 60)

before_drop = len(df)
df_cleaned = df.dropna(subset=['AQI', 'AQI_Bucket']).reset_index(drop=True)
removed = before_drop - len(df_cleaned)

print(f"Rows removed (missing AQI) : {removed:,}")
print(f"Rows retained              : {len(df_cleaned):,}")

# ─────────────────────────────────────────────────────────────
# STEP 7 — FEATURE ENGINEERING
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 7: Feature engineering")
print("=" * 60)

df_cleaned = df_cleaned.copy()

# Temporal features
df_cleaned['Year']  = df_cleaned['Date'].dt.year
df_cleaned['Month'] = df_cleaned['Date'].dt.month_name()

# PM2.5 Severity binning
# Using include_lowest=True so PM2.5 = 0.0 is captured in the first bin.
# Without this, any reading of exactly 0 would become NaN.
pm25_bins   = [0, 30, 60, 90, 120, 250, 1000]
pm25_labels = ['Good', 'Satisfactory', 'Moderately Polluted', 'Poor', 'Very Poor', 'Severe']

df_cleaned['PM2.5_Severity'] = pd.cut(
    df_cleaned['PM2.5'],
    bins=pm25_bins,
    labels=pm25_labels,
    include_lowest=True   # Ensures PM2.5 = 0 falls into 'Good' bin
)

print(f"Year and Month columns derived from Date.")
print(f"PM2.5_Severity bins: {pm25_bins}")
print(f"PM2.5_Severity distribution:")
print(df_cleaned['PM2.5_Severity'].value_counts().sort_index().to_string())

# ─────────────────────────────────────────────────────────────
# STEP 8 — DATA QUALITY CHECKS
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 8: Data quality checks on cleaned dataset")
print("=" * 60)

# Check for negative pollutant values (physically impossible)
quality_issues = []
for col in pollutant_cols:
    neg_count = (df_cleaned[col] < 0).sum()
    if neg_count > 0:
        print(f"  WARNING: {col} has {neg_count} negative values.")
        quality_issues.append({'Issue': f'Negative {col}', 'Count': neg_count, 'Action': 'Flagged — not removed'})
    else:
        quality_issues.append({'Issue': f'Negative {col}', 'Count': 0, 'Action': 'None'})

# AQI > 500 (above the standard scale — real but extreme)
aqi_extreme = (df_cleaned['AQI'] > 500).sum()
print(f"  AQI > 500       : {aqi_extreme} records (extreme but valid — not removed)")
quality_issues.append({'Issue': 'AQI > 500', 'Count': int(aqi_extreme), 'Action': 'Retained — extreme but real readings'})

# PM10 < PM2.5 (suspicious — PM10 should always be >= PM2.5)
mask = df_cleaned['PM10'].notna() & df_cleaned['PM2.5'].notna()
pm_suspect = (df_cleaned.loc[mask, 'PM10'] < df_cleaned.loc[mask, 'PM2.5']).sum()
print(f"  PM10 < PM2.5    : {pm_suspect} records (possibly imputed — flagged)")
quality_issues.append({'Issue': 'PM10 < PM2.5', 'Count': int(pm_suspect), 'Action': 'Flagged — may result from imputation'})

# Skewness
print("\n  Skewness of key columns:")
for col in ['PM2.5', 'PM10', 'AQI']:
    sk = df_cleaned[col].skew()
    print(f"    {col:<8}: {sk:.2f}  ({'right-skewed' if sk > 1 else 'left-skewed' if sk < -1 else 'approx normal'})")

# Save quality report
quality_df = pd.DataFrame(quality_issues)
quality_df.to_csv(QUALITY_PATH, index=False)
print(f"\n  Quality report saved → {QUALITY_PATH}")

# ─────────────────────────────────────────────────────────────
# STEP 9 — AGGREGATION
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 9: City-wise annual aggregation")
print("=" * 60)

city_annual_summary = (
    df_cleaned
    .groupby(['City', 'Year'])[['PM2.5', 'PM10', 'AQI']]
    .mean()
    .round(2)
    .reset_index()
)
print(city_annual_summary.head(10).to_string())

# ─────────────────────────────────────────────────────────────
# STEP 10 — EXPORT
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 10: Exporting cleaned datasets")
print("=" * 60)

df_cleaned.to_csv(CLEAN_PATH, index=False)
city_annual_summary.to_csv(SUMMARY_PATH, index=False)
print(f"Cleaned dataset   → {CLEAN_PATH}")
print(f"Annual summary    → {SUMMARY_PATH}")

# ─────────────────────────────────────────────────────────────
# POST-CLEANING VERIFICATION
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("POST-CLEANING VERIFICATION")
print("=" * 60)

print(f"Final shape          : {df_cleaned.shape[0]:,} rows × {df_cleaned.shape[1]} columns")
print(f"Duplicate rows       : {df_cleaned.duplicated().sum()}")
print(f"Unique cities        : {df_cleaned['City'].nunique()}")
print(f"Date range           : {df_cleaned['Date'].min().date()} to {df_cleaned['Date'].max().date()}")
print(f"Year range           : {df_cleaned['Year'].min()} to {df_cleaned['Year'].max()}")
print(f"\nMissing values after cleaning:")
mv_after = df_cleaned.isnull().sum()
any_missing = False
for col in df_cleaned.columns:
    if mv_after[col] > 0:
        print(f"  {col}: {mv_after[col]}")
        any_missing = True
if not any_missing:
    print("  NONE — all columns complete.")

print(f"\nAQI category distribution:")
print(df_cleaned['AQI_Bucket'].value_counts().to_string())

print(f"\nColumn data types:")
print(df_cleaned.dtypes.to_string())

print("\n✓ Preprocessing complete.")
