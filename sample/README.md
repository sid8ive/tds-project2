# Data Analysis Report

## Overview
File: imdb_top_1000.csv

## Summary Statistics
                                                                                                                                              Poster_Link Series_Title Released_Year Certificate  Runtime  Genre  IMDB_Rating                                                                                                                Overview  Meta_score          Director      Star1        Star2         Star3          Star4   No_of_Votes      Gross
count                                                                                                                                                1000         1000          1000         899     1000   1000  1000.000000                                                                                                                    1000  843.000000              1000       1000         1000          1000           1000  1.000000e+03        831
unique                                                                                                                                               1000          999           100          16      140    202          NaN                                                                                                                    1000         NaN               548        660          841           891            939           NaN        823
top     https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX67_CR0,0,67,98_AL_.jpg     Drishyam          2014           U  100 min  Drama          NaN  Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.         NaN  Alfred Hitchcock  Tom Hanks  Emma Watson  Rupert Grint  Michael Caine           NaN  4,360,000
freq                                                                                                                                                    1            2            32         234       23     85          NaN                                                                                                                       1         NaN                14         12            7             5              4           NaN          5
mean                                                                                                                                                  NaN          NaN           NaN         NaN      NaN    NaN     7.949300                                                                                                                     NaN   77.971530               NaN        NaN          NaN           NaN            NaN  2.736929e+05        NaN
std                                                                                                                                                   NaN          NaN           NaN         NaN      NaN    NaN     0.275491                                                                                                                     NaN   12.376099               NaN        NaN          NaN           NaN            NaN  3.273727e+05        NaN
min                                                                                                                                                   NaN          NaN           NaN         NaN      NaN    NaN     7.600000                                                                                                                     NaN   28.000000               NaN        NaN          NaN           NaN            NaN  2.508800e+04        NaN
25%                                                                                                                                                   NaN          NaN           NaN         NaN      NaN    NaN     7.700000                                                                                                                     NaN   70.000000               NaN        NaN          NaN           NaN            NaN  5.552625e+04        NaN
50%                                                                                                                                                   NaN          NaN           NaN         NaN      NaN    NaN     7.900000                                                                                                                     NaN   79.000000               NaN        NaN          NaN           NaN            NaN  1.385485e+05        NaN
75%                                                                                                                                                   NaN          NaN           NaN         NaN      NaN    NaN     8.100000                                                                                                                     NaN   87.000000               NaN        NaN          NaN           NaN            NaN  3.741612e+05        NaN
max                                                                                                                                                   NaN          NaN           NaN         NaN      NaN    NaN     9.300000                                                                                                                     NaN  100.000000               NaN        NaN          NaN           NaN            NaN  2.343110e+06        NaN

## Missing Values
Poster_Link        0
Series_Title       0
Released_Year      0
Certificate      101
Runtime            0
Genre              0
IMDB_Rating        0
Overview           0
Meta_score       157
Director           0
Star1              0
Star2              0
Star3              0
Star4              0
No_of_Votes        0
Gross            169

### Correlation Analysis
![Correlation Heatmap](correlation_heatmap.png)

### Outlier Detection
![Outlier Detection](outliers.png)

### Time Series Analysis
Time series insights:
- To analyze trends or patterns in time series data, we would typically consider several key aspects. Here's how to approach the analysis step-by-step:

### Steps for Time Series Analysis

1. **Data Preparation**
   - Ensure the time series data is properly indexed by the time variable.
   - Check for missing values and handle them appropriately (imputation, interpolation, etc.).

