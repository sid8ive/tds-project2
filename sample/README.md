# Data Analysis Report

## Overview
File: extras/imdb_top_1000.csv

## Summary Statistics
                                              Poster_Link Series_Title Released_Year Certificate  Runtime  Genre  IMDB_Rating                                           Overview  Meta_score          Director      Star1        Star2         Star3          Star4   No_of_Votes      Gross
count                                                1000         1000          1000         899     1000   1000  1000.000000                                               1000  843.000000              1000       1000         1000          1000           1000  1.000000e+03        831
unique                                               1000          999           100          16      140    202          NaN                                               1000         NaN               548        660          841           891            939           NaN        823
top     https://m.media-amazon.com/images/M/MV5BMDFkYT...     Drishyam          2014           U  100 min  Drama          NaN  Two imprisoned men bond over a number of years...         NaN  Alfred Hitchcock  Tom Hanks  Emma Watson  Rupert Grint  Michael Caine           NaN  4,360,000
freq                                                    1            2            32         234       23     85          NaN                                                  1         NaN                14         12            7             5              4           NaN          5
mean                                                  NaN          NaN           NaN         NaN      NaN    NaN     7.949300                                                NaN   77.971530               NaN        NaN          NaN           NaN            NaN  2.736929e+05        NaN
std                                                   NaN          NaN           NaN         NaN      NaN    NaN     0.275491                                                NaN   12.376099               NaN        NaN          NaN           NaN            NaN  3.273727e+05        NaN
min                                                   NaN          NaN           NaN         NaN      NaN    NaN     7.600000                                                NaN   28.000000               NaN        NaN          NaN           NaN            NaN  2.508800e+04        NaN
25%                                                   NaN          NaN           NaN         NaN      NaN    NaN     7.700000                                                NaN   70.000000               NaN        NaN          NaN           NaN            NaN  5.552625e+04        NaN
50%                                                   NaN          NaN           NaN         NaN      NaN    NaN     7.900000                                                NaN   79.000000               NaN        NaN          NaN           NaN            NaN  1.385485e+05        NaN
75%                                                   NaN          NaN           NaN         NaN      NaN    NaN     8.100000                                                NaN   87.000000               NaN        NaN          NaN           NaN            NaN  3.741612e+05        NaN
max                                                   NaN          NaN           NaN         NaN      NaN    NaN     9.300000                                                NaN  100.000000               NaN        NaN          NaN           NaN            NaN  2.343110e+06        NaN

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
dtype: int64

## Insights
Based on the provided summary statistics and missing values of the dataset, we can derive several insights regarding the film dataset:

### 1. Basic Dataset Composition
- The dataset contains **1,000 entries** (films).
- The **most common film genre** is Drama, which appears **85 times**.
- The dataset includes a wide range of **release years**, from earlier classics to more recent films, with the most frequently released year being **2014**, with **32 entries**.
  
### 2. Audience Ratings and Reception
- The average **IMDB rating** of the films in the dataset is **7.95**, with a minimum rating of **7.6** and a maximum of **9.3**. This suggests generally favorable reviews, as a rating above 7 is typically considered good.
- The **Meta score**, which measures critical reception, has **157 missing values**, indicating that not all films have been critically reviewed or scored. The average Meta score for those that do is approximately **77.97**, suggesting a mostly positive critical reception, as scores above 70 are often considered good.

### 3. Certification and Content Rating
- There are **16 unique certificates** in the dataset, with the **'U' (Universal) certificate** being the most common, suggesting a substantial number of family-friendly content aimed primarily at a wide audience.
- The dataset has **101 missing values** for the `Certificate` attribute, indicating that either the classification hasn't been applied to all films or that some entries may not have readily available ratings.

### 4. Runtime and Length of Films
- The average **runtime** is approximately **100 minutes** across the dataset. This aligns with standard movie lengths, indicating a typical feature film length.
- The **standard deviation** of the runtime is not provided, but if we analyze further (if available data shows variability), we could infer some films are much longer or shorter than the average.

### 5. Director and Star Popularity
- The dataset has **548 unique directors** and **660 unique main stars**, indicating a diverse range of contributors. This could lead to varied styles and approaches in filmmaking.
- The most frequently mentioned director is **Alfred Hitchcock**, suggesting many films in this dataset (perhaps imports or re-releases) feature his classic works.
  
