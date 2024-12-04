# Data Analysis Report for file python/tdsproject2/goodreads/goodreads.csv

## Data Quality Report
**Total Rows:**
- 10000
**Total Columns:**
- 23
**Missing Values:**
- book_id: 0
- goodreads_book_id: 0
- best_book_id: 0
- work_id: 0
- books_count: 0
- isbn: 700
- isbn13: 585
- authors: 0
- original_publication_year: 21
- original_title: 585
- title: 0
- language_code: 1084
- average_rating: 0
- ratings_count: 0
- work_ratings_count: 0
- work_text_reviews_count: 0
- ratings_1: 0
- ratings_2: 0
- ratings_3: 0
- ratings_4: 0
- ratings_5: 0
- image_url: 0
- small_image_url: 0
**Data Types:**
- book_id: int64
- goodreads_book_id: int64
- best_book_id: int64
- work_id: int64
- books_count: int64
- isbn: object
- isbn13: float64
- authors: object
- original_publication_year: float64
- original_title: object
- title: object
- language_code: object
- average_rating: float64
- ratings_count: int64
- work_ratings_count: int64
- work_text_reviews_count: int64
- ratings_1: int64
- ratings_2: int64
- ratings_3: int64
- ratings_4: int64
- ratings_5: int64
- image_url: object
- small_image_url: object
**Unique Values:**
- book_id: 10000
- goodreads_book_id: 10000
- best_book_id: 10000
- work_id: 10000
- books_count: 597
- isbn: 9300
- isbn13: 9153
- authors: 4664
- original_publication_year: 293
- original_title: 9274
- title: 9964
- language_code: 25
- average_rating: 184
- ratings_count: 9003
- work_ratings_count: 9053
- work_text_reviews_count: 4581
- ratings_1: 2630
- ratings_2: 4117
- ratings_3: 6972
- ratings_4: 7762
- ratings_5: 8103
- image_url: 6669
- small_image_url: 6669

## Statistical Analysis
### Descriptive Statistics
| Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|--------|-------|------|-----|-----|-----|-----|-----|-----|
| book_id | 10000.0 | 5000.5 | 2886.8956799071675 | 1.0 | 2500.75 | 5000.5 | 7500.25 | 10000.0 |
| goodreads_book_id | 10000.0 | 5264696.5132 | 7575461.863589611 | 1.0 | 46275.75 | 394965.5 | 9382225.25 | 33288638.0 |
| best_book_id | 10000.0 | 5471213.5801 | 7827329.890719961 | 1.0 | 47911.75 | 425123.5 | 9636112.5 | 35534230.0 |
| work_id | 10000.0 | 8646183.4246 | 11751060.824080039 | 87.0 | 1008841.0 | 2719524.5 | 14517748.25 | 56399597.0 |
| books_count | 10000.0 | 75.7127 | 170.47072765025834 | 1.0 | 23.0 | 40.0 | 67.0 | 3455.0 |
| isbn13 | 9415.0 | 9755044298883.463 | 442861920665.57336 | 195170342.0 | 9780316192995.0 | 9780451528640.0 | 9780830777175.0 | 9790007672390.0 |
| original_publication_year | 9979.0 | 1981.987674115643 | 152.57666516754668 | -1750.0 | 1990.0 | 2004.0 | 2011.0 | 2017.0 |
| average_rating | 10000.0 | 4.002191000000001 | 0.25442748053872905 | 2.47 | 3.85 | 4.02 | 4.18 | 4.82 |
| ratings_count | 10000.0 | 54001.2351 | 157369.95643554674 | 2716.0 | 13568.75 | 21155.5 | 41053.5 | 4780653.0 |
| work_ratings_count | 10000.0 | 59687.3216 | 167803.7852374182 | 5510.0 | 15438.75 | 23832.5 | 45915.0 | 4942365.0 |
| work_text_reviews_count | 10000.0 | 2919.9553 | 6124.378131569911 | 3.0 | 694.0 | 1402.0 | 2744.25 | 155254.0 |
| ratings_1 | 10000.0 | 1345.0406 | 6635.626262783459 | 11.0 | 196.0 | 391.0 | 885.0 | 456191.0 |
| ratings_2 | 10000.0 | 3110.885 | 9717.123578396993 | 30.0 | 656.0 | 1163.0 | 2353.25 | 436802.0 |
| ratings_3 | 10000.0 | 11475.8938 | 28546.449183182456 | 323.0 | 3112.0 | 4894.0 | 9287.0 | 793319.0 |
| ratings_4 | 10000.0 | 19965.6966 | 51447.35838380058 | 750.0 | 5405.75 | 8269.5 | 16023.5 | 1481305.0 |
| ratings_5 | 10000.0 | 23789.8056 | 79768.88561077163 | 754.0 | 5334.0 | 8836.0 | 17304.5 | 3011543.0 |
### Skewness
- book_id: 0.0
- goodreads_book_id: 1.3450513460623226
- best_book_id: 1.3501105965199585
- work_id: 1.7627888851221998
- books_count: 8.408830046446552
- isbn13: nan
- original_publication_year: nan
- average_rating: -0.5115402712762502
- ratings_count: 13.056937765958065
- work_ratings_count: 12.41265961075493
- work_text_reviews_count: 9.128828420036513
- ratings_1: 37.70594081575401
- ratings_2: 16.490237450570774
- ratings_3: 10.397906022313085
- ratings_4: 10.805281499311098
- ratings_5: 16.371074464371038
### Kurtosis
- book_id: -1.2000000240000006
- goodreads_book_id: 0.6877880006303982
- best_book_id: 0.7455236635400508
- work_id: 2.492260588357113
- books_count: 95.25480435603895
- isbn13: nan
- original_publication_year: nan
- average_rating: 0.8810778699146051
- ratings_count: 258.6161476127255
- work_ratings_count: 233.9543612299873
- work_text_reviews_count: 133.9792532453793
- ratings_1: 2288.469084590992
- ratings_2: 493.81813757193135
- ratings_3: 160.74709915460724
- ratings_4: 173.93804062246545
- ratings_5: 419.6704232912079
## Visualizations
![Pairplot](img/pairplot.png)
## Dimensionality Reduction
Reduced Data Shape: (10000, 2)

