# Final Report Notes — SDG 11 Air Quality Analysis
## DEV AAT — 23CS5PCDEV | B.M.S. College of Engineering

> These are verified results from the actual analysis.
> Use them to write your report in your own words.
> Do not copy this text directly — rephrase it in your own language.

---

## Verified Dataset Statistics

| Metric | Value |
|---|---|
| Raw records | 29,531 |
| Cleaned records | 24,850 |
| Original columns | 16 |
| Cleaned columns | 18 |
| Cities | 26 |
| Date range | 1 Jan 2015 – 1 Jul 2020 |
| Missing values after cleaning | 0 (all columns complete) |
| Duplicate rows | 0 |

---

## Actual Analysis Results (use these in your report)

### Most Polluted Cities (Mean AQI)
1. Ahmedabad — 452.1
2. Delhi — 259.5
3. Patna — 240.8
4. Gurugram — 225.1
5. Lucknow — 218.0

### Least Polluted Cities (Mean AQI)
1. Aizawl — 34.8
2. Shillong — 53.8
3. Coimbatore — 73.0
4. Thiruvananthapuram — 75.9
5. Ernakulam — 92.4

### Year-wise Mean AQI
| Year | Mean AQI | Note |
|---|---|---|
| 2015 | 212.5 | Highest year |
| 2016 | 197.2 | |
| 2017 | 181.5 | |
| 2018 | 182.7 | Slight increase |
| 2019 | 156.5 | |
| 2020 | 113.5 | Jan–Jul only; COVID lockdown effect |

### Monthly Mean AQI
| Month | Mean AQI |
|---|---|
| November | 241.7 (highest) |
| January | 231.7 |
| December | 227.1 |
| July | 111.9 (lowest) |
| August | 113.6 |

### AQI Category Distribution
| Category | Count | Percentage |
|---|---|---|
| Good | 1,341 | 5.4% |
| Satisfactory | 8,224 | 33.1% |
| Moderate | 8,829 | 35.5% |
| Poor | 2,781 | 11.2% |
| Very Poor | 2,337 | 9.4% |
| Severe | 1,338 | 5.4% |

### Strongest Pollutant Correlations with AQI
| Pollutant | Pearson r |
|---|---|
| CO | 0.678 |
| PM2.5 | 0.635 |
| NO2 | 0.533 |
| PM10 | 0.514 |
| SO2 | 0.486 |

### PM2.5 vs PM10
- Pearson correlation: **r = 0.594** (moderate-to-strong positive)
- PM2.5 mean: 68.9 µg/m³
- PM10 mean: 121.8 µg/m³

### Key Skewness Values
- AQI: 3.40 (strongly right-skewed — long tail of extreme values)
- PM2.5: 2.82 (strongly right-skewed)
- PM10: 1.96 (right-skewed)

---

## Data Quality Issues Found

| Issue | Count | Decision |
|---|---|---|
| Xylene missing | 18,109 (61.3%) | Column dropped |
| Rows with no AQI | 4,681 | Rows removed |
| Duplicate rows | 0 | None to remove |
| Negative pollutant values | 0 | None found |
| AQI > 500 (extreme) | 543 | Retained — real readings |
| PM10 < PM2.5 (suspicious) | 2,757 | Flagged — may be imputation artifact |

---

## Graphs Generated (use these in PPT/report)

All saved in `outputs/graphs/`:

1. `aqi_distribution.png` — Histogram of AQI distribution
2. `aqi_category_distribution.png` — Bar chart of AQI categories
3. `top_polluted_cities.png` — Top 10 most polluted cities
4. `least_polluted_cities.png` — 10 least polluted cities
5. `yearly_aqi_trend.png` — Year-wise AQI line chart
6. `monthly_aqi_trend.png` — Monthly AQI seasonal pattern
7. `pollutant_correlation_heatmap.png` — Correlation heatmap
8. `pm25_pm10_scatter.png` — Scatter plot PM2.5 vs PM10
9. `pollutant_boxplots.png` — Box plots for 7 pollutants
10. `city_pollutant_comparison.png` — Grouped bar: PM2.5, PM10, NO2 by city

---

## Suggested Report Structure

1. Title Page
2. Abstract (3–4 sentences: problem, dataset, method, key finding)
3. Introduction — SDG 11, air quality problem in India
4. Objectives and Research Questions
5. Dataset Description — source, size, columns, grain
6. Data Types in the Dataset
7. Tools and Libraries Used
8. Data Cleaning and Preprocessing — steps, before/after table
9. Statistical Analysis — descriptive stats table
10. EDA and Visualizations — each graph with interpretation
11. Key Findings — bullet list of numbered answers
12. Limitations — 5–6 points
13. Conclusion — connect findings to SDG 11
14. References — CPCB, Kaggle, WHO guidelines

---

## Suggested PPT Slide Outline

1. Title slide
2. Outline
3. SDG 11 and Problem Statement
4. Dataset Overview
5. Data Types in the Dataset
6. Summary Statistics (table)
7. Tools/Libraries
8. Data Quality Issues (before cleaning)
9. Cleaning Pipeline (before/after table)
10. Visualization: AQI Distribution
11. Visualization: AQI Category Distribution
12. Visualization: Most/Least Polluted Cities
13. Visualization: Year-wise Trend
14. Visualization: Seasonal Pattern
15. Visualization: Correlation Heatmap
16. Visualization: PM2.5 vs PM10
17. Key Findings (bullet list)
18. Limitations
19. Conclusion
20. References