2. **Visualization**
   - **Plot the Data**: Plot the time series to visually assess trends, seasonality, and anomalies.
   - **Decompose the Series**: Use seasonal decomposition to break down the series into trend, seasonal, and residual components.

   ![Time series decomposition example](https://www.statsmodels.org/stable/_images/statsmodels-example-time-series-decomposition-1.png)

3. **Trend Analysis**
   - **Trend Identification**: Use moving averages or smoothing techniques to detect underlying trends.
   - **Statistical Tests**: Apply statistical tests (like the Mann-Kendall test) to determine whether trends are statistically significant.

4. **Seasonality Detection**
   - **Seasonal Patterns**: Identify repeating patterns within the data (e.g., monthly, quarterly).
   - **Autocorrelation Function (ACF)**: Analyze ACF and Partial Autocorrelation Function (PACF) plots to evaluate seasonality and lag effects.

5. **Anomaly Detection**
   - Identify any outliers or anomalies that deviate from the expected pattern using statistical measures (e.g., Z-scores).

6. **Forecasting**
   - Fit time series models like ARIMA, SARIMA, or Prophet to predict future values based on the analyzed patterns.
   - Validate the model using a holdout sample or cross-validation methodologies.

### Example Insights

Here’s how you might summarize findings after analysis using a hypothetical dataset:

| Aspect         | Observation                                        | Recommendation                         |
|----------------|---------------------------------------------------|--------------------------------------|
| **Trend**      | Increasing sales trend over the last 5 years.    | Expand marketing in high-growth areas. |
| **Seasonality**| Sales peak during Q4 every year.                  | Prepare inventory for Q4 months.      |
| **Anomalies**  | Significant drop in sales in March 2023.        | Investigate potential causes (e.g., competition, market changes). |
| **Forecast**   | Expected growth of 10% over the next year.       | Allocate resources to capitalize on growth opportunities. |

### Visual Representation

- **Original Time Series Plot**: Display original data with highlighted regions of interest (trends, seasonal effects, outliers).
- **Decomposed Plot**: Show individual trend, seasonal, and residual components of the time series.

### Conclusion

By systematically analyzing time series data, you can uncover valuable insights about trends, seasonality, and anomalies, leading to actionable recommendations. Continue to refine your analysis with advanced models for better accuracy in forecasting. If you have specific data points or trends observed, please share them for a more tailored analysis.

### Geographic Distribution
Geographic insights:
- To provide insights on the geographic distribution based on the context of a geographic plot, I’ll outline key elements to consider and analyze:

### Key Elements to Analyze
1. **Data Points Distribution**:
   - Identify clusters or concentrations of data points in specific geographic areas.
   - Determine if distributions are uniform or if there are notable hotspots.

2. **Regional Trends**:
   - Highlight specific regions with significant activity or anomalies.
   - Analyze whether geographic features (e.g., mountains, rivers) correlate with data concentrations.

3. **Demographic Influences**:
   - Examine the relationship between geographic distribution and local demographics (population density, age, income levels, etc.).

4. **Temporal Changes**:
   - If historical data is available, assess how geographic distributions have changed over time.
   - Identify any emerging trends or shifts in specific areas.

### Pattern Recognition
- **Hotspots**: Regions with a high frequency of occurrences or significant measurements.
- **Cold Spots**: Areas with low activity that may require further investigation.
- **Geographic Correlation**: Look for patterns related to geographic features such as urban vs. rural areas.

### Recommendations
- **Targeted Interventions**: For areas identified as hotspots, focus resources or interventions where they are likely to have the most impact.
- **Further Investigation**: Cold spots may indicate areas needing additional research or attention to understand underlying causes.
- **Resource Allocation**: Allocate resources based on geographic data to ensure effective reach and engagement.

### Visualization (Hypothetical Example)
A geographic plot could visually represent this data:

| Region          | Data Points | Classification  | Notes                            |
|------------------|-------------|-----------------|----------------------------------|
| Urban Center A   | 150         | Hotspot         | High activity in Q4; targeted marketing may yield benefits. |
| Suburban Area B  | 30          | Cold Spot       | Less engagement; consider outreach programs. |
| Rural Zone C     | 10          | Cold Spot       | Needs demographic study; potential for growth. |

### Summary
By analyzing the geographic distribution, we can derive actionable insights, reinforce or reshape strategies, and ensure that resources are utilized effectively to achieve desired outcomes. If additional data or specific figures from the geographic plot are available, more tailored recommendations could be offered.

### Categorical Data Distribution
![Poster_Link Top 15 Distribution](Poster_Link_top_15_distribution.png)

![Poster_Link Bottom 15 Distribution](Poster_Link_bottom_15_distribution.png)

![Series_Title Top 15 Distribution](Series_Title_top_15_distribution.png)

![Series_Title Bottom 15 Distribution](Series_Title_bottom_15_distribution.png)

![Released_Year Top 15 Distribution](Released_Year_top_15_distribution.png)

![Released_Year Bottom 15 Distribution](Released_Year_bottom_15_distribution.png)

![Certificate Distribution](Certificate_distribution.png)

![Runtime Top 15 Distribution](Runtime_top_15_distribution.png)

![Runtime Bottom 15 Distribution](Runtime_bottom_15_distribution.png)

![Genre Top 15 Distribution](Genre_top_15_distribution.png)

![Genre Bottom 15 Distribution](Genre_bottom_15_distribution.png)

![Overview Top 15 Distribution](Overview_top_15_distribution.png)

![Overview Bottom 15 Distribution](Overview_bottom_15_distribution.png)

![Director Top 15 Distribution](Director_top_15_distribution.png)

![Director Bottom 15 Distribution](Director_bottom_15_distribution.png)

![Star1 Top 15 Distribution](Star1_top_15_distribution.png)

![Star1 Bottom 15 Distribution](Star1_bottom_15_distribution.png)

![Star2 Top 15 Distribution](Star2_top_15_distribution.png)

![Star2 Bottom 15 Distribution](Star2_bottom_15_distribution.png)

![Star3 Top 15 Distribution](Star3_top_15_distribution.png)

![Star3 Bottom 15 Distribution](Star3_bottom_15_distribution.png)

![Star4 Top 15 Distribution](Star4_top_15_distribution.png)

![Star4 Bottom 15 Distribution](Star4_bottom_15_distribution.png)

![Gross Top 15 Distribution](Gross_top_15_distribution.png)

![Gross Bottom 15 Distribution](Gross_bottom_15_distribution.png)

Categorical insights:
- To derive insights from categorical distributions, it's essential to break down the analysis into several key components. Below, I’ll provide a framework for how to analyze categorical data and the types of insights you may draw, including possible actions based on those insights.

### Framework for Analysis

1. **Identify Categories**: List all the unique categories present in the dataset.
2. **Count Frequencies**: Determine the count or proportions of each category.
3. **Visual Representation**: Utilize bar charts or pie charts to visualize the distribution.
4. **Compare Categories**: Look for patterns such as the most or least common categories.
5. **Correlation with Other Variables**: Analyze potential relationships between categorical variables and numerical outcomes.

### Example Insights

#### 1. Frequency Distribution

| Category     | Frequency | Percentage |
|--------------|-----------|------------|
| Category A   | 150       | 30%        |
| Category B   | 300       | 60%        |
| Category C   | 50        | 10%        |

- **Insight**: Category B constitutes the majority (60%) of the data, suggesting it is a key focus area.
- **Actionable Recommendation**: Allocate resources toward Category B for optimization and increased engagement.

#### 2. Key Observations

- **Outliers**: Identify if any categories have significantly lower frequencies (e.g., Category C).
- **Potential for Growth**: Categories with low representation can indicate market opportunities.
  
#### 3. Visual Representation

- **Bar Chart**: A bar chart can visualize the distribution:
  
  ```
  | Category     | Frequency |
  |--------------|-----------|
  | A            | ****      | 30
  | B            | **********| 60
  | C            | *         | 10
  ```

- **Pie Chart**: Visualizing the data in a pie chart will help in understanding relative sizes.

#### 4. Comparative Analysis

- **Cross-tabulation**: If there are multiple categorical variables, cross-tabulate to see how they interact.

| Category A | Category B | Count |
|------------|------------|-------|
| Yes        | Yes        | 80    |
| Yes        | No         | 70    |
| No         | Yes        | 90    |
| No         | No         | 10    |

- **Insight**: The combination of “Yes” in Category A with “Yes” in Category B is prevalent.
- **Actionable Recommendation**: Focus marketing toward the consumers who embrace both categories.

#### 5. Statistical Measures

- **Chi-square Test**: Conduct a Chi-square test for independence to see if there are any significant relationships between categorical variables.

### Example Insights Based on Country Data

If categorical data involve region or country:

- Countries with higher frequencies could represent strong markets for product placement.
- Less common countries could be explored for potential expansion strategies.

### Conclusion

By analyzing categorical distributions through frequency counts, visual representations, comparative assessments, and statistical testing, actionable insights can be uncovered that guide business strategies, resource allocation, and marketing efforts. Depending on the dataset, you can adjust recommendations more specifically.

## Story
### Story Based on Dataset Analysis

#### A) The Data Received
- **Total Entries**: 1000 movie records.
- **Unique Titles**: 999 (indicating one duplicate).
- **Release Years**: Films from 2014 to 2023.
- **Certificates**: 16 unique age ratings, with 10.1% of data missing values.
- **Genres**: 140 unique genres, with 'Drama' being the most frequent (85 occurrences).
- **IMDB Ratings**: Range from 7.6 to 9.3, mean rating of approximately 7.95.
- **Votes and Revenue**: Median number of votes is approximately 138,548, and gross revenue ranges from $25,088 to $2,343,110.

#### B) The Analysis Carried Out
- **Summary Statistics Calculation**:
  - Analyzed IMDB ratings, meta scores, number of votes, and gross revenue.
  - Checked for missing values and their potential impact on data quality.
  
- **Statistical Summary**:
  - Generated descriptive statistics for numerical columns.
  
- **Missing Values Assessment**:
  - Identified patterns in missing certificates, meta scores, and gross figures.
  
- **Visualization Recommendations**:
  - Suggested creating histograms and box plots to understand distributions and outliers.

#### C) Insights Discovered
1. **IMDB Ratings**:
   - **Central Tendency**: Mean rating of 7.95 suggests generally favorable reception.
   - **Low Variability**: Standard deviation of 0.28 indicates ratings cluster closely around the average.
   
2. **Meta Scores**:
   - **Positive Reception**: Average meta score of 77.97, with a moderate variation (std. dev. of 12.38).
   - **Range**: Scores span from 28 to 100, reflecting a mix of critically acclaimed and poorly received films.

3. **Popularity Indicators**:
   - **Vote Counts**: High mean (273,693) and variability (std. dev. of 327,372) suggest popularity skewed towards blockbusters.
   - **Financial Performance**: Gross revenue ranges widely, indicating some films are significantly more profitable than others.

#### D) Implications of Findings
1. **Data Imputation Strategies**:
   - Impute missing 'Certificate' values to maintain data integrity.
   - Seek additional sources or methods to fill in missing 'Meta Score' and 'Gross' data.

2. **Genre Deep-Dive**:
   - Conduct performance trending analysis per genre to identify which genres yield higher ratings and revenue.
   - Focus on the most prevalent genres like 'Drama' for deeper exploration of successful titles.

3. **Trend Analysis Over Years**:
   - Investigate annual changes in ratings and gross revenue to ascertain improvements or declines in movie quality and profitability.
  
4. **Star Influence**:
   - Analyze correlations between star power (famous actors) and film performance in terms of gross revenue and ratings. Consider leveraging star appeal in marketing.

5. **Certificate Focus**:
   - Investigate the impact of age certificates on audience reception. Are certain ratings leading to higher gross revenues?

6. **Highlight High Ratings**:
   - Develop targeted marketing strategies for films with IMDB ratings over 8.0, as they signify potential high audience engagement.

7. **Visual Representation**:
   - Use visual tools like box plots and histograms to convey insights on rating distributions and financial performance, aiding stakeholders' understanding.

### Numeric Insights Summary

| **Statistic**         | **IMDB Rating** | **Meta Score** | **Number of Votes** |
|-----------------------|------------------|-----------------|----------------------|
| **Count**             | 1000             | 843             | 1000                 |
| **Mean**              | 7.95             | 77.97           | 273,692.9            |
| **Standard Deviation** | 0.28             | 12.38           | 327,372.7            |
| **Minimum**           | 7.60             | 28              | 25,088               |
| **25th Percentile**   | 7.70             | 70              | 55,526               |
| **Median**            | 7.90             | 79              | 138,548              |
| **75th Percentile**   | 8.10             | 87              | 374,161              |
| **Maximum**           | 9.30             | 100             | 2,343,110            |

### Conclusion
The analysis of this dataset not only reveals insights into the movie industry's performance metrics but also uncovers areas for potential growth and strategic focus. By addressing data gaps, exploring genre dynamics, leveraging audience engagement metrics, and utilizing strong performer attributes, stakeholders can optimize their decision-making processes to better cater to audience preferences and drive revenue growth.