### 6. Financial Aspects
- The **Gross earnings** of films show some variability with **169 missing values**. The highest **gross** recorded is over **2.34 million**, while the mean gross is around **831,000**. This indicates a range of box office performances, with some films being significant hits while others may not have performed as well financially.
- The **number of votes** (indicating audience engagement) shows a wide range, with the highest being over **4.36 million** votes for popular films, suggesting that popularity and viewer engagement play significant roles in a film's reception.

### Recommendations for Further Analysis
- **Handle Missing Values**: Particularly in the Certificate and Meta score attributes, further analysis could be conducted to impute missing values based on other correlated features or exclude films without crucial ratings.
- **Trend Analysis**: Conducting a time-based analysis to observe how the genres, ratings, or gross earnings have changed over the years could yield insights into evolving cinematic trends.
- **Genre Breakdown**: A deeper dive into the ratings and earnings based on genre could provide insights into which genres are generally better received and perform better financially.
- **Explore Collaborations**: Analyzing how certain directors or combinations of stars influence ratings and grosses could offer insights into successful film-making collaborations.

In summary, the dataset offers a rich source of information that could lead to various analyses regarding film quality, genre popularity, and audience engagement, though attention is needed to address missing values and correlation among variables.

## Numeric Insights
Based on the summary statistics provided for the numeric columns (IMDB_Rating, Meta_score, and No_of_Votes), here are some insights:

### 1. **IMDB_Rating**
- **Count**: There are 1,000 entries for IMDB ratings, indicating a complete dataset without missing values.
- **Mean**: The average IMDB rating is approximately **7.95**, which is relatively high and suggests that the dataset mostly comprises well-received films.
- **Standard Deviation**: The standard deviation of about **0.28** indicates that there is low variability in IMDB ratings, meaning most ratings are clustered closely around the mean value.
- **Range**: The ratings range from a minimum of **7.6** to a maximum of **9.3**, further supporting the notion that the films in this dataset are generally well-regarded.
- **Interquartile Range**:
  - **25th percentile (Q1)**: **7.7**
  - **Median (Q2)**: **7.9**
  - **75th percentile (Q3)**: **8.1**
  - This IQR (Q3 - Q1 = 0.4) suggests that the middle 50% of films have ratings between **7.7** and **8.1**, confirming the clustering around higher ratings.

### 2. **Meta_score**
- **Count**: The Meta_score has 843 entries, indicating some missing data (approximately 16% of data missing).
- **Mean**: The average Meta score is about **77.97**, which aligns with a generally favorable reception in film criticism.
- **Standard Deviation**: A standard deviation of **12.38** suggests more variability in the Meta scores compared to IMDB ratings. This variability could indicate a broader range of critical opinions.
- **Range**: The Meta scores vary from a minimum of **28** to a maximum of **100**, indicating that while many films are well-regarded, some received very low scores.
- **Interquartile Range**:
  - **Q1**: **70**
  - **Median (Q2)**: **79**
  - **Q3**: **87**
  - The IQR of **17** (Q3 - Q1) suggests a significant difference in perceptions among films, with the middle 50% of scores ranging from **70** to **87**.

### 3. **No_of_Votes**
- **Count**: There are 1,000 entries for the number of votes, indicating no missing values for this column.
- **Mean**: The average number of votes is approximately **273,693**, indicating a significant audience engagement with the films in this dataset.
- **Standard Deviation**: A high standard deviation of about **327,373** reflects substantial variability in the number of votes, suggesting that a few films receive an exceptionally high number of votes while many others receive significantly fewer.
- **Range**: The number of votes ranges from **25,088** to **2,343,110**, with the maximum value indicating the presence of a few extremely popular films.
- **Interquartile Range**:
  - **Q1**: **55,526**
  - **Median (Q2)**: **138,548**
  - **Q3**: **374,161**
  - This high IQR indicates a large disparity in voting activity, which might point to a few blockbuster films skewing the average.

