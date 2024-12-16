# /// script
# requires-python = ">=3.12"
# dependencies = [
#   'requests',
#   'pandas',
#   'numpy',
#   'matplotlib',
#   'seaborn',
#   'chardet',
#   'wordcloud',
#   'scikit-learn',
#   'networkx',
#   'logging',
#   'tabulate',
#   'tenacity'
# ]
# ///

# Standard library imports
import argparse
import base64
import logging
import os
import sys
from datetime import datetime
from enum import Enum

# Third-party library imports
import chardet
import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import cm
import networkx as nx
import numpy as np
import pandas as pd
import requests
import seaborn as sns
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from tenacity import retry, stop_after_attempt, retry_if_exception_type
from wordcloud import WordCloud, STOPWORDS


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration Section
CONFIG = {
    "AIPROXY_URL": "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
    "AIPROXY_TOKEN": os.getenv("AIPROXY_TOKEN"),
    "LLM_MODEL": "gpt-4o-mini",
    "LLM_TOKENS_MAX" : 5000,
    "LLM_RETRY_MAX" :3,  # Max API call attempts (on retries)
    "LLM_FUNCTION_CALLS_MAX":7, #limit the number of function calls per run
    "LLM_ENABLE_AI_ANALYSIS":True, #Parameter to enable and disable general analysis by AI LLM bot
    "LLM_ENABLE_IMAGE_ANALYSIS":True, #Parameter to enable and disable image specific analysis by AI LLM bot. "LLM_ENABLE_AI_ANALYSIS" should also be true if we wish to enable this flag
    "OUTLIER_THRESHOLD" : 1.5,
    "Z_SCORE_THRESHOLD": 3,
    "TIME_SERIES_DATE_FORMATS": [
        '%Y-%m-%d', '%m/%d/%Y', '%Y', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S',
        '%m-%d-%Y %I:%M:%S %p', '%B %d, %Y', '%Y%m%d',
        '%Y-%m-%d %H:%M:%S.%f', '%Y%m%d%H%M%S', '%d %b %Y', '%d %B %Y',
        '%Y-%m', '%m-%Y', '%b-%Y', '%B, %Y', '%Y-%m-%dT%H:%M:%S.%fZ'],
    "PRIORITY_IMAGE_ANALYSIS":["Word Cloud", "Correlation Heatmap", "Outlier Detection Box Plot" ], #Added to tell priority analysis
    "MAX_DISTRIBUTION_PLOTS":3,
    "PLOT_WIDTH" : 10,
    "PLOT_HEIGHT" : 6,
}

if CONFIG["LLM_ENABLE_AI_ANALYSIS"]:
    # Check for missing AIPROXY_TOKEN
    if not CONFIG["AIPROXY_TOKEN"]:
        logging.error("AI analysis flag is enabled. But the environment variable 'AIPROXY_TOKEN' is missing or empty. Please set it to use AI features.")
    # Set the API header and key globally for the OpenAI library reference
    HEADERS = {"Authorization": f"Bearer {CONFIG['AIPROXY_TOKEN']}", "Content-Type": "application/json"}


# --- Helper Functions ---

def check_empty_dataframe(df, analysis_type):
  """Helper to check the dataframe and return default markdown output."""
  if df.empty:
      logging.warning(f"Dataframe is empty, skipping {analysis_type} analysis")
      return create_markdown_comment("No data available", analysis_type), True
  return None, False #returning False for success and None


def select_relevant_columns(df, analysis_type, excluded_keywords=None, sample_size=None, as_markdown=False, columns=None):
  """
  Selects relevant columns from a DataFrame based on analysis type and keywords.

  Args:
      df (pd.DataFrame): The input DataFrame.
      analysis_type (str): The type of analysis ('numeric' or 'object').
      excluded_keywords (list or str, optional): Keywords to exclude from column names.
          Can be a list of strings or a comma-separated string. Defaults to ['date', 'number', 'id', 'time', 'timestamp'].
      sample_size (int, optional): Number of sample rows to include in markdown output. Defaults to None.
      as_markdown (bool, optional): If True, returns a markdown formatted sample. Defaults to False.
      columns (list, optional): If provided, return only specific columns

  Returns:
      pd.DataFrame or str: Selected DataFrame or a markdown string of sample data.

  Example:
    df = pd.DataFrame({'col1': [1, 2, 3], 'date_col': ['2021-01-01', '2021-01-02','2021-01-03'], 'text': ['abc', 'def', 'ghi'], 'amount': [10.2,12.3,13.4]})

    # select numeric columns
    select_relevant_columns(df, 'numeric')

    # select object columns and remove date column
    select_relevant_columns(df, 'object', 'date') # can also pass excluded_keywords = ['date']

    # select top 2 rows from object column
    select_relevant_columns(df, 'object', sample_size=2, as_markdown=True)
  """
  if excluded_keywords is None:
      excluded_keywords = ['date', 'number', 'id', 'time', 'timestamp']
  if isinstance(excluded_keywords, str):
      excluded_keywords = [keyword.strip() for keyword in excluded_keywords.split(',')] #split by comma, remove whitespace

  if analysis_type == "numeric":
        selected_df = df.select_dtypes(include=[np.number])
  elif analysis_type == "object":
    if columns: # use list of columns if passed
        relevant_columns = [col for col in df.select_dtypes(include=['object']).columns if col in columns and not any(keyword in col.lower() for keyword in excluded_keywords)]
    else:
      relevant_columns = [col for col in df.select_dtypes(include=['object']).columns if not any(keyword in col.lower() for keyword in excluded_keywords)]
    selected_df = df[relevant_columns]
  else:
    return pd.DataFrame()  # Return empty dataframe

  if sample_size and as_markdown and len(selected_df) > 0:
      
    def format_cell(value):
          if isinstance(value, str) and value.startswith(('http://', 'https://')): #check if string starts with URL.
             return f'<img src="{value}" alt="Image" width="100" />' # HTML img tag for URL's
          else:
             return str(value) #convert other data types to string if required.
    formatted_df = selected_df.sample(min(sample_size, len(selected_df))).fillna('').applymap(format_cell)
    return f"Sample data:\n{formatted_df.to_markdown(index=False)}"
  elif as_markdown and len(selected_df) == 0:
      return "No relevant data to show"
  else:
      return selected_df

def create_markdown_comment(message, header=None, style="comment"):
   """Helper function to format comments in markdown"""
   if header:
       if style == "error":
           return f"\n<!--<span style=\"color:red\">### {header}\n{message}</span>-->\n"
       elif style == "warning":
           return f"\n<!--<span style=\"color:orange\">### {header}\n{message}</span>-->\n"
       else:
            return f"\n<!--### {header}\n{message}\n-->\n"
   else:
       if style == "error":
           return f"\n<!--<span style=\"color:red\">{message}</span>-->\n"
       elif style == "warning":
           return f"\n<!--<span style=\"color:orange\">{message}</span>-->\n"
       else:
            return f"\n<!--{message}-->\n"


def handle_analysis_error(func_name, e):
    """Handles analysis errors by logging and returning a markdown comment."""
    logging.error(f"Error during {func_name}: {e}")

    return f"\n<!--### {func_name}\nError during {func_name}\n-->\n" #Returning markdown comment

