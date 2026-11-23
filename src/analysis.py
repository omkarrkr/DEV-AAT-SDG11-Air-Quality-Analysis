"""Summarize cleaned city-days and check sensitivity to coverage and data quality."""

import pandas as pd

if __package__:
    from .dfmodif import CLEAN_PATH, PROJECT_ROOT, RAW_PATH, prepare_city_days
else:
    from dfmodif import CLEAN_PATH, PROJECT_ROOT, RAW_PATH, prepare_city_days

TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
STATS_DIR = PROJECT_ROOT / "outputs" / "statistics"
KEY_COLUMNS = ["PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "CO", "SO2", "O3", "AQI"]
MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def aqi_summary(data, group):
    summary = data.groupby(group)["AQI"].agg(
        Mean="mean", Median="median", StdDev="std", Records="count"
    )
    return summary.round(1)


def comparable_period(data):
    """Compare January to June across cities with 80% coverage in every year."""
    years = sorted(data["Year"].unique())
    first_half = data.loc[data["Date"].dt.month.le(6)]
    city_year = first_half.groupby(["City", "Year"])["AQI"].agg(Mean="mean", Records="count")
    counts = city_year["Records"].unstack().reindex(columns=years, fill_value=0).fillna(0)
    days = pd.Series({
        year: (pd.Timestamp(year=year, month=7, day=1) - pd.Timestamp(year=year, month=1, day=1)).days
        for year in years
    })
    cities = counts.index[counts.div(days).ge(0.8).all(axis=1)]
    panel = city_year.loc[city_year.index.get_level_values("City").isin(cities)]
    summary = panel.groupby("Year").agg(Mean_AQI=("Mean", "mean"), Records=("Records", "sum"))
    summary = summary.reindex(years).round(1)
    summary["Records"] = summary["Records"].fillna(0).astype(int)
    summary["Cities"] = len(cities)
    return summary, cities.tolist()


def sensitivity_checks(prepared, cleaned):
    measured = prepared.dropna(subset=["AQI", "AQI_Bucket"])
    measured_pairs = measured.dropna(subset=["PM2.5", "PM10"])
    pm_correlation = pd.DataFrame(
        {
            "Records": [len(measured_pairs), len(cleaned)],
            "Pearson_r": [
                measured_pairs["PM2.5"].corr(measured_pairs["PM10"]),
                cleaned["PM2.5"].corr(cleaned["PM10"]),
            ],
        },
        index=pd.Index(["Measured pairs", "After imputation"], name="Input"),
    ).round(3)

    all_aqi = cleaned.groupby("City")["AQI"].agg(Mean_AQI="mean", Records="count")
    within_500 = cleaned.loc[cleaned["AQI"].le(500)].groupby("City")["AQI"].agg(
        Mean_AQI_Up_To_500="mean", Records_Up_To_500="count"
    )
    city_aqi = all_aqi.join(within_500).sort_values("Mean_AQI", ascending=False)
    city_aqi["Records_Up_To_500"] = city_aqi["Records_Up_To_500"].fillna(0).astype(int)
    return pm_correlation, city_aqi.round(1)


def main():
    data = pd.read_csv(CLEAN_PATH, parse_dates=["Date"])
    prepared = prepare_city_days(pd.read_csv(RAW_PATH))
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    STATS_DIR.mkdir(parents=True, exist_ok=True)

    city = aqi_summary(data, "City")
    extremes = data.groupby("City")["AQI"].agg(Min="min", Max="max")
    city = city.join(extremes)[["Mean", "Median", "StdDev", "Min", "Max", "Records"]]
    city.sort_values("Mean", ascending=False).to_csv(TABLE_DIR / "city_aqi_statistics.csv")

    year = aqi_summary(data, "Year")
    year["Cities"] = data.groupby("Year")["City"].nunique()
    year.to_csv(TABLE_DIR / "year_aqi_statistics.csv")
    aqi_summary(data, "Month").reindex(MONTH_ORDER).to_csv(TABLE_DIR / "monthly_aqi_statistics.csv")

    panel, cities = comparable_period(data)
    panel.to_csv(TABLE_DIR / "comparable_period_aqi.csv")
    pm_correlation, city_sensitivity = sensitivity_checks(prepared, data)
    pm_correlation.to_csv(STATS_DIR / "pm_correlation_sensitivity.csv")
    city_sensitivity.to_csv(TABLE_DIR / "city_aqi_sensitivity.csv")

    city_pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "AQI"]
    pollutant_means = data.groupby("City")[city_pollutants].mean().round(2)
    pollutant_means.sort_values("AQI", ascending=False).to_csv(TABLE_DIR / "city_pollutant_averages.csv")
    data["PM2.5_Severity"].value_counts().to_csv(TABLE_DIR / "pm25_severity_distribution.csv")
    data[KEY_COLUMNS].describe().round(2).to_csv(STATS_DIR / "descriptive_statistics.csv")
    data[KEY_COLUMNS].corr().round(3).to_csv(STATS_DIR / "correlation_matrix.csv")
    print(f"Analysis complete. Comparable-period cities: {', '.join(cities) or 'none'}.")


if __name__ == "__main__":
    main()
