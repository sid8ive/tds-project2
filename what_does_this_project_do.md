This script provides a comprehensive data analysis pipeline encapsulated within the DataAnalyzer class. Here's an outline of its capabilities and structure:

# Key Functionalities
- ### Data Loading:
  - Loads CSV files into pandas DataFrames with error handling.
- ### Data Cleaning:

  - Handles missing values using imputers (mean for numeric, most frequent for categorical).
  - Removes duplicates and performs advanced cleaning using IsolationForest and StandardScaler.
- ### Data Quality Report:

  - Provides insights into dataset composition, missing values, data types, and unique values.
- ### Statistical Analysis:

  - Computes descriptive statistics, skewness, and kurtosis for numeric columns.
- ### Advanced Visualizations:

  - Generates pair plots and saves them as images.
  - Creates word clouds from text data.
- ### Dimensionality Reduction:

  - Uses PCA to reduce numeric data to 2 dimensions and outputs explained variance.
- ### Clustering:

  - Implements KMeans clustering and optionally uses DBSCAN for adaptive clustering.
  - Visualizes cluster distributions using PCA-reduced dimensions.
- ### Trend Analysis:

  - Analyzes time-series trends using Holt-Winters Exponential Smoothing.
  - Assumes time-related columns based on naming conventions.
- ### Content Summary:

  - Uses OpenAI's GPT API to summarize data and extract insights.
- ### File Generation:

  - Produces a markdown summary (output.md) with embedded visualizations and analysis.