def report_relevant_columns(relevant_cols, text_str):
    """Generates markdown text for relevant columns in the dataset."""
    if relevant_cols and isinstance(relevant_cols, list):
        return f"{text_str}{', '.join(relevant_cols)}\n"
    return ""

def clean_data(df):
    """
    Cleans the dataframe columns and data

    Args:
        df (pd.DataFrame): The input DataFrame

    Returns:
        pd.DataFrame: The cleaned dataframe
    """
    # Clean column names
    df.columns = df.columns.str.strip().str.lower()
    logging.info(f"Column names changed to: {', '.join(df.columns)}")

    # Further cleaning logic for text or other data
    #Example
    for column in df.select_dtypes(include='object'):
       df[column] = df[column].str.strip()  #remove whitespace from text

    logging.info(f"Removed white spaces from string columns: {', '.join(df.select_dtypes(include='object').columns)}")

    return df

# encoding the image to base64. Used by ai_bot_helper function
def encode_image(img_path):
    """Encode an image to a base64 string."""
    with open(img_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def log_model_cost_info(response_json):
    """
    Extracts and logs specific cost and model related information from the API response.
    Args:
        response_json: The JSON response received from the AI proxy API
    """

    if "model" in response_json:
        logging.info(f"model: {response_json['model']}")
    if "usage" in response_json:
        usage = response_json['usage']
        logging.info(f"usage: {usage}")
    if 'monthlyCost' in response_json:
        logging.info(f"monthlyCost: {response_json['monthlyCost']}")
    if 'cost' in response_json:
        logging.info(f"cost: {response_json['cost']}")
    if 'monthlyRequests' in response_json:
        logging.info(f"monthlyRequests: {response_json['monthlyRequests']}")

def generate_chart(plt, file_name, df, output_dir, saved_files):
    logging.info(f"Generating chart: {file_name}")
    try:
        if file_name:
            # Replace spaces with underscores in file_name
            file_name = file_name.replace(" ", "_")
            if not file_name.strip():  # Check if file_name is empty or contains only spaces
                logging.warning(f"Warning: file_name is empty after processing.")
                return None
            full_path = os.path.join(output_dir, file_name)

            plt.subplots_adjust(left=0.1, right=0.9, bottom=0.2, top=0.9)  # Adjust margins
            plt.savefig(full_path, bbox_inches='tight', dpi=100)
            plt.close() # close to release the resource
            logging.info(f"Chart saved at: {full_path}")

            # Add to saved files
            saved_files.add(full_path)
            return full_path
        else:
            logging.warning(f"Warning: file_name not passed.")
            return None
    except Exception as e:
        logging.error(f"Error generating the chart {file_name}: {e}")
        return None


def create_plot_with_title(df, plot_func, title, output_dir, saved_files, file_name=None, *args, **kwargs):
    """
     Create a plot, set title, and handle save operation.
    """
    ai_insights = ""
    try:
        plt.figure(figsize=(CONFIG["PLOT_WIDTH"], CONFIG["PLOT_HEIGHT"]))  # Setting plot size from the config
        plot_func(df, *args, **kwargs)  # Call the plot function, passing any arguments provided
        plt.title(title)  # Set the title
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels (45 deg) and align right
        if file_name is None:
             file_name = f"{title.lower().replace(' ', '_')}.png"

        fPath = generate_chart(plt, file_name, df, output_dir, saved_files)
        if not fPath:
            logging.warning(f"No image was generated for the title {title}")
            return "", ai_insights  # if no image was generated, return empty string

        analysis_str = f"![{title}]({os.path.basename(fPath)})\n\n"

        if CONFIG.get("LLM_ENABLE_IMAGE_ANALYSIS", False) and (title in CONFIG.get("PRIORITY_IMAGE_ANALYSIS", [])):
            ai_insights = call_ai_for_image_analysis(df, title, fPath, analysis_content=analysis_str, kwargs=kwargs)  # Added to avoid duplicated logic
        return analysis_str, ai_insights  # returned markdown for image
    except Exception as e:
        return handle_analysis_error(f"generating chart {title}", e), ai_insights
    
# helper functions for analysis. These functions only do the processing, no plotting etc.
def calculate_word_frequencies(df, column_name=None):
      """Calculates word frequencies from text data in a DataFrame."""
      text_df = select_relevant_columns(df, "object")
      if not text_df.shape[1]:
          logging.warning("No text data found for wordcloud analysis.")
          return None #returning markdown comment

      if column_name:
          if column_name not in df.columns:
              logging.error(f"Error: column {column_name} not found for wordcloud analysis")
              return None
          text_data = df[column_name].dropna().apply(lambda x: str(x)) # drop NaN values, string type
      else:
          text_data = text_df.apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1).dropna()

      all_words = []
      for item in text_data:
          words = item.lower().split()  # Split into words
          all_words.extend([word for word in words if len(word) >= 4 and not word.startswith(('http://', 'https://')) and word.isalpha()])
      all_text = " ".join(all_words)
      if not all_text:
          logging.warning("No relevant words found for wordcloud analysis")
          return None

      stopwords = set(STOPWORDS) # Using built in stopwords
      wordcloud = WordCloud(width=400, height=200, background_color="white", max_words=500, collocations=False, stopwords=stopwords).generate(all_text) #generate wordcloud
      return wordcloud

def calculate_correlation_matrix(df):
    """Calculates the correlation matrix for numeric columns."""
    numeric_df = select_relevant_columns(df, "numeric")
    if numeric_df.empty:
         logging.warning("No numeric columns found for correlation analysis.")
         return None
    correlation = numeric_df.corr()
    return correlation

def calculate_outlier_summary(df):
    """Calculate IQR bounds for outlier detection."""
    numeric_df = select_relevant_columns(df, "numeric")
    outliers_summary = {}
    def calculate_iqr_bounds(series):
        """Calculate IQR bounds for outlier detection."""
        iqr = series.quantile(0.75) - series.quantile(0.25)
        
        # Handle edge case: when IQR is zero
        if iqr == 0:
            lower_bound = series.min() - 1.5 * 1
            upper_bound = series.max() + 1.5 * 1 #consider 1 as default value in this case
        else:
            lower_bound = series.quantile(0.25) - 1.5 * iqr
            upper_bound = series.quantile(0.75) + 1.5 * iqr

        return lower_bound, upper_bound
    for col in numeric_df.columns:
        lower, upper = calculate_iqr_bounds(df[col])
        outliers_summary[col] = {
            "lower_bound": lower,
            "upper_bound": upper,
            "outliers_count": df[(df[col] < lower) | (df[col] > upper)].shape[0],
        }
    return outliers_summary

def calculate_clustering_data(df, n_clusters):
    """Performs clustering on numerical data."""
    numeric_df = select_relevant_columns(df, "numeric")
    if numeric_df.empty:
            logging.warning("No numeric columns found for clustering analysis.")
            return None, None

     # Scaling and imputing
    scaler = StandardScaler()
    imputer = SimpleImputer(strategy="mean")
    df_scaled = scaler.fit_transform(imputer.fit_transform(numeric_df))
    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(df_scaled)

    return df, df_scaled

def calculate_pca(df, n_components):
    """Performs PCA for dimensionality reduction."""
    numeric_df = select_relevant_columns(df, "numeric")
    if numeric_df.empty:
        logging.warning("No numeric columns found for PCA analysis.")
        return None, None
        # Scaling and PCA
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(numeric_df)
    pca = PCA(n_components=min(n_components, numeric_df.shape[1]))
    pca_components = pca.fit_transform(df_scaled)

    # Add PCA components to the DataFrame
    df["PCA1"], df["PCA2"] = pca_components[:, 0], pca_components[:, 1]
    return df, pca_components

