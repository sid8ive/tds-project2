*Every story is complicated until it finds the right storyteller — Anonymous*


Statistical data in markup:
# Summary of findings

## Overview
File name: goodreads.csv

The file has 10000 rows and 23 columns

### Sample 5 rows from file, for context

Sample data:
|       isbn | authors                      | original_title        | title                                  | language_code   | image_url                                                                                                                      | small_image_url                                                                                                              |
|-----------:|:-----------------------------|:----------------------|:---------------------------------------|:----------------|:-------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------|
|  312374976 | Linda Castillo               | Sworn to Silence      | Sworn to Silence (Kate Burkholder, #1) | eng             | <img src="https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png" alt="Image" width="100" /> | <img src="https://s.gr-assets.com/assets/nophoto/book/50x75-a91bf249278a81aabab721ef782c4a74.png" alt="Image" width="100" /> |
|  140432108 | Anne Brontë, Angeline Goreau | Agnes Grey            | Agnes Grey                             |                 | <img src="https://images.gr-assets.com/books/1400875530m/298230.jpg" alt="Image" width="100" />                                | <img src="https://images.gr-assets.com/books/1400875530s/298230.jpg" alt="Image" width="100" />                              |
|   91879205 | Michael J. Fox               | Lucky Man             | Lucky Man                              | eng             | <img src="https://images.gr-assets.com/books/1398617130m/133729.jpg" alt="Image" width="100" />                                | <img src="https://images.gr-assets.com/books/1398617130s/133729.jpg" alt="Image" width="100" />                              |
| 1455559318 | Jodi Ellen Malpas            |                       | Promised (One Night, #1)               | eng             | <img src="https://images.gr-assets.com/books/1398092254m/21795430.jpg" alt="Image" width="100" />                              | <img src="https://images.gr-assets.com/books/1398092254s/21795430.jpg" alt="Image" width="100" />                            |
| 1101875046 | Judy Blume                   | In the Unlikely Event | In the Unlikely Event                  | eng             | <img src="https://images.gr-assets.com/books/1421711380m/23899174.jpg" alt="Image" width="100" />                              | <img src="https://images.gr-assets.com/books/1421711380s/23899174.jpg" alt="Image" width="100" />                            |

### Descriptive analysis of the data

|       |   book_id |   goodreads_book_id |     best_book_id |         work_id |   books_count |         isbn13 |   original_publication_year |   average_rating |    ratings_count |   work_ratings_count |   work_text_reviews_count |   ratings_1 |   ratings_2 |   ratings_3 |      ratings_4 |       ratings_5 |
|:------|----------:|--------------------:|-----------------:|----------------:|--------------:|---------------:|----------------------------:|-----------------:|-----------------:|---------------------:|--------------------------:|------------:|------------:|------------:|---------------:|----------------:|
| count |  10000    |     10000           |  10000           | 10000           |      10000    | 9415           |                     9979    |         10000    |  10000           |      10000           |                  10000    |    10000    |    10000    |     10000   | 10000          | 10000           |
| mean  |   5000.5  |         5.2647e+06  |      5.47121e+06 |     8.64618e+06 |         75.71 |    9.75504e+12 |                     1981.99 |             4    |  54001.2         |      59687.3         |                   2919.96 |     1345.04 |     3110.89 |     11475.9 | 19965.7        | 23789.8         |
| std   |   2886.9  |         7.57546e+06 |      7.82733e+06 |     1.17511e+07 |        170.47 |    4.42862e+11 |                      152.58 |             0.25 | 157370           |     167804           |                   6124.38 |     6635.63 |     9717.12 |     28546.5 | 51447.4        | 79768.9         |
| min   |      1    |         1           |      1           |    87           |          1    |    1.9517e+08  |                    -1750    |             2.47 |   2716           |       5510           |                      3    |       11    |       30    |       323   |   750          |   754           |
| 25%   |   2500.75 |     46275.8         |  47911.8         |     1.00884e+06 |         23    |    9.78032e+12 |                     1990    |             3.85 |  13568.8         |      15438.8         |                    694    |      196    |      656    |      3112   |  5405.75       |  5334           |
| 50%   |   5000.5  |    394966           | 425124           |     2.71952e+06 |         40    |    9.78045e+12 |                     2004    |             4.02 |  21155.5         |      23832.5         |                   1402    |      391    |     1163    |      4894   |  8269.5        |  8836           |
| 75%   |   7500.25 |         9.38223e+06 |      9.63611e+06 |     1.45177e+07 |         67    |    9.78083e+12 |                     2011    |             4.18 |  41053.5         |      45915           |                   2744.25 |      885    |     2353.25 |      9287   | 16023.5        | 17304.5         |
| max   |  10000    |         3.32886e+07 |      3.55342e+07 |     5.63996e+07 |       3455    |    9.79001e+12 |                     2017    |             4.82 |      4.78065e+06 |          4.94236e+06 |                 155254    |   456191    |   436802    |    793319   |     1.4813e+06 |     3.01154e+06 |

## Missing values report

|                           |   Missing Values Count |   Missing Percentage (%) |
|:--------------------------|-----------------------:|-------------------------:|
| book_id                   |                      0 |                     0    |
| goodreads_book_id         |                      0 |                     0    |
| best_book_id              |                      0 |                     0    |
| work_id                   |                      0 |                     0    |
| books_count               |                      0 |                     0    |
| isbn                      |                    700 |                     7    |
| isbn13                    |                    585 |                     5.85 |
| authors                   |                      0 |                     0    |
| original_publication_year |                     21 |                     0.21 |
| original_title            |                    585 |                     5.85 |
| title                     |                      0 |                     0    |
| language_code             |                   1084 |                    10.84 |
| average_rating            |                      0 |                     0    |
| ratings_count             |                      0 |                     0    |
| work_ratings_count        |                      0 |                     0    |
| work_text_reviews_count   |                      0 |                     0    |
| ratings_1                 |                      0 |                     0    |
| ratings_2                 |                      0 |                     0    |
| ratings_3                 |                      0 |                     0    |
| ratings_4                 |                      0 |                     0    |
| ratings_5                 |                      0 |                     0    |
| image_url                 |                      0 |                     0    |
| small_image_url           |                      0 |                     0    |


### Word Cloud Analysis
![Word Cloud](word_cloud.png)


Some of these most frequently words are: john, life, robert, james, girl, david, story, last, love, night, world, book, king, michael, dark, death, little, secret, stephen, tale.


![Correlation Heatmap](correlation_heatmap.png)


This heatmap visualizes the correlation between numerical features.


![Outlier Detection Box Plot](outlier_detection_box_plot.png)


This boxplot highlights potential outliers for numerical features.

### Outlier Summary:

|                |   book_id |   goodreads_book_id |   best_book_id |       work_id |   books_count |        isbn13 |   original_publication_year |   average_rating |   ratings_count |   work_ratings_count |   work_text_reviews_count |   ratings_1 |   ratings_2 |   ratings_3 |   ratings_4 |   ratings_5 |
|:---------------|----------:|--------------------:|---------------:|--------------:|--------------:|--------------:|----------------------------:|-----------------:|----------------:|---------------------:|--------------------------:|------------:|------------:|------------:|------------:|------------:|
| lower_bound    |   -4998.5 |        -1.39576e+07 |   -1.43344e+07 |  -1.92545e+07 |           -43 |   9.77954e+12 |                      1958.5 |            3.355 |        -27658.4 |             -30275.6 |                  -2381.38 |      -837.5 |    -1889.88 |     -6150.5 |    -10520.9 |    -12621.8 |
| upper_bound    |   14999.5 |         2.33861e+07 |    2.40184e+07 |   3.47811e+07 |           133 |   9.7816e+12  |                      2042.5 |            4.675 |         82280.6 |              91629.4 |                   5819.62 |      1918.5 |     4899.12 |     18549.5 |     31950.1 |     35260.2 |
| outliers_count |       0   |       345           |  357           | 601           |           844 | 556           |                      1031   |          158     |          1163   |               1143   |                   1005    |      1140   |     1156    |      1149   |      1131   |      1158   |


### Time Series Analysis
![Time Series Analysis](time_series_analysis.png)


This line plot shows trends over time for numerical data with a `Date` column.




<!--### Geographic Distribution
No geographic data found
-->



<!--### Network Analysis
No network analysis generated
-->



### Categorical Data Distribution
The following plots show the distribution of categorical data:

![Distribution of isbn](distribution_of_isbn.png)


This bar chart shows the distribution of `isbn` column.

Sample 5 rows from provided data, for context to Categorical distribution 
| isbn       |
|:-----------|
| 140278404X |
| 6640613    |
| 440243394  |
| 380017601  |
| 553381334  |
![Distribution of authors](distribution_of_authors.png)


This bar chart shows the distribution of `authors` column.

Sample 5 rows from provided data, for context to Categorical distribution 
| authors           |
|:------------------|
| Becca Fitzpatrick |
| Lincoln Peirce    |
| Daphne du Maurier |
| Dean Koontz       |
| Linda Castillo    |
![Distribution of original_title](distribution_of_original_title.png)


This bar chart shows the distribution of `original_title` column.

Sample 5 rows from provided data, for context to Categorical distribution 
| original_title              |
|:----------------------------|
| The Executioners            |
| Aesopica                    |
| Dry: A Memoir               |
| Batman Chronicles: Volume 1 |
| بوف کور                     |




### Numerical Data Histograms

This histogram plot represents the distribution of `book_id` column.

![Distribution of book_id](distribution_of_book_id.png)

This histogram plot represents the distribution of `goodreads_book_id` column.

![Distribution of goodreads_book_id](distribution_of_goodreads_book_id.png)

This histogram plot represents the distribution of `best_book_id` column.

![Distribution of best_book_id](distribution_of_best_book_id.png)



![Cluster Analysis](cluster_analysis.png)


This scatter plot represents the cluster analysis results.

Sample data with clusters:

|   book_id |   goodreads_book_id |   best_book_id |   work_id |   books_count | isbn       | isbn13          | authors             |   original_publication_year | original_title            | title                                            | language_code   |   average_rating |   ratings_count |   work_ratings_count |   work_text_reviews_count |   ratings_1 |   ratings_2 |   ratings_3 |   ratings_4 |   ratings_5 | image_url                                                   | small_image_url                                             |   Cluster |
|----------:|--------------------:|---------------:|----------:|--------------:|:-----------|:----------------|:--------------------|----------------------------:|:--------------------------|:-------------------------------------------------|:----------------|-----------------:|----------------:|---------------------:|--------------------------:|------------:|------------:|------------:|------------:|------------:|:------------------------------------------------------------|:------------------------------------------------------------|----------:|
|       773 |               47021 |          47021 |   3152341 |           689 | 074347757X | 9780743477570.0 | William Shakespeare |                        1593 | The Taming of the Shrew   | The Taming of the Shrew                          | en-US           |             3.81 |          126318 |               134240 |                      2370 |        2869 |        9611 |       35666 |       47453 |       38641 | https://images.gr-assets.com/books/1327935253m/47021.jpg    | https://images.gr-assets.com/books/1327935253s/47021.jpg    |         1 |
|      5671 |             3342764 |        3342764 |   3381062 |            48 | 316037885  | 9780316037880.0 | Trudi Canavan       |                        2009 | The Magician's Apprentice | The Magician's Apprentice (Black Magician, #0.5) | eng             |             3.94 |           17128 |                19089 |                       575 |         325 |        1049 |        4419 |        7005 |        6291 | https://images.gr-assets.com/books/1344264805m/3342764.jpg  | https://images.gr-assets.com/books/1344264805s/3342764.jpg  |         1 |
|      6897 |            26224667 |       26224667 |  46209108 |            11 |            |                 | Jana Aston          |                        2015 | Wrong                     | Wrong (Wrong, #1)                                | eng             |             3.94 |           14596 |                21374 |                      2184 |         641 |        1303 |        4316 |        7507 |        7607 | https://images.gr-assets.com/books/1443007627m/26224667.jpg | https://images.gr-assets.com/books/1443007627s/26224667.jpg |         0 |
|       623 |            18775247 |       18775247 |  26680281 |           111 | 1476754454 | 9781476754450.0 | Stephen King        |                        2014 | Mr. Mercedes              | Mr. Mercedes (Bill Hodges Trilogy, #1)           | eng             |             3.92 |          125847 |               148491 |                     12447 |        3242 |        7332 |       32479 |       60965 |       44473 | https://images.gr-assets.com/books/1468705326m/18775247.jpg | https://images.gr-assets.com/books/1468705326s/18775247.jpg |         0 |
|      2714 |             9462795 |        9462795 |  10862992 |            47 | 62011995   | 9780062011990.0 | Josephine Angelini  |                        2011 | Starcrossed               | Starcrossed (Starcrossed, #1)                    | en-US           |             4.08 |           49448 |                55202 |                      4837 |        1687 |        2999 |        9061 |       17058 |       24397 | https://images.gr-assets.com/books/1358266716m/9462795.jpg  | https://images.gr-assets.com/books/1358266716s/9462795.jpg  |         1 |



<!--### pca analysis
Error during pca analysis
-->


[]