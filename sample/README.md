# Every data tell's a story

## Story
# The Journey of Data in Cinema: An Analytical Tale from IMDB’s Top 1000 Films

## 1. The Data We Received
In our quest to uncover the secrets of cinematic success, we received a richly detailed dataset titled `imdb_top_1000.csv`. This dataset includes key attributes for the top 1000 films, containing:

- **Basic Information**: Series title, released year, and a synopsis.
- **Ratings**: IMDB ratings, meta scores, and total votes.
- **Financial Data**: Gross earnings (though with some missing data).
- **Cast and Crew**: Directors and leading stars.
- **Genres**: A broad spectrum of cinematic styles.

### Overview of Key Columns
| Column            | Description                                              | Unique Values |
|-------------------|----------------------------------------------------------|---------------|
| `Series_Title`    | Title of the film                                       | 999           |
| `Released_Year`   | Year of release                                        | 100 years     |
| `IMDB_Rating`     | Viewer rating on IMDB                                  | Range: 7.6 - 9.3 |
| `Meta_score`      | Critic assessment score                                 | Range: 28 - 100   |
| `Gross`           | Total gross earnings                                    | Missing for 169 |

### Visualizing Data Availability
![Image illustrating the presence of missing values in various columns](missing_values_plot.png)

## 2. The Analysis We Carried Out
After cleansing the data, we conducted extensive analyses including:

- **Statistical Summary**: Delivered insights into central trends and dispersion metrics for key numerical variables (e.g., IMDB ratings, meta scores, and gross earnings).
  
- **Correlation Analysis**: A pivotal examination of how IMDB ratings, meta scores, and the number of votes interact. The correlation heatmap illustrated the dynamics within these attributes.

![Correlation Heatmap](correlation_heatmap.png)

| Pairing                    | Correlation Coefficient | Strength           |
|---------------------------|-------------------------|---------------------|
| IMDB_Rating & Meta_score  | 0.27                    | Weak Positive       |
| IMDB_Rating & No_of_Votes | 0.49                    | Moderate Positive    |
| Meta_score & No_of_Votes  | -0.02                   | Very Weak Negligible |

- **Categorical Distributions**: Evaluated categorical data to discern popular genres, directors, and top films.

### Outlier Detection for Financial Analysis
![Outlier Detection Chart](outliers.png)

Utilizing box plots, we identified potential outliers in gross earnings and votes, indicating films that either drastically underperform or outperform expected metrics.

## 3. Insights We Discovered
From our analysis, several key insights emerged:

### **A. Ratings and Popularity**
- **High Viewer Satisfaction**: The average IMDB rating of **7.95** conveys that most films received positive reviews from audiences.
- **Critical Reception**: Meta scores averaged **77.97**, showcasing critical acclaim, albeit with notable missing values (15.7% of entries).

### **B. Relationship Dynamics**
- **Votes and Ratings**: The moderate positive correlation (0.49) suggests that films with higher IMDB ratings generally receive more votes, validating the notion that quality begets popularity.

### **C. Genre Trends and Distribution**
- Diverse genres with varying representation indicate potential gaps where marketing or production teams might diversify offerings.

### **D. Market Potential**
- Gross earnings command attention; however, missing data for **16.9%** of entries invites caution and further investigation into box-office performances for a more rounded perspective.

## 4. The Implications of Our Findings
The practical implications of these insights are multi-faceted and can aid decision-making within the cinematic industry:

### Actionable Recommendations
1. **Enhance Viewer Engagement for High-Performing Films**: Develop targeted marketing strategies for films rated above 8.0, leveraging their strong ratings to boost audience visibility and engagement.
  
2. **Investigate Underperformers**: Delve into films with low votes but high ratings to understand audience engagement barriers and explore opportunities for increased visibility.

3. **Focus on Trends by Genre**: Expand production in genres exhibiting high viewer satisfaction and critical acclaim, tapping into audience preferences reflected in the data.

4. **Data Completion Strategies**: Address the shortcomings of missing financial data by implementing measures to collect complete data for a clearer financial outline, ensuring reliable performance insights.

### Visual Representation of Recommendations
Consider scatter plots visualizing the relationship between **IMDB Ratings** and **No of Votes** to identify outliers and patterns effectively over time.

![Scatter Plot Example](scatter_plot.png)

## Conclusion
Through this analytical journey, we transformed raw data into actionable insights within the world of cinema. The findings carved pathways for strategic recommendations that could optimize production, marketing strategies, and ultimately enhance viewer satisfaction across the industry's landscape. As the cinematic world evolves, leveraging data insights will remain crucial for thriving within the competitive arena of film.