# Helper function to generate plots
def plot_word_cloud(wordcloud, title, output_dir, saved_files, df):
   plt.figure(figsize=(7, 4))
   plt.imshow(wordcloud, interpolation="bilinear")
   plt.axis('off')  # No axes for word cloud
   plt.title(title)
   fName = f"word_cloud.png"
   fPath = generate_chart(plt, fName, df, output_dir, saved_files)
   return fPath

def plot_correlation_heatmap(correlation, title, output_dir, saved_files):
   def _plot_corr_heatmap(data): # creating inner function
       sns.heatmap(data, annot=True, cmap='viridis', fmt=".2f", linewidths=0.5)
   return create_plot_with_title(df=correlation, plot_func=_plot_corr_heatmap, title = title, output_dir = output_dir, saved_files=saved_files)


def create_outlier_boxplot(df, title, output_dir, saved_files):
    """Plot box plot for outliers and return path"""
    def _plot_box_plot(data): # create a inner helper function
        sns.boxplot(data=data, palette="viridis")
    return create_plot_with_title(
          df=df,
          plot_func=_plot_box_plot,
          title=title,
          output_dir=output_dir,
          saved_files=saved_files,
      )

def convert_to_datetime(df, date_column):
      """Convert the provided date column to datetime.

        Args:
           df (pd.DataFrame): The input DataFrame.
            date_column (str): name of the date column
        Returns:
           pd.DataFrame:  with converted date column
         """
      logging.info(f"Trying to convert '{date_column}' to time series data type")
      try:
          df_copy = df.copy()
          # if the column is numeric, it is assumed that is a year column.
          if df[date_column].dtype == np.dtype('int64') or df[date_column].dtype == np.dtype('float64'):
              df_copy[date_column] = pd.to_datetime(df_copy[date_column].apply(lambda x: f"{int(x)}-01-01"), errors='raise')
              logging.info(f"Column '{date_column}' was converted using numeric values")
              return df_copy #return df after converting date column

          df_copy[date_column] = pd.to_datetime(df_copy[date_column], errors='raise', infer_datetime_format=True)
          logging.info(f"Column '{date_column}' was converted using infer datetime format.")
          return df_copy

      except ValueError:
          logging.warning(f"Column '{date_column}' does not have a valid date format. Trying configured formats")
          converted = False
          for format in CONFIG["TIME_SERIES_DATE_FORMATS"]:
               try:
                 df_copy = df.copy()
                 df_copy[date_column] = pd.to_datetime(df_copy[date_column], errors='raise', format=format)  # Try format
                 converted = True
                 logging.info(f"Column '{date_column}' converted using format: '{format}'")
                 return df_copy #return df after converting date column
               except ValueError:
                  continue
          if not converted:
            logging.warning(f"Column '{date_column}' does not have a valid date format for time series analysis using configured formats.")
          return None
      except Exception as e:
          logging.warning(f"An unexpected error occurred during date conversion : {e}, skipping")
          return None

def plot_time_series(df, output_dir, saved_files):
        """
           Generates time series plot if a suitable date/year field is available.
        """
        logging.info("Starting time series analysis...")
        ai_insights = ""
        try:
           date_column = next((col for col in df.columns if any(keyword in col.lower() for keyword in ['date', 'year'])), None)
           if date_column:
              logging.info(f"Found column '{date_column}' using keywords 'date' or 'year' for time series analysis.")
           else:
                logging.warning("No 'date' or 'year' column found. Trying to find other suitable columns")
                for col in df.columns:
                     df_copy = convert_to_datetime(df, col)
                     if df_copy is not None:
                        date_column=col
                        df = df_copy #reset the df if the column is converted successfully
                        logging.info(f"Using column '{col}' for time series analysis")
                        break
                     else:
                        continue
           if not date_column:
               logging.warning(f"No suitable date/year column found for time series analysis.")
               return f"\n<!--### Time Series Analysis\nNo time series analysis found\n-->\n", ai_insights

          # Set the date column as index
           df = df.set_index(date_column)
           numeric_cols = df.select_dtypes(include=np.number).columns
           if not len(numeric_cols):
               logging.warning("No numeric column found to plot time series analysis")
               return f"\n<!--### Time Series Analysis\nNo time series analysis found\n-->\n", ai_insights # returning markdown comment
          # Use common function to generate plot and save
           analysis_str, ai_insights = plot_time_series_graph(df, "Time Series Analysis", output_dir, saved_files,
                                                        numeric_cols=numeric_cols)
           if analysis_str:
                analysis_str = f"{analysis_str}\nThis line plot shows trends over time for numerical data with a `Date` column.\n"
           else:
                analysis_str = f"\n<!--### Time Series Analysis\nNo time series analysis found\n-->\n", ai_insights
                logging.info("Time series analysis chart saved.")
           return analysis_str, ai_insights
        except Exception as e:
            return handle_analysis_error("time series analysis", e), ai_insights

def plot_geographic_analysis(df, output_dir, saved_files):
    """
    Generates geographic plots if `Latitude` and `Longitude` columns are present.

    Args:
        df (pd.DataFrame): The input DataFrame.
        output_dir (str): Directory to save the plot.
        saved_files (set): Set to track saved files.

    Returns:
        tuple: A string containing analysis markdown and AI insights.
    """
    logging.info("Starting geographic analysis...")
    ai_insights = ""

    try:
        # Identify Latitude and Longitude columns
        latitude_column = next((col for col in df.columns if 'latitude' in col.lower()), None)
        longitude_column = next((col for col in df.columns if 'longitude' in col.lower()), None)

        if not latitude_column or not longitude_column:
            logging.warning("No 'Latitude' or 'Longitude' columns found for geographic analysis.")
            return f"\n<!--### Geographic Distribution\nNo geographic data found\n-->\n", ai_insights

        # Generate the scatter plot
        analysis_str, ai_insights = create_plot_with_title(
            df=df,
            plot_func=sns.scatterplot,
            title="Geographic Distribution of Data",
            output_dir=output_dir,
            saved_files=saved_files,
            x=longitude_column,
            y=latitude_column,
            data=df
        )

        if analysis_str:
            analysis_str += (
                "\nThis scatter plot maps data points based on their geographic coordinates "
                f"(`Latitude`: `{latitude_column}` and `Longitude`: `{longitude_column}`).\n"
            )
            # Add a sample of 5 rows for additional context
            sample_data = df[[latitude_column, longitude_column]].sample(
                min(5, len(df))
            ).fillna("").to_markdown(index=False)
            analysis_str += f"\nSample rows from the dataset:\n\n{sample_data}\n"

        logging.info("Geographic distribution chart saved successfully.")
        return analysis_str, ai_insights

    except Exception as e:
        logging.error(f"Error during geographic analysis: {e}")
        return handle_analysis_error("geographic analysis", e), ai_insights