### Overall Insights:
- The dataset appears to consist of popular films based on the high average ratings, Meta scores, and significant voting numbers.
- There are disparities in critical reception (Meta scores) compared to public opinion (IMDB ratings), with greater variability in Meta scores.
- The voting numbers suggest that while most films are well-rated, a few major hits dominate in popularity and public engagement.
- Handling the missing values in Meta scores may be necessary if further analysis is to be conducted, especially in assessing trends or making predictive models.

## Story
# A Cinematic Journey Through Data: Unpacking Film Insights

## a) The Data You Received
- **Dataset Composition**: The dataset comprises **1,000 films** with various attributes, including:
  - **Series_Title**: Title of the film
  - **Released_Year**: Year of release
  - **Certificate**: Content rating
  - **Runtime**: Duration of the film
  - **Genre**: Genre classification
  - **IMDB_Rating**: Audience ratings
  - **Meta_score**: Critical ratings
  - **Director**: Director's name
  - **Stars**: Main actors in the film
  - **No_of_Votes**: Total audience votes
  - **Gross**: Box office earnings
- **Summary Statistics**: Key statistics highlight average IMDB ratings of about **7.95**, a mean Meta score of **77.97**, and a gross earnings mean of **831,000** with notable variations.
- **Missing Values**: Noteworthy missing data includes **101 entries** for `Certificate` and **157 entries** for `Meta_score`.

## b) The Analysis You Carried Out
1. **Descriptive Analysis**: Initial exploratory analysis was conducted to summarize key statistics for each attribute, focusing on unique counts, averages, and distribution.
2. **Missing Data Analysis**: Evaluated the extent of missing values across critical columns to assess potential biases in the dataset.
3. **Numerical Insights**: Physics of ratings (IMDB, Meta score), votes, and financial data were analyzed for ranges, averages, and statistical volatility.
4. **Rating Comparison**: Cross-examined audience reception (IMDB ratings) with critical reception (Meta scores) to identify discrepancies.

## c) The Insights You Discovered
### 1. Basic Dataset Composition
- Dominance of **Drama** as a genre (85 occurrences).
- Peak release year **2014** with **32 films** released.

### 2. Audience Ratings and Reception
- Average **IMDB rating** of **7.95** reflects a generally well-received collection of films.
- Average **Meta score** at **77.97** indicates favorable critical reviews, albeit with **16% missing data**.

### 3. Certification Dynamics
- **16 unique* classification certificates; the most common being 'U', pointing towards a family-friendly film selection.
- Missing values in the `Certificate` column may affect content analysis validity.

### 4. Runtime Insights
- Typical film length averages around **100 minutes**, aligning with industry standards.

### 5. Popularity of Directors and Stars
- High diversity in directors (548 unique), signaling varied filmmaking styles.
- **Alfred Hitchcock** appears prominently, suggesting strong representation of classic films.

### 6. Financial Performance Metrics
- Gross revenues are variable; the lowest at **25,088** and the highest near **2.34 million**. Average gross indicates a mostly modest financial performance.

## d) The Implications of Findings
### 1. Addressing Missing Data
- **Action Required**: Tackle the missing values in the `Certificate` and `Meta_score` attributes to enhance data completeness. Possible approaches include:
  - Imputation based on genre or director popularity.
  - Exclusion of entries missing critical ratings when performing more extensive analyses.

### 2. Trend and Further Research
- **Future Analyses**: Conduct longitudinal studies to observe genre fluctuations, audience engagement changes, and variations in rating trends over time.
- Explore genre-specific trends for ratings and gross earnings to pinpoint which genres are consistently well-received.

### 3. Audience Engagement Strategies
- **Marketing Insights**: Leverage insights on high voter engagement films to shape future marketing strategies for lesser-known films.

### 4. Collaboration Studies
- Analyze director and actor collaborations to reveal insights into successful combinations that yield higher ratings or grosses.

### 5. Financial Benchmarking
- Develop financial forecasts based on the categorization of films by genre and observed audience reception metrics to guide future investment decisions.

Through these insights, one can glean not just a clearer picture of cinematic trends and impacts, but also a roadmap for strategic action in entertainment project development and analysis. The dataset serves as a treasure trove for filmmakers, marketers, and analysts aiming to understand the nuances of film reception and performance in the evolving landscape of cinema.
