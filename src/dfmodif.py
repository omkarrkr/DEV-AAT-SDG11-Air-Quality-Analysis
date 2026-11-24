"""Clean the daily city dataset and export the reusable analysis inputs."""

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "dataset" / "raw" / "city_day.csv"
PROCESSED_DIR = PROJECT_ROOT / "dataset" / "processed"
CLEAN_PATH = PROCESSED_DIR / "city_day_cleaned.csv"
SUMMARY_PATH = PROCESSED_DIR / "city_annual_summary.csv"
QUALITY_PATH = PROJECT_ROOT / "outputs" / "statistics" / "data_quality_report.csv"
AQI_CATEGORIES = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
POLLUTANTS = [
    "PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "CO", "SO2", "O3",
    "Benzene", "Toluene",
]


def prepare_city_days(raw):
    """Normalize keys and remove exact duplicates before filling readings."""
    data = raw.assign(
        Date=pd.to_datetime(raw["Date"]),
        City=raw["City"].str.strip(),
    ).sort_values(["City", "Date"])
    if data["City"].fillna("").eq("").any() or data["Date"].isna().any():
        raise ValueError("Every source row must have a city and date.")
    unknown_labels = set(data["AQI_Bucket"].dropna()) - set(AQI_CATEGORIES)
    if unknown_labels:
        raise ValueError(f"Unexpected reported AQI categories: {sorted(unknown_labels)}")
    data = data.drop_duplicates().drop(columns="Xylene")
    if data.duplicated(["City", "Date"]).any():
        raise ValueError("Conflicting rows share the same City and Date.")
    return data


def clean_city_days(prepared):
    """Fill pollutant gaps before selecting the rows with reported AQI."""
    data = prepared.copy()
    filled = data.groupby("City")[POLLUTANTS].ffill()
    filled = filled.groupby(data["City"]).bfill()
    data[POLLUTANTS] = filled.fillna(filled.median())

    cleaned = data.dropna(subset=["AQI", "AQI_Bucket"]).reset_index(drop=True)
    cleaned["Year"] = cleaned["Date"].dt.year
    cleaned["Month"] = cleaned["Date"].dt.month_name()
    cleaned["PM2.5_Severity"] = pd.cut(
        cleaned["PM2.5"],
        bins=[0, 30, 60, 90, 120, 250, float("inf")],
        labels=["Good", "Satisfactory", "Moderately Polluted", "Poor", "Very Poor", "Severe"],
        include_lowest=True,
    )
    return cleaned


def quality_report(prepared, cleaned):
    """Count questionable values while retaining them in the baseline."""
    measured = prepared.dropna(subset=["AQI", "AQI_Bucket", "PM2.5", "PM10"])
    issues = [
        (f"Negative {column}", int(cleaned[column].lt(0).sum()), "Checked")
        for column in POLLUTANTS
    ]
    issues.extend([
        ("AQI > 500", int(cleaned["AQI"].gt(500).sum()), "Retained for sensitivity analysis"),
        ("PM10 < PM2.5 (measured pairs)", int(measured["PM10"].lt(measured["PM2.5"]).sum()),
         "Checked before imputation on the same AQI-eligible population"),
        ("PM10 < PM2.5", int(cleaned["PM10"].lt(cleaned["PM2.5"]).sum()),
         "Retained; compare against measured pairs"),
    ])
    return pd.DataFrame(issues, columns=["Issue", "Count", "Action"])


def main():
    raw = pd.read_csv(RAW_PATH)
    prepared = prepare_city_days(raw)
    cleaned = clean_city_days(prepared)
    quality = quality_report(prepared, cleaned)
    annual = (
        cleaned.groupby(["City", "Year"])[["PM2.5", "PM10", "AQI"]]
        .mean()
        .round(2)
        .reset_index()
    )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    QUALITY_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(CLEAN_PATH, index=False)
    annual.to_csv(SUMMARY_PATH, index=False)
    quality.to_csv(QUALITY_PATH, index=False)
    print(f"Preprocessing complete: {len(raw):,} raw rows, {len(cleaned):,} cleaned rows.")


if __name__ == "__main__":
    main()
