# Presentation Notes — SDG 11 Air Quality Analysis
## DEV AAT | B.M.S. College of Engineering

> These are talking points for your college presentation.
> Do not read them verbatim — use them to prepare your own explanation.

---

## Slide 1: Dataset Chosen

**What to say:**
"We chose the Indian Cities Air Quality dataset from CPCB (Central Pollution Control Board). It contains daily air quality readings from 26 cities across India, from January 2015 to July 2020. The raw file has 29,531 rows and 16 columns. Each row represents one city on one day."

**Key column to mention:**
AQI, PM2.5, PM10, NO2, CO, SO2, O3 (all in µg/m³, CO in mg/m³)

---

## Slide 2: Different Types of Data in the Dataset

**Types present:**
- **Numerical (continuous):** PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, AQI — all float64
- **Numerical (discrete/derived):** Year (int), Month number (int)
- **Categorical (nominal):** City (26 categories), AQI_Bucket (6 categories)
- **Categorical (ordinal):** PM2.5_Severity (Good < Satisfactory < Moderately Polluted < Poor < Very Poor < Severe)
- **Temporal:** Date (datetime64)

---

## Slide 3: Domain/Context

**What to say:**
"This project is linked to SDG 11, specifically Target 11.6, which is about reducing the environmental impact of cities — including air pollution. India faces a serious air quality crisis. Many of its cities rank among the most polluted in the world, and air pollution causes millions of premature deaths annually. The CPCB collects air quality data from monitoring stations and calculates the AQI daily."

---

## Slide 4: Initial Summary Statistics

**Key numbers to mention:**
- Mean AQI: 166.5 (falls in Moderate category)
- Median AQI: 118 (lower than mean — confirms right-skew)
- Max AQI: 2,049 (Ahmedabad — extreme event)
- Min AQI: 13
- PM2.5 mean: 68.9 µg/m³ (WHO safe limit is 15 µg/m³ annually)
- 24,850 valid records after cleaning

---

## Slide 5: Tools and Libraries

| Tool/Library | Purpose |
|---|---|
| Python 3.12 | Programming language |
| pandas | Data loading, cleaning, manipulation |
| numpy | Numerical operations |
| matplotlib | Base chart library |
| seaborn | Statistical visualizations |
| Jupyter Notebook | Interactive analysis environment |

---

## Slide 6: Major Quality Issues in Raw Data

**Be specific — these are real numbers:**

| Issue | Details |
|---|---|
| Xylene: 61.3% missing | 18,109 out of 29,531 rows — column was dropped |
| AQI missing: 15.9% | 4,681 rows had no target — these rows were removed |
| NH3: 35.0% missing | Filled using forward fill per city |
| PM10: 37.7% missing | Filled using forward fill per city |
| No duplicate rows | 0 exact duplicates found |
| No negative readings | All pollutant values are non-negative |

**When asked why forward fill:**
"Air quality follows continuous trends. If a sensor was working on Monday and Friday but not Tuesday–Thursday, it's reasonable to assume the values in between are similar to the nearest known reading. This is better than deleting those rows or using a global average that ignores the city-specific trend."

---

## Likely Evaluation Questions & Answers

**Q: Why did you remove Xylene?**  
A: 61.3% of its values were missing. If we imputed that much data, we'd essentially be making up 18,000+ readings. The imputed values would not reflect real measurements at all — so removing the column was the correct decision.

**Q: What is the difference between PM2.5 and PM10?**  
A: PM stands for particulate matter. PM10 is particles less than 10 micrometres in diameter. PM2.5 is a subset of PM10 — the finer particles less than 2.5 micrometres. PM2.5 is more dangerous because fine particles penetrate deeper into the lungs and bloodstream.

**Q: Why is Ahmedabad so polluted in this dataset?**  
A: Ahmedabad has a large industrial sector, significant vehicle traffic, and the monitoring station in this dataset picked up high readings. The average AQI of 452 is partly driven by extreme events (some readings above 1,000) that skew the mean very high.

**Q: What does the correlation heatmap tell you?**  
A: PM2.5 and CO have the strongest correlations with AQI (r = 0.635 and 0.678). This means these two pollutants are most strongly associated with the overall AQI score. It does not mean they cause the AQI to be high — it means they tend to increase together.

**Q: Why is 2020 AQI lower?**  
A: Two reasons. First, the data only covers January–July 2020 — it misses the high-pollution winter months (October–December). Second, the COVID-19 lockdown from March to May 2020 significantly reduced vehicle traffic and industrial activity, which lowered emissions.

**Q: What is forward fill?**  
A: Forward fill (ffill) copies the last known non-null value forward to fill subsequent missing values. For example, if Monday has a PM2.5 reading of 50 and Tuesday–Wednesday have no reading, forward fill sets Tuesday and Wednesday to 50. We did this within each city's time series so we don't mix readings from different cities.