def plot_network_analysis(df, output_dir, saved_files):
    """
    Performs network analysis if the required columns are present
    """
    logging.info("Starting network analysis...")

    ai_insights = ""
    try:
        # Assuming your DataFrame has 'source' and 'destination' columns
        if 'source' not in df.columns or 'destination' not in df.columns:
            logging.warning("No 'source' or 'destination' columns found for network analysis")
            return  f"\n<!--### Network Analysis\nNo network analysis generated\n-->\n", ai_insights #returning markdown comment
        # Create graph
        G = nx.from_pandas_edgelist(df, source='source', target='destination',create_using=nx.DiGraph())

         # Calculate network metrics
        degrees = dict(G.degree())
        centrality = nx.degree_centrality(G)
        # Visualization and save
        analysis_str, ai_insights = plot_network_chart(df, G,degrees, "Network Analysis", output_dir, saved_files, layout="circular")

        if analysis_str:
            analysis_str = "\n### Network Analysis\n"
            analysis_str += f"**This plot shows the network of cities and network between them.**\n\n"
            analysis_str += f"**Network Information:**\n- **Nodes:** {list(G.nodes())}\n- **Edges:** {list(G.edges())}\n"
            analysis_str += f"- **Node Degrees:** {degrees}\n- **Centralities:** {centrality}\n\n"
            
             # Add sample of 5 rows from data
            sample_data = f"\nSample 5 rows from provided data, for context to Network Analysis \n{df.sample(min(5, len(df))).fillna('').to_markdown(index=False)}"

            analysis_str+=sample_data
        else:
            analysis_str= f"\n<!--### Network Analysis\nNo network analysis generated\n-->\n", ai_insights #returning markdown comment
        logging.info("Network analysis chart saved.")
        return analysis_str, ai_insights

    except Exception as e:
        # Handle exceptions and log error details
        logging.error(f"Error during network analysis: {e}")
        return handle_analysis_error("network analysis", e), ai_insights


def plot_categorical_data(df, output_dir, saved_files):
    """
    Generates bar plots for each categorical column
    """
    logging.info("Starting Categorical data analysis")
    ai_insights = ""
    try:

        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) == 0:
            logging.warning("No categorical column found.")
            return f"\n<!--### Categorical Data Distribution\nNo categorical columns to analyze\n-->\n", ai_insights #returning markdown comment
        logging.info(f"Categorical Data distribution: max {CONFIG['MAX_DISTRIBUTION_PLOTS']} plots will be generated.")

        analysis_str = "\n### Categorical Data Distribution\nThe following plots show the distribution of categorical data:\n\n"

        top_n = 10  # Number of top categories to plot

        plot_count=0
        for col in categorical_cols:
            if plot_count >= CONFIG['MAX_DISTRIBUTION_PLOTS']:
                logging.info("Categorical plot creation count limit reached, skipping to next plot")
                break
            plot_count+=1
            # Limit to the top N categories by frequency
            value_counts = df[col].value_counts().nlargest(top_n)

            # If there are more categories, group them into 'Other'
            if len(value_counts) < len(df[col].unique()):
                other_count = df[col].value_counts().iloc[top_n:].sum()
                # Create a new series for "Other" category
                other_series = pd.Series({'Other': other_count})
                # Concatenate the 'Other' category with the top categories
                value_counts = pd.concat([value_counts, other_series])

            # Use common function to generate plot and save
            plot_str, insight = plot_categorical_chart(df,value_counts, f"Distribution of {col}", output_dir, saved_files)
            analysis_str += plot_str
            if insight:
                ai_insights.append(insight)
            if analysis_str:
                analysis_str += f"\nThis bar chart shows the distribution of `{col}` column.\n"
                # Add sample of 5 rows from data
                sample_data = f"\nSample 5 rows from provided data, for context to Categorical distribution \n{df[[col]].sample(min(5, len(df))).fillna('').to_markdown(index=False)}\n"
                analysis_str+=sample_data
            logging.info(f"Categorical distribution chart for {col} saved")
        return analysis_str, ai_insights

    except Exception as e:
        return handle_analysis_error("categorical plot analysis", e), ai_insights


def plot_histograms(df, output_dir, saved_files):
      """
       Generates histogram plots for each numerical column
      """
      logging.info("Starting Histograms data analysis")
      ai_insights = ""
      try:
          numeric_df = select_relevant_columns(df, "numeric")
          if numeric_df.empty:
              logging.warning("No numeric column found.")
              return f"\n<!--### Numerical Data Histograms\nNo Numerical column found\n-->\n", ai_insights #returning markdown comment
          logging.info(f"Histogram Distribution: max {CONFIG['MAX_DISTRIBUTION_PLOTS']} plots will be generated.")
          analysis_str = "\n\n### Numerical Data Histograms\n\n" #Added new lines after the header
          plot_count=0

          numeric_cols = numeric_df.columns.tolist() # fix: get numeric column here
          for col in numeric_cols:
              if plot_count >= CONFIG['MAX_DISTRIBUTION_PLOTS']:
                  logging.info("Histogram plot limit reached, skipping next plot")
                  break
              plot_count+=1
              # Use common function to generate plot and save
              plot_str, insight =  plot_histogram_chart(df, col, f"Distribution of {col}", output_dir, saved_files)
              analysis_str += f"This histogram plot represents the distribution of `{col}` column.\n\n{plot_str}" #Added newlines here
              if insight:
                ai_insights.append(insight)
            
              logging.info(f"Histogram distribution chart for {col} saved")
          return analysis_str, ai_insights

      except Exception as e:
           return handle_analysis_error("histogram analysis", e), ai_insights

def perform_pca(df, output_dir, saved_files, n_components=2):
    """
    Performs PCA for dimensionality reduction and visualizes the results.
    """
    logging.info("Starting PCA analysis...")

    df, pca_components = calculate_pca(df, n_components)

    if df is None or pca_components is None:
        return f"\n<!--### PCA Analysis\nNo numeric columns found for PCA analysis\n-->\n", None
    analysis_str, ai_insights = plot_pca_chart(df, pca_components, "Principal Component Analysis", output_dir, saved_files)


    if analysis_str:
        analysis_str += "\nThis scatter plot shows the PCA results.\n"

    logging.info("PCA analysis completed successfully.")
    return analysis_str, ai_insights



# --- Plotting Functions ---

def plot_time_series_graph(df, title, output_dir, saved_files, numeric_cols):
    """Plot time series graph."""
    def _plot_time_series(df, numeric_cols):
        df[numeric_cols].plot(use_index=True, alpha=0.7)
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xticks(rotation=45)
    return create_plot_with_title(df, lambda df: _plot_time_series(df, numeric_cols), title, output_dir, saved_files)


def plot_network_chart(df, G, degrees, title, output_dir, saved_files, layout="spring"):
    """Helper function to plot a network graph."""
    def _plot_network_chart(G, degrees, layout):
        # Choose layout dynamically
        if layout == "spring":
            pos = nx.spring_layout(G)
        elif layout == "circular":
            pos = nx.circular_layout(G)
        elif layout == "kamada_kawai":
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.random_layout(G)

        # Normalize degrees for color mapping
        norm = mcolors.Normalize(vmin=min(degrees.values()), vmax=max(degrees.values()))
        cmap = cm.get_cmap('coolwarm')  # Use a color map for node coloring
        node_colors = [cmap(norm(deg)) for deg in degrees.values()]

        # Draw the graph
        nx.draw(
            G, pos, with_labels=True, node_size=500, font_size=10,
            node_color=node_colors, edge_color="gray", linewidths=1.0, alpha=0.8
        )

    return create_plot_with_title(df, lambda df: _plot_network_chart(G, degrees, layout), title, output_dir, saved_files)




