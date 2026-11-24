# Presentation Notes — SDG 11 Air Quality Analysis

DEV AAT · B.M.S. College of Engineering

| Slide | Talking points | Visual |
|---|---|---|
| 1. Title and objective | Study reported air quality in Indian cities in the context of SDG Target 11.6. | |
| 2. Source data | One row per city-day. 26 cities, 29,531 raw records, 1 January 2015 to 1 July 2020. Show date, city, AQI and category, and numeric pollutant concentrations. AQI is an index. | Raw-data preview from the notebook |
| 3. Cleaning and quality | Drop Xylene (61.3% missing), fill pollutant gaps within city and use a median where gaps remain, and exclude rows without AQI or category. 24,850 records remain. | [Missingness](../outputs/graphs/00_raw_missing_values.png) |
| 4. AQI distribution | Mean 166.5, median 118. Moderate is the largest category. Poor, Very Poor and Severe account for 26.0% of city-days. | [Distribution](../outputs/graphs/aqi_distribution.png) · [Categories](../outputs/graphs/aqi_category_distribution.png) |
| 5. City differences | Ahmedabad has the highest mean (452.1), and Aizawl the lowest (34.8). Ahmedabad still ranks first after excluding AQI above 500, with a mean of 291.7. | [Highest city means](../outputs/graphs/top_polluted_cities.png) · [Lowest city means](../outputs/graphs/least_polluted_cities.png) |
| 6. Changes over time | Pooled coverage rises from 7 to 26 cities. Only Delhi has at least 80% January–June coverage every year. Its comparable-period mean falls from 306.3 to 182.1. November has the highest pooled monthly AQI, and July has the lowest. | [Yearly trends](../outputs/graphs/yearly_aqi_trend.png) · [Monthly trends](../outputs/graphs/monthly_aqi_trend.png) |
| 7. Pollutant relationships | CO and PM2.5 show the strongest cleaned-data correlations with AQI. Measured PM10–AQI Pearson r is 0.803 on 17,764 pairs and 0.514 in the filled dataset. Measured and filled samples differ. | [Correlation heatmap](../outputs/graphs/pollutant_correlation_heatmap.png) · [PM scatter plot](../outputs/graphs/pm25_pm10_scatter.png) |
| 8. City category profiles | In 2019, Poor or worse accounted for 95.17% of Ahmedabad's reported days and 53.15% of Delhi's. Include only cities with at least 300 reported days. | [Category shares](../outputs/graphs/city_aqi_category_profile_2019.png) |
| 9. Interpretation and limits | Findings describe recorded city-days. City coverage, imputation, and extreme values affect interpretation. The official SDG indicator uses population-weighted annual particulate matter concentrations. | |
| 10. Sources and questions | Credit the dataset, UN framework, and the project workflow built with Python, pandas, Matplotlib, seaborn, and Jupyter. | |

## Questions to prepare for

- **Why use a comparable period?** Calendar coverage changes by year, and the 2020 file ends July 1. January through June gives each year the same months. The coverage threshold limits the comparison to Delhi.
- **Why check measured pairs separately?** Missing PM2.5 and PM10 may be filled from different days. The measured-pair check shows how the association changes when the analysis uses pairs available in the raw source.
- **Why keep values above 500?** Keeping them preserves the reported baseline. Excluding them in a separate analysis tests how much they change city means.
- **Can the analysis show which policy or activity changed air quality?** The plotted trends and correlations describe the data. A causal study would need a design and data that account for other influences.

[Dataset source](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india) · [UN Goal 11](https://sdgs.un.org/goals/goal11) · [Indicator metadata](https://unstats.un.org/sdgs/metadata/files/Metadata-11-06-02.pdf)
