# Report Notes — SDG 11 Air Quality Analysis

DEV AAT · 23CS5PCDEV · B.M.S. College of Engineering

## Dataset and method

The source has 29,531 records and 16 columns. After cleaning, the analysis has 24,850 city-days and 18 columns across 26 cities, covering 1 January 2015 to 1 July 2020. The cleaned dataset has zero missing cells and zero duplicate city-date keys. One row represents one city and date. Station counts and locations are unavailable in this file.

Xylene was dropped because 18,109 values (61.3%) were missing. Pollutant gaps were filled within city using forward fill and backward fill, then the column median for remaining gaps. The analysis excludes 4,681 rows with missing AQI or category. The existing AQI category is retained separately from the derived PM2.5 concentration bands.

## Results to use in the report

| Question | Result | Evidence |
|---|---|---|
| Highest and lowest city means | Ahmedabad 452.1, Delhi 259.5, Patna 240.8. At the low end, Aizawl 34.8, Shillong 53.8, Coimbatore 73.0. City means summarize available days. | [City AQI](../outputs/tables/city_aqi_statistics.csv) |
| Pooled annual pattern | Mean AQI was 212.5 in 2015, 156.5 in 2019 and 113.5 in partial-year 2020. The number of cities with data grew from 7 to 26. | [Yearly AQI](../outputs/tables/year_aqi_statistics.csv) |
| Comparable annual pattern | At least 80% of January–June days had AQI in every study year for Delhi alone. Delhi's January–June mean went from 306.3 in 2015 to 245.9 in 2019 and 182.1 in 2020. | [Comparable-period AQI](../outputs/tables/comparable_period_aqi.csv) |
| Monthly pattern | November had the highest pooled mean (241.7), and July had the lowest (111.9). Coverage varies by month. | [Monthly AQI](../outputs/tables/monthly_aqi_statistics.csv) |
| AQI distribution | Mean 166.5 and median 118. Moderate was the largest source category (35.5%). Poor, Very Poor and Severe accounted for 26.0% combined. | [Distribution](../outputs/graphs/aqi_distribution.png) · [Categories](../outputs/graphs/aqi_category_distribution.png) |
| Pollutant associations | CO (0.678) and PM2.5 (0.635) had the strongest Pearson correlations with AQI in the cleaned data. These are associations. | [Correlation matrix](../outputs/statistics/correlation_matrix.csv) |

## Data quality and sensitivity

- Of 17,146 measured PM2.5–PM10 pairs on days eligible for AQI analysis, 229 had PM10 below PM2.5. In the cleaned data, 2,757 of 24,850 rows had that pattern. Pearson correlation was 0.853 on measured pairs and 0.594 in the cleaned dataset. Both the analyzed sample and the treatment of missing readings differ between these summaries. [Quality checks](../outputs/statistics/data_quality_report.csv) · [Correlation sensitivity](../outputs/statistics/pm_correlation_sensitivity.csv)
- The source contains 543 AQI records above 500. Ahmedabad remains first when those records are excluded, and its mean drops from 452.1 to 291.7. The above-500 values warrant source-level validation. [City AQI sensitivity](../outputs/tables/city_aqi_sensitivity.csv)
- City means pool the observations available for each city. Annual and monthly averages reflect changing coverage. Weather, policies, lockdown effects, and population exposure are outside what this design can estimate.

## Report sequence

1. Title page and abstract
2. SDG 11 context, objectives, and research questions
3. Source data, unit of observation, and data types
4. Preprocessing and the before-and-after quality checks
5. Descriptive statistics, AQI distributions, city comparisons, trends, and pollutant relationships
6. Sensitivity results and limitations
7. Conclusion and references

Use the notebook's eleven exported charts selectively. Cite the [dataset listing](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india) and [UN Goal 11](https://sdgs.un.org/goals/goal11). The official [indicator 11.6.2 methodology](https://unstats.un.org/sdgs/metadata/files/Metadata-11-06-02.pdf) provides the context for discussing population-weighted exposure.