def plot_categorical_chart(df, value_counts, title, output_dir, saved_files):
    """Helper function to plot categorical data."""
    def _plot_categorical_chart(value_counts):
        value_counts.plot(kind='barh', color='skyblue')
    return create_plot_with_title(df, lambda df: _plot_categorical_chart(value_counts), title, output_dir, saved_files)



def plot_histogram_chart(df, col, title, output_dir, saved_files):
    """Helper function to plot histogram data."""
    def _plot_histogram_chart(df, col):
        df[col].hist()
        plt.xticks(rotation=45, ha='right')
    return create_plot_with_title(df, lambda df: _plot_histogram_chart(df, col), title, output_dir, saved_files)



def plot_cluster_chart(df, df_scaled, title, output_dir, saved_files):
    """Helper function to plot clusters."""
    def _plot_cluster_chart(df_scaled):
        plt.scatter(df_scaled[:, 0], df_scaled[:, 1], c=df['Cluster'], cmap='viridis')
    return create_plot_with_title(df, lambda df: _plot_cluster_chart(df_scaled), title, output_dir, saved_files)



def plot_pca_chart(df, pca_components, title, output_dir, saved_files):
    """Helper function to plot PCA data."""
    def _plot_pca_chart(pca_components):
        plt.scatter(pca_components[:, 0], pca_components[:, 1], alpha=0.7, edgecolors='w', s=80)
        plt.xlabel("Principal Component 1", fontsize=12)
        plt.ylabel("Principal Component 2", fontsize=12)
        plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
        plt.tight_layout()
    return create_plot_with_title(df, lambda df: _plot_pca_chart(pca_components), title, output_dir, saved_files)

def read_csv_with_multiple_encodings(file_path):
    """
    Reads a CSV file, attempting to detect encoding automatically.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
         pd.DataFrame: The DataFrame if successful.

    Raises:
        Exception: If there is an error during file reading.
    """
    try:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        enc = result['encoding']
        logging.info(f"Detected file encoding: {enc}")

        try:
            df = pd.read_csv(file_path, encoding=enc)
            return df  # Return the dataframe if successful
        except UnicodeDecodeError as e:
            # If the encoding fails, log the error and re-raise
            logging.error(f"Failed to read file with encoding '{enc}': {e}")
            raise #re-raise the exception for caller to handle
    except Exception as e:
        logging.error(f"An error occurred while reading the file: {e}")
        raise

def do_basic_analysis(df, csv_file):
    """Performs basic analysis of the dataframe

    Args:
        df (pd.DataFrame): Input dataframe
        csv_file (str): Input CSV file path

    Returns:
        str: analysis output as string
    """
    # Summary Statistics (for both numeric and categorical columns)
    numeric_df = df.select_dtypes(include=[np.number])
    details_summary = numeric_df.describe().map(lambda x: f"{x:.2f}" if isinstance(x, float) else (x if pd.notna(x) else ''))

    # Add sample of 5 rows from data
    sample_data = select_relevant_columns(df, "object", sample_size =5, as_markdown=True)

    # Missing Values Count
    missing_values = df.isna().sum()

    # Percentage of Missing Values for each column
    missing_percentage = (df.isna().mean() * 100)

    # Displaying the missing values as percentage
    missing_info = pd.DataFrame({
        'Missing Values Count': missing_values,
        'Missing Percentage (%)': missing_percentage
    })

    analysis_str = "# Summary of findings\n\n"
    analysis_str += "## Overview\n"
    analysis_str += f"File name: {os.path.basename(csv_file)}\n\n"
    analysis_str += f"The file has {len(df)} rows and {len(df.columns)} columns\n\n"

    analysis_str +="### Sample 5 rows from file, for context\n\n"
    analysis_str += sample_data + "\n\n"

    # Write details summary as Markdown table
    analysis_str += "### Descriptive analysis of the data\n\n"

    details_summary = details_summary.dropna(axis=0, how='all') #remove all nan rows

    details_summary_str = details_summary.to_markdown()  # Converts the DataFrame to Markdown format, remove nan rows.
    analysis_str += details_summary_str + "\n\n"

    # Write missing values report as Markdown table
    analysis_str += "## Missing values report\n\n"
    missing_info_str = missing_info.to_markdown()  # Converts the DataFrame to Markdown format
    analysis_str += missing_info_str + "\n\n"
    logging.info("Generated basic summary statistics and checked for missing values")

    return analysis_str