## KMeans Clustering
Clustered Data:
   book_id  goodreads_book_id  best_book_id    work_id  ...  ratings_5                                          image_url                                    small_image_url Cluster
0      1.0          2767052.0     2767052.0  2792775.0  ...  2706317.0  https://images.gr-assets.com/books/1447303603m...  https://images.gr-assets.com/books/1447303603s...      -1
1      2.0                3.0           3.0  4640799.0  ...  3011543.0  https://images.gr-assets.com/books/1474154022m...  https://images.gr-assets.com/books/1474154022s...      -1
2      3.0            41865.0       41865.0  3212258.0  ...  1355439.0  https://images.gr-assets.com/books/1361039443m...  https://images.gr-assets.com/books/1361039443s...      -1
3      4.0             2657.0        2657.0  3275794.0  ...  1714267.0  https://images.gr-assets.com/books/1361975680m...  https://images.gr-assets.com/books/1361975680s...      -1
4      5.0             4671.0        4671.0   245494.0  ...   947718.0  https://images.gr-assets.com/books/1490528560m...  https://images.gr-assets.com/books/1490528560s...      -1

[5 rows x 24 columns]

![KMean Clustering](img/kmeans_clustering.png)
![Word Cloud](img/word_cloud.png)
## Content Summary
### Detailed Summary of the Dataset

The provided dataset appears to be a collection of book information sourced from Goodreads, with entries for various books, their metadata, and user-generated ratings. 

#### Overall Dataset Composition:
- The dataset contains six primary observations, each corresponding to a distinct book. There are 25 fields in total, covering various attributes of the books.
- Key identifiers include `book_id`, `goodreads_book_id`, `best_book_id`, and `work_id`, which are unique identifiers for the books.
- Attributes such as `authors`, `original_publication_year`, `original_title`, `title`, and `language_code` provide contextual information about each book.
- The dataset includes several numeric fields dealing with ratings and reviews, offering quantifiable measures of the books’ popularity and reception.

#### Key Variables and Their Significance:
- **`average_rating`**: This numeric field indicates the average user rating for each book on Goodreads, likely on a scale from 1 to 5. Higher ratings generally reflect positive reception.
- **`ratings_count`**: This value shows how many users have rated the book, indicating its popularity among readers.
- **`work_text_reviews_count`**: Counts the number of text reviews for the book, suggesting that it has garnered considerable user engagement.
- **`ratings_1` to `ratings_5`**: These fields categorize the counts of ratings across five tiers, providing insight into how polarized or consensual the ratings are. For example, a high count in `ratings_5` and low in `ratings_1` indicates a favorable reception.
- **`image_url` and `small_image_url`**: These fields contain URLs linking to images of the book covers, enhancing visual engagement with the data.

#### Notable Patterns or Trends:
1. **Rating Distribution**: 
   - Books like "Harry Potter and the Philosopher's Stone" and "The Hunger Games" have a high `average_rating` (4.44 and 4.34 respectively) supported by massive `ratings_count` (over 4 million ratings). This indicates strong reader loyalty and acclaim.
   - In contrast, "Twilight" has a lower average rating (3.57), suggesting that while popular, it has polarized opinions among readers.

2. **Impact of Publication Year**:
   - The dataset includes books from various decades, with older classics like "To Kill a Mockingbird" (1960) holding strong ratings (4.25). This suggests that quality literature retains value over time.

3. **Engagement Metrics**:
   - The number of text reviews correlates with `ratings_count`, indicating that more popular books often elicit substantial reader feedback, affirming reader engagement with the material.

#### Potential Insights or Implications:
- **Market Trends**: The prominence of fantasy and young adult genres (“Harry Potter” and “Twilight”) may indicate a trend toward more magical or adventurous literature appealing to younger audiences.
- **Timelessness**: The sustained popularity of classic literature demonstrates the long-lasting appeal of well-crafted storytelling that transcends time and engages new generations.
- **Reader Behavior**: High engagement metrics, such as ratings and reviews, can inform marketing strategies for publishers, indicating which books may benefit from additional promotion or highlighting in campaigns.

#### Conclusion:
This dataset serves as an invaluable resource for studying reader preferences and the dynamics of book reception over time. Future analyses could explore correlations between publication years and ratings to assess the evolving landscape of literature tastes. Additionally, examining regional language codes could provide insights into cultural reception of these works across different demographics.
