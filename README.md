# SDG 11 — Air Quality in Indian Cities

Data Exploration and Visualization (23CS5PCDEV) · B.M.S. College of Engineering, Bangalore.

This project explores reported AQI and pollutant concentrations for 26 Indian cities from 1 January 2015 to 1 July 2020. It compares city means, annual and monthly patterns, AQI categories, and pollutant associations. The dataset contains 29,531 raw city-days and 24,850 city-days with reported AQI and category after cleaning. [Dataset source](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india)

The project discusses air quality in the context of SDG Target 11.6. The official indicator 11.6.2 measures population-weighted annual particulate matter concentrations. This analysis summarizes the city-days available in the source file. [UN Goal 11](https://sdgs.un.org/goals/goal11) · [Indicator metadata](https://unstats.un.org/sdgs/metadata/files/Metadata-11-06-02.pdf)

## Run the project

From this directory, use Python 3.12. The following PowerShell commands assume `python --version` reports Python 3.12.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_all.py
```

The runner executes these stages in order.

1. `src/dfmodif.py` reads the raw CSV, normalizes city and date fields, removes exact duplicates, fills pollutant gaps, and exports the cleaned data, annual city summaries, and the data quality report.
2. `src/analysis.py` reads the cleaned data, exports the summary tables, and compares the baseline against a matched calendar period, measured PM pairs, and an AQI subset capped at 500 by exclusion.
3. `notebooks/SDG11_Air_Quality_Analysis.ipynb` executes with the runner's Python interpreter, saves its outputs in the notebook, and regenerates 12 PNG charts.

To work interactively, launch Jupyter from the project directory.

```powershell
.\.venv\Scripts\python.exe -m jupyter notebook notebooks/SDG11_Air_Quality_Analysis.ipynb
```

Choose the Python kernel with the project dependencies and run all cells. The notebook can read and clean the source CSV directly using the same preprocessing functions. Use the runner to regenerate every CSV as well.

## File layout

| Location | Contents |
|---|---|
| `dataset/raw/city_day.csv` | Source data |
| `dataset/processed/` | Generated cleaned dataset and city-by-year summary |
| `src/` | Preprocessing and statistical analysis |
| `notebooks/` | Executed exploratory analysis notebook |
| `outputs/graphs/` | Raw missingness chart and eleven exploratory charts |
| `outputs/tables/` | City, year and month summaries, pollutant averages, PM2.5 bands, comparable-period AQI, city AQI sensitivity, and 2019 category shares |
| `outputs/statistics/` | Data quality counts, descriptive statistics, correlation matrix, PM correlation sensitivity, raw and cleaned numeric profiles, and selected measured-pair correlations |
| `report/` and `presentation/` | Word report, walkthrough, report notes and presentation talking points |
| `archive/` | Original preprocessing script and local logs from the earlier run |

## How to read the results

- The pooled annual series includes 7 cities in 2015 and 26 in partial-year 2020. `comparable_period_aqi.csv` compares January–June using cities with at least 80% of calendar days present every year. Only Delhi qualifies.
- Reported AQI values above 500 stay in the baseline. `city_aqi_sensitivity.csv` shows how excluding those records changes the city means and sample sizes.
- Forward fill, backward fill, and a column median fill pollutant gaps. `pm_correlation_sensitivity.csv` compares measured PM2.5–PM10 pairs with the imputed analysis dataset.
- AQI is an index. Pollutant concentration units differ by field. Station coverage, population exposure, and causes of changes cannot be inferred from this city-day analysis.

## Extended EDA

- The numeric profiles include quartiles, skewness, IQR flags and concentration CV. IQR flags are retained for review.
- The selected relationships table compares Pearson and Spearman on observed pairs with Pearson on the filled dataset. Pair counts are reported because measurement availability varies by pollutant.
- The 2019 category chart compares the distribution of reported AQI buckets within cities with at least 300 observed days in that year.

## Read the project

- [Executed EDA notebook](notebooks/SDG11_Air_Quality_Analysis.ipynb) contains the full 14-section analysis.
- [Final Word report](report/SDG%2011%20Air%20Quality%20Analysis%20Final%20Report.docx) and [project walkthrough](report/How%20We%20Built%20the%20SDG%2011%20Air%20Quality%20Project.docx) summarize the results and explain the workflow.