def perform_analysis(analysis_type, df, output_dir, saved_files, *args, **kwargs):
         """General function to handle the analysis logic
         Args:
             analysis_type (str): analysis type to be called
             df (pd.DataFrame): input dataframe
             output_dir (str): output directory
             saved_files (set): used to track saved files
         Returns:
             analysis_str (str): analysis string generated
             ai_insights (list) : list of insights generated by AI LLM bot
         """
         logging.info(f"Starting {analysis_type} analysis")
         ai_insights = []
         analysis_str = ""
         try:
          empty_check_str, isEmpty = check_empty_dataframe(df, analysis_type)
          if isEmpty:
            return empty_check_str, ai_insights
          if analysis_type == "word_cloud":
              wordcloud = calculate_word_frequencies(df, kwargs.get('column_name'))
              if not wordcloud:
                  return create_markdown_comment("No text data found for word cloud analysis", analysis_type), ai_insights
              fPath = plot_word_cloud(wordcloud, "Word Cloud", output_dir, saved_files, df)
              if not fPath:
                  return create_markdown_comment("No Word Cloud created", analysis_type), ai_insights
              analysis_str = f"\n### Word Cloud Analysis\n![Word Cloud]({os.path.basename(fPath)})\n\n"
              top_words = list(wordcloud.words_.keys())[:20]
              analysis_str += f"\nSome of these most frequently words are: {', '.join(top_words)}.\n"
              ai_insight = call_ai_for_image_analysis(df, "Word Cloud", fPath, analysis_content=analysis_str, sample_size=3, column_name=kwargs.get('column_name'))
              if ai_insight:
                analysis_str += f"\n{ai_insight}\n"
              analysis_str += "\n\n" #added for formatting
              

          elif analysis_type == "correlation":
             correlation = calculate_correlation_matrix(df)
             if correlation is None:
                  return create_markdown_comment("No numeric columns for correlation analysis", analysis_type), ai_insights
             analysis_str, ai_insight = plot_correlation_heatmap(correlation, "Correlation Heatmap", output_dir, saved_files)
             if ai_insight:
                 analysis_str += f"\n{ai_insight}\n"
             if analysis_str:
                 analysis_str += "\nThis heatmap visualizes the correlation between numerical features.\n"
             analysis_str += "\n\n" #added for formatting


          elif analysis_type == "outlier":
              numeric_df = select_relevant_columns(df, 'numeric')
              if numeric_df.empty:
                  logging.warning("No numeric columns found for outlier analysis.")
                  return create_markdown_comment("No numeric columns for outlier analysis", analysis_type), ai_insights
              outliers_summary = calculate_outlier_summary(df)
              analysis_str, ai_insight = create_outlier_boxplot(df, "Outlier Detection Box Plot", output_dir, saved_files)
              if ai_insight:
                 analysis_str += f"\n{ai_insight}\n"
              if analysis_str:
                  analysis_str += "\nThis boxplot highlights potential outliers for numerical features.\n"
                  outlier_summary_md = pd.DataFrame(outliers_summary).to_markdown()
                  analysis_str += f"\n### Outlier Summary:\n\n{outlier_summary_md}\n"
              analysis_str += "\n\n" #added for formatting
          elif analysis_type == "clustering":
                 df, df_scaled = calculate_clustering_data(df, kwargs.get('n_clusters',3))
                 if df is None or df_scaled is None:
                     return create_markdown_comment("No numeric columns found for clustering analysis", analysis_type), ai_insights
                 analysis_str, ai_insight = plot_cluster_chart(df, df_scaled, "Cluster Analysis", output_dir, saved_files)
                 if ai_insight:
                     analysis_str += f"\n{ai_insight}\n"
                 if analysis_str:
                     analysis_str += "\nThis scatter plot represents the cluster analysis results.\n"
                     sample_data = df.sample(min(5, len(df))).fillna("").to_markdown(index=False)
                     analysis_str += f"\nSample data with clusters:\n\n{sample_data}\n"
                 analysis_str += "\n\n" #added for formatting
          elif analysis_type == "time_series":
              analysis_str, ai_insight = plot_time_series(df, output_dir, saved_files)
              if ai_insight:
                  analysis_str += f"\n{ai_insight}\n"
              if analysis_str:
                 analysis_str = f"### Time Series Analysis\n{analysis_str}\n"
                 
              analysis_str += "\n\n" #added for formatting

          elif analysis_type == "geographic":
             analysis_str, ai_insight = plot_geographic_analysis(df, output_dir, saved_files)
             if ai_insight:
                analysis_str += f"\n{ai_insight}\n"
             analysis_str += "\n\n" #added for formatting
          elif analysis_type == "network":
                analysis_str, ai_insight = plot_network_analysis(df, output_dir, saved_files)
                if ai_insight:
                   analysis_str += f"\n{ai_insight}\n"
                analysis_str += "\n\n" #added for formatting
          elif analysis_type == "categorical":
                analysis_str, ai_insight = plot_categorical_data(df, output_dir, saved_files)
                if ai_insight:
                    analysis_str += f"\n{ai_insight}\n"
                analysis_str += "\n\n" #added for formatting
          elif analysis_type == "histogram":
                analysis_str, ai_insight = plot_histograms(df, output_dir, saved_files)
                if ai_insight:
                    analysis_str += f"\n{ai_insight}\n"
                analysis_str += "\n\n" #added for formatting
          elif analysis_type == "pca":
                 analysis_str, ai_insight = perform_pca(df, output_dir, saved_files)
                 if ai_insight:
                     analysis_str += f"\n{ai_insight}\n"
                 analysis_str += "\n\n" #added for formatting
          else:
              return  create_markdown_comment(f"Analysis type '{analysis_type}' not supported", f"{analysis_type} Analysis"), ai_insights
          return analysis_str, ai_insights

         except Exception as e:
             return handle_analysis_error(f"{analysis_type} analysis", e), ai_insights
         

def analyze_csv_data(csv_file):
    """
    Reads, cleans, analyzes, and returns analysis content.
     """
    logging.info(f"Starting analysis for file: {csv_file}")
    try:
        df = read_csv_with_multiple_encodings(csv_file)
        logging.info(f"Successfully loaded the csv file")
    except Exception as e:
        logging.error(f"Error reading csv file: {e}")
        return None, None, None, None # return None, so that the main function can handle it and log the errors

    # Use the same directory as of the input CSV file
    output_dir = os.path.dirname(csv_file)

    # save all analysis in file
    analyses_file_path = os.path.join(output_dir, f"data_analysis.md")
    logging.info(f"Output directory set to: {output_dir}")

    # Following variable to track successfully created files. This is to ensure that final document has only generated file and no empty paths
    saved_files = set()
    try:
        # Data Cleaning
        df = clean_data(df)

        analysis_content = ""
        ai_insights = [] #Initialize, we will get the insights from main
        analysis_content += do_basic_analysis(df, csv_file)

        # Perform analyses using the new perform_analysis function
        analysis_str, insights = perform_analysis("word_cloud", df, output_dir, saved_files)
        analysis_content += analysis_str
        if insights:
            ai_insights.extend(insights)

        analysis_str, insights = perform_analysis("correlation", df, output_dir, saved_files)
        analysis_content += analysis_str
        if insights:
            ai_insights.extend(insights)

        analysis_str, insights = perform_analysis("outlier", df, output_dir, saved_files)
        analysis_content += analysis_str
        if insights:
            ai_insights.extend(insights)

        analysis_str, insights = perform_analysis("time_series", df, output_dir, saved_files)
        analysis_content += analysis_str
        if insights:
            ai_insights.extend(insights)

        analysis_str, insights = perform_analysis("geographic", df, output_dir, saved_files)
        analysis_content += analysis_str
        if insights:
            ai_insights.extend(insights)

        analysis_str, insights = perform_analysis("network", df, output_dir, saved_files)
        analysis_content += analysis_str
        if insights:
            ai_insights.extend(insights)

        analysis_str, insights = perform_analysis("categorical", df, output_dir, saved_files)
        analysis_content += analysis_str
        if insights:
             ai_insights.extend(insights)

        analysis_str, insights = perform_analysis("histogram", df, output_dir, saved_files)
        analysis_content += analysis_str
        if insights:
            ai_insights.extend(insights)
        
        analysis_str, insights = perform_analysis("clustering", df, output_dir, saved_files, n_clusters = 3)
        analysis_content += analysis_str
        if insights:
            ai_insights.extend(insights)
        
        analysis_str, insights = perform_analysis("pca", df, output_dir, saved_files)
        analysis_content += analysis_str
        if insights:
            ai_insights.extend(insights)

        # Write analysis to file
        with open(analyses_file_path, "w") as analyses_file:
            analyses_file.write(analysis_content)
        logging.info(f"All static analysis written to {analyses_file_path} file")
        return analysis_content, analyses_file_path, saved_files, ai_insights

    except IOError as e:
        logging.error(f"An IO error occurred during the analysis process: {e}")
        return None, None, None, None
    except Exception as e:
         logging.error(f"Error during the analysis process: {e}")
         return None, None, None, None
    
def tell_me_a_story(analyses, analyses_path, saved_files, ai_insights):
    """
    Narrates a story based on the analysis.
     """
    readme_path = os.path.join(analyses_path, "README.md")
    try:
        with open(readme_path, "w") as readme_file:
            story_context = f"Statistical data in markup:\n{analyses}"
            #story_context += f"\n\nAI generated insights:\n {ai_insights}" if ai_insights else "" # Removed AI insights from here

            readme_file.write("*Every story is complicated until it finds the right storyteller — Anonymous*\n\n\n")
           # readme_file.write(f"{story_context}\n\n{ai_insights}")  # do not write it now. will add it later
            
            try:
                story = ai_bot_helper(
                    "Generate a creative, yet data-driven and professional story based on the provided content and graphs. The narrative should focus on four key aspects:" +
                    " 1) clearly describe the data you received, to a non-technical audience," +
                    " 2) the analysis carried out by you, explaining the methodologies," +
                    " 3) insights and anomalies identified by you, explaining them clearly and" +
                    " 4) the implications of your findings." +
                    " Include relevant images from the provided content, using the image descriptions and your analysis to make the story engaging and provide insights on the images. Also mention any data limitations or biases. Use external hyperlinks and references to strengthen the storyline.",
                    story_context, #Use the full context with ai_insights
                     )
                if story:
                    if not isinstance(story, str):
                        logging.error("AI bot did not return markdown output, but proceeding with static markdown")
                        readme_file.write(f"{story_context}\n\n{ai_insights}")
                        return readme_path
                    readme_file.write(f"{story}\n")
                    logging.info("Added story to README.md file")
                    return readme_path
                else:
                    logging.error(f"Unable to generate a story by AI Bot. Static content with all available insights will be used")
                    readme_file.write(f"{story_context}\n\n{ai_insights}")
                    logging.info("Added story to README.md file, using static content since AI bot returned None")
                    return readme_path
            except Exception as e:
                logging.error(f"Error during AI bot call in tell_me_a_story function: {e}, will use static analysis.")
                #fall back to static content
                readme_file.write(f"{story_context}\n\n{ai_insights}")
                logging.info("Added story to README.md file, using static content due to AI bot failure")
                return readme_path
    except FileNotFoundError as e:
        logging.error(f"Error opening the analysis file {analyses_path}: {e}")
        return None
    except Exception as e:
        logging.error(f"Error opening or writing to the file {readme_path}: {e}")
        return None
    
def perform_story_time(args):
    """
    Performs basic story time analysis for the arguments passed by AI bot

    Args:
        args (str): arguments of the function from AI bot

    Returns:
        str: analysis output as string
    """
    try:
        logging.info(f"Received arguments from AI bot: {args}")

        # Check if 'args' is a string and load as JSON
        if isinstance(args, str):
            args = json.loads(args)

        insights = args.get("insights", "")  # Get the insights parameter from function argument
        vision_analysis = args.get("vision_analysis", "")  # Get vision analysis argument if present

        # Handle different cases of insights and vision analysis
        if insights and vision_analysis:
            return f"Response from function 'story_time' with insights: {insights}, visual analysis: {vision_analysis}"
        elif insights:
            return f"Response from function 'story_time' with insights: {insights}"
        elif vision_analysis:
            return f"Response from function 'story_time' with visual analysis: {vision_analysis}"
        else:
            return f"Response from function 'story_time', arguments were present, but no value was passed"

    except Exception as e:
        logging.error(f"An error occurred while processing function 'story_time' args: {e}")
        return f"An error occurred while processing function 'story_time' args: {str(e)}"


def funky():
    # A function object that will be passed to AI LLM bot request for function calling
    tools = [
        {
            "type": "function",
            "function": {
                "name": "story_time",
                "description": "Create insights on the content provided, in addition to visual analysis on images, if available.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "insights": {
                            "type": "string",
                            "description": "Provide a comprehensive analysis which covers data overview, key patterns and relationships, outliers and anomalies, potential insights using basic statistics, sample values, other advanced analysis method like regression, time series etc",
                        },
                        "vision_analysis": {
                            "type": "string",
                            "description": "Contains base64 string representation of annotated statistical charts like correlation heatmaps, distribution plots, scatter plot, timeseries plots and others along with their respective analysis information",
                        }
                    },
                    "required": ["insights", "vision_analysis"],
                    "additionalProperties": False,
                },
            },
        }
    ]
    return tools


def format_ai_message(question, context, img_path=None):
    """Formats the message for the AI bot."""
    messages = [
        {
            "role": "system",
            "content": "You are a expert data analyst, tasked with generating a clear story from the provided input, in a markdown(.md) format." +
            "The story must include data insights, statistical observations, graphs interpretations and your recommendations." +
            "Use well-structured markdown including headers, tables, lists, paragpahs and emphasis."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"{question}\n\n**Context:**\n```\n{context}\n```"
                },
            ],
        },
    ]

    if img_path:
         try:
            base64_image = encode_image(img_path)
            messages[1]["content"].append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low"
                            },
                    },
                )
         except Exception as e:
            logging.error(f"Error processing image, not sending image data : {e}")
    return messages

@retry(stop=stop_after_attempt(CONFIG.get('LLM_RETRY_MAX',3)),
   retry = retry_if_exception_type((Timeout, ConnectionError, HTTPError, RequestException)),
   before_sleep= lambda retry_state: logging.info(f"Retrying API call, attempt number: {retry_state.attempt_number+1}")
    )
def call_ai_api(payload):
    """Makes the API call to AI proxy service"""
    try:
         response = requests.post(CONFIG["AIPROXY_URL"], headers=HEADERS, json=payload, timeout=30)
         response.raise_for_status()
         return response.json() # return the response json
    except HTTPError as e:
            logging.error(f"HTTP error communicating with AI Proxy API: {e}, Response Status: {e.response.status_code}, Response Text: {e.response.text}")
            return None
    except Exception as e:
         logging.error(f"An unexpected error occurred during AI proxy API call : {e}")
         return None

def process_ai_response(response_json, payload):
    """Process response and extract data"""
    if not response_json or 'choices' not in response_json or not response_json['choices']:
        logging.error("Received unexpected response format from AI.")
        return None
    logging.info(f"Received response from AI LLM API service")
    log_model_cost_info(response_json)
    message = response_json['choices'][0]['message']
    if "tool_calls" in message:
        return  message, payload
    elif message.get('content'):
            return message['content'], None
    else:
            logging.error("API returned no content in response.")
            return None, None

def call_ai_for_image_analysis(df, title, fPath, analysis_content, sample_size=3, column_name=None, **kwargs):
     """Helper to call AI if image analysis is enabled"""
     if not CONFIG.get("LLM_ENABLE_IMAGE_ANALYSIS",False):
        return None
     if not CONFIG.get("AIPROXY_TOKEN", None): #Check for token
        logging.warning("Prerequsite AIPROXY_TOKEN value is missing, skipping AI call for the image analysis. Set AIPROXY_TOKEN to use AI features")
        return None
     sample_data_context = ""
     if column_name and column_name in df.columns:
          sample_data_context = select_relevant_columns(df,sample_size=sample_size, columns=[column_name], as_markdown=True, analysis_type="object")
     else :
        text_df = select_relevant_columns(df,  analysis_type ="object") # get the object columns
        if text_df.shape[1]: # ensure that there are object columns
          sample_data_context = select_relevant_columns(df,sample_size=sample_size,columns =text_df.columns.to_list() , as_markdown=True,  analysis_type="object")

     logging.info(f'AI image analysis flag is TRUE. Sending analysis inputs: for {title} chart and sample data: {sample_data_context}')
     try:
           image_analysis = ai_bot_helper(question=f"As a data analyst, please interpret this {title} chart, focusing on key trends, patterns, and any anomalies or outliers. Relate your findings to the data. Explain the trends and insights from the chart, use context if required",
                                              context = f"Relevant info from the provided data is: {sample_data_context}\n\n Previous Analysis:\n{analysis_content}", img_path=fPath) # Added analysis_str to the context
           if image_analysis:
                logging.info(f'Recievd following insights from AI LLM bot: {image_analysis}')
                return f"{image_analysis}\n\n"
           else:
                logging.warning(f"No analysis generated by bot for the image")
                return None
     except Exception as e:
           logging.error(f"Error during AI call: {e}")
           return None

def ai_bot_helper(question, context, img_path=None):
    """Sends a query to an AI LLM bot and returns the response."""
    if not CONFIG.get("AIPROXY_TOKEN",None): #Checking if token is present, before calling api
         logging.error(f"Prerequsite AIPROXY_TOKEN value is missing, skipping AI call for AI bot. Set AIPROXY_TOKEN to use AI features")
         return None
    logging.info(f"Sending question to AI LLM bot: {question}")
    messages = format_ai_message(question, context, img_path)
    function_calling = funky()
    payload = {
       "model": CONFIG["LLM_MODEL"],
        "messages": messages,
        "tools" : function_calling,
        "max_tokens" :CONFIG["LLM_TOKENS_MAX"],
    }
    logging.debug(f"Payload to AI Bot : {payload}") # Log the entire payload

    processed_tool_calls = set() # this set will track processed tool calls
    tool_call_count = 0 # initialize the tool call counter

    while tool_call_count < CONFIG.get("LLM_FUNCTION_CALLS_MAX",5):
        logging.info(f"Calling AI API, attempt: {tool_call_count}")
        response_json = call_ai_api(payload)
        if response_json is None: #if response is none, terminate. Error already logged by the function
           logging.warning(f"API call failed, terminating AI call")
           return None
        message, payload = process_ai_response(response_json, payload)

        if isinstance(message, str): # if we get content back, then return it.
             logging.info(f"Received response from AI, with content: {message}")
             return message
        elif isinstance(message, dict) and "tool_calls" in message:
                tool_calls = message["tool_calls"]
                logging.info(f"Tool calls are present in the response. Information: {tool_calls}")
                
                for tool_call in tool_calls: #iterate over all tool calls
                    tool_call_id = tool_call["id"]
                    if tool_call_id in processed_tool_calls: #if tool id is already present
                       logging.warning(f"Tool call id {tool_call_id} was already present, skipping")
                       continue
                    function_name = tool_call["function"]["name"]
                    function_args = tool_call["function"]["arguments"]
                    if function_name == "story_time":
                         tool_output = perform_story_time(function_args)
                         payload["messages"].append(message)
                         payload["messages"].append({
                             "role": "tool",
                              "tool_call_id": tool_call_id,
                             "content": tool_output
                          })
                         logging.info(f"Processed tool call, id : {tool_call_id}, tool name: {function_name}, tool output: {tool_output}")
                         logging.debug(f"Appended following object to message in payload: {{'role': 'tool', 'tool_call_id': {tool_call_id}, 'content': {tool_output}}}")
                    else:
                        logging.warning(f"Unknown tool name {function_name} from AI Bot")
                        payload["messages"].append(message)
                        payload["messages"].append({
                                "role": "tool",
                                "tool_call_id": tool_call_id,
                                                               "content": f"Unknown tool name {function_name}"
                         })
                        logging.warning(f"Processed tool call, id : {tool_call_id}, tool name: {function_name}")
                        logging.debug(f"Appended following object to message in payload: {{'role': 'tool', 'tool_call_id': {tool_call_id}, 'content': 'Unknown tool name {function_name}'}}")
                    processed_tool_calls.add(tool_call_id) #add tool_call_id to set
                tool_call_count += 1
                continue
        else:
           logging.error(f"Unexpected message from AI Bot: {message}")
           return None # should never reach here
    logging.warning(f"Tool call limit of {CONFIG.get('LLM_FUNCTION_CALLS_MAX',5)} reached. Returning last message without processing.")
    return None


# start here
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated data analysis tool")
    parser.add_argument("dataset_path", type=str, help="Path to the CSV file")

    args = parser.parse_args()

    # Check if the dataset_path argument is provided and valid
    if not args.dataset_path:
        logging.error("The dataset_path argument is required.")
        logging.info("Usage: uv run autolysis.py <dataset_path>")
        sys.exit(1)

    # Check if the provided file exists and is a CSV file
    if not os.path.isfile(args.dataset_path) or not args.dataset_path.endswith(".csv"):
        logging.error("The provided dataset_path must be a valid CSV file.")
        logging.info("Usage: uv run autolysis.py <dataset_path>")
        sys.exit(1)
    if CONFIG.get("LLM_ENABLE_AI_ANALYSIS", False) and not CONFIG.get("AIPROXY_TOKEN", None):
        logging.error("AI analysis flag is enabled. But the environment variable 'AIPROXY_TOKEN' is missing or empty. Static narrative will be saved to README file.")
        # Use the same directory as of the input CSV file
        output_dir = os.path.dirname(args.dataset_path)
        # save all analysis in file
        analyses_file_path = os.path.join(output_dir, f"data_analysis.md")
        # Following variable to track successfully created files. This is to ensure that final document has only generated file and no empty paths
        saved_files = set()
        try:
             df = read_csv_with_multiple_encodings(args.dataset_path)
             logging.info(f"Successfully loaded the csv file")
        except Exception as e:
            logging.error(f"Error reading csv file: {e}")
            sys.exit(1)
        # Data Cleaning
        df = clean_data(df)
        analysis_report_content = do_basic_analysis(df, args.dataset_path)
        # Write analysis content directly to README.md
        output_dir = os.path.dirname(args.dataset_path)
        if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                logging.info(f"Created output directory since it didn't exist: {output_dir}")
        readme_path = os.path.join(output_dir, "README.md")
        try:
            with open(readme_path, "w") as readme_file:
                readme_file.write(analysis_report_content)
            logging.info(f"All activities complete. Static narrative complete. Analysis data copied to the README.md file at: {readme_path} for users")
        except Exception as e:
            logging.error(f"Error writing analysis content to README.md file: {e}")

        sys.exit(0) # exit
    try:
        dataset_path = args.dataset_path
        logging.info(f"Starting data analysis on file: {dataset_path}")

        analysis_report_content, analysis_path, saved_files, ai_insights = analyze_csv_data(dataset_path)

        if not analysis_report_content:
             logging.error(f"Error during the analyses process for the file: {dataset_path}")
             sys.exit(1)
        logging.info(f"Based on analysis, now creating a story in README.md file")

        readme_path = os.path.join(os.path.dirname(dataset_path), "README.md") #setting the readme path

        if CONFIG.get("LLM_ENABLE_AI_ANALYSIS", False):
            logging.info(f"AI analysis flag is enabled. Content may be enriched in README.md file")
            readme_file = tell_me_a_story(analysis_report_content, os.path.dirname(dataset_path), saved_files, ai_insights)
            if readme_file:
                 logging.info(f"Final story is saved to: {readme_file}")
            else:
                logging.error(f"Error generating README.md file with AI assistance. Static content will be used")
        else:
            logging.info(f"AI analysis flag is disabled. Static narrative will be saved to README file, 'without' AI assistance")
            # Write analysis content directly to README.md
            output_dir = os.path.dirname(dataset_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                logging.info(f"Created output directory since it didn't exist: {output_dir}")
            try:
                 # Also add analysis to README.md. This will avoid confusion that readme.md is generated when AI is enabled
                 with open(readme_path, "w") as readme_file:
                    readme_file.write(analysis_report_content)
                 logging.info(f"All activities complete. Static narrative complete. Analysis data copied to the README.md file at: {readme_path} for users")
            except Exception as e:
                 logging.error(f"Error writing analysis content to README.md file: {e}")
    except Exception as e:
        logging.error(f"Error occurred in main function: {e}")
