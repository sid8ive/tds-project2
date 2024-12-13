# /// script
# requires-python = ">=3.12"
# dependencies = [
#   'requests',
#   'pandas',
#   'numpy',
#   'matplotlib',
#   'seaborn',
#   'requests',
#   'chardet',
#   'wordcloud',
#   'scikit-learn',
#   'tabulate',
#   'networkx',
#   'logging'
# ]
# ///
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import chardet
from datetime import datetime
import base64
from wordcloud import WordCloud, STOPWORDS
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
import logging
import argparse
import networkx as nx


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration Section
CONFIG = {
    "AIPROXY_URL": "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
    "AIPROXY_TOKEN": os.getenv("AIPROXY_TOKEN"),
    "LLM_MODEL": "gpt-4o-mini",    
    "OUTLIER_THRESHOLD": 1.5,
    "Z_SCORE_THRESHOLD": 3,
    "PLOT_WIDTH":7, #default plot width
    "PLOT_HEIGHT":4, #default plot height
    "PLOT_DPI":100, # default image dpi
    "MAX_FUNCTION_CALLS":5 #limit the number of function calls per run
}

# Set the API header and key globally for the OpenAI library reference
HEADERS = {"Authorization": f"Bearer {CONFIG['AIPROXY_TOKEN']}", "Content-Type": "application/json"}

fSuffix = ""
#"_"+datetime.now().strftime("%d%m%y%H%M%S")

# --- Helper Functions ---
def prepare_data_for_analysis(df, analysis_type, excluded_keywords = None):
   """ Prepares data for analysis by selecting relevant columns."""
   if excluded_keywords is None:
      excluded_keywords = ['date', 'number', 'id', 'time', 'timestamp']

   if analysis_type == "numeric":
        return df.select_dtypes(include=[np.number])
   elif analysis_type == "object":
       relevant_columns = [col for col in df.select_dtypes(include=['object']).columns if not any(keyword in col.lower() for keyword in excluded_keywords)]
       return df[relevant_columns]
   else:
      return pd.DataFrame() # Return empty dataframe

def handle_analysis_error(func_name, e):
    """Handles analysis errors by logging and returning a markdown comment."""
    logging.error(f"Error during {func_name}: {e}")
    print(traceback.format_exc()) #print traceback
    return f"\n<!--### {func_name}\nError during {func_name}\n-->\n" #Returning markdown comment

def generate_chart(plt, file_name, df, output_dir, saved_files):

    logging.info(f"Generating chart: {file_name}")
    try:
        if len(file_name) > 0:
            # Replace spaces with underscores in file_name
            file_name = file_name.replace(" ", "_")
            full_path = os.path.join(output_dir, file_name)

            plt.tight_layout()
            plt.savefig(full_path, bbox_inches='tight', dpi=CONFIG["PLOT_DPI"])  # Using PLOT_DPI from config
            plt.close()
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
    Args:
    df (pandas.DataFrame): The DataFrame containing the data.
    plot_func (function): The function that generates the chart
    title (str): The title of the plot.
    output_dir (str): The output directory for the image.
    saved_files (set): A set to store the paths of saved files.
    file_name (str) : Filename for the plot image
    *args: args to be passed to plot function
    **kwargs: keyword args to be passed to plot function
     Returns:
         str: The analysis markdown string, or an empty string in case of error
     """
    try:
        plt.figure(figsize=(CONFIG["PLOT_WIDTH"], CONFIG["PLOT_HEIGHT"])) # Setting plot size from the config
        plot_func(df, *args, **kwargs) #Call the plot function, and pass df
        plt.title(title) #Set the title
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels (45 deg) and align right
        if file_name is None:
           file_name=f"{title.lower().replace(' ','_')}{fSuffix}.png"
           
        fPath = generate_chart(plt, file_name, df, output_dir, saved_files)
        if fPath:
            return f"![{title}]({os.path.basename(fPath)})\n\n" #returned markdown for image
        else:
           logging.warning(f"No image was generated for the title {title}")
           return "" # if no image was generated, return empty string
    except Exception as e:
        return handle_analysis_error(f"generating chart {title}", e)




# --- Analysis Functions ---
def generate_word_cloud(df, output_dir, saved_files, column_name=None):
    """
    Generate a word cloud from text data in a DataFrame.
    """
    logging.info("Starting word cloud analysis...")
    try:
        text_df = prepare_data_for_analysis(df, "object")
        if column_name:
            if column_name not in df.columns:
                logging.error(f"Error: column {column_name} not found for wordcloud analysis")
                return None            
            text_data = df[column_name].dropna().apply(lambda x: str(x)) # drop NaN values, string type
        else:
            text_data = text_df.apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1).dropna()
            
        all_text = ",".join([f'"{item}"' for item in text_data])
        stopwords = set(STOPWORDS)
        wordcloud = WordCloud(width=400, height=200, background_color="white", max_words=500, collocations=False, stopwords=stopwords).generate(all_text)
        plt.figure(figsize=(7, 4))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis('off')  # No axes for word cloud
        plt.title("Word Cloud")

        fName = f"word_cloud{fSuffix}.png"
        fPath = generate_chart(plt, fName, df, output_dir, saved_files)
        if fPath:
            analysis_str = f"\n### Word Cloud Analysis\n![Word Cloud]({fName})\n\nThis word cloud visualizes the most frequent words from the content"
            sample_data = "Some of the most used frequent words are: " + ", ".join(list(wordcloud.words_.keys())[:20]) + "\n"
            logging.info(sample_data)
            analysis_str += sample_data
        else:
            analysis_str =  "<!--### Word Cloud Analysis\nNo Word Cloud created\n-->" #returning markdown comment
        logging.info(f"Word cloud saved at {fPath}")
        return analysis_str
    except Exception as e:
         return handle_analysis_error("word cloud analysis", e)


def report_relevant_columns(relevant_cols, text_str):
    """Generates markdown text for relevant columns in the dataset."""
    if relevant_cols and isinstance(relevant_cols, list):
        return f"{text_str}{', '.join(relevant_cols)}\n"
    return ""

def plot_correlation_matrix(df, output_dir, saved_files):
    """Generates a correlation matrix and saves it as an image."""
    logging.info("Starting correlation matrix analysis...")
    numeric_df = prepare_data_for_analysis(df, "numeric")
    if numeric_df.empty:
        logging.warning("No numeric columns found for correlation analysis.")
        return  f"\n<!--### Correlation Analysis\nNo correlation analysis generated\n-->\n" #returning markdown comment
    correlation = numeric_df.corr()
    logging.debug(f"Correlation Matrix (Text Table): {correlation}")

    def plot_corr_heatmap(df, correlation):
      sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)

    # Use common function to generate plot and save
    analysis_str= create_plot_with_title(df, plot_corr_heatmap, "Correlation Heatmap", output_dir, saved_files, correlation=correlation)
    if analysis_str:
        analysis_str = f"\n### Correlation Analysis\n{analysis_str}\nThis heatmap visualizes the correlation between numerical features in the dataset.\n"
        #analysis_str+= report_relevant_columns(numeric_df.columns.to_list(), "") # sending a list of column names now.
        
    else:
        analysis_str =  f"\n<!--### Correlation Analysis\nNo correlation analysis generated\n-->\n" #returning markdown comment
    logging.info("Correlation heatmap saved.")
    return analysis_str

def plot_outliers(df, output_dir, saved_files):
    """Detects and visualizes outliers in the numeric columns of a DataFrame."""
    logging.info("Starting outlier analysis...")
    try:
        numeric_df = prepare_data_for_analysis(df, "numeric")
        if numeric_df.empty:
            logging.warning("No numeric data for outlier analysis.")
            return  f"\n<!--### Outlier Detection\nNo outlier analysis generated\n-->\n" #returning markdown comment

        outliers = {}
        for col in df.select_dtypes(include=[np.number]).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - CONFIG["OUTLIER_THRESHOLD"] * IQR
            upper_bound = Q3 + CONFIG["OUTLIER_THRESHOLD"] * IQR

            lower_outliers = df.loc[df[col] < lower_bound, col]
            upper_outliers = df.loc[df[col] > upper_bound, col]

            # Creating a dictionary which contains sample of 5 or actual number that is present (whichever is minimum) of
            # lower bound and upper bound outliers and their total count
            outliers[col] = {
                'lower_bound': lower_outliers.sample(n=min(5, len(lower_outliers))).tolist() if not lower_outliers.empty else [],
                'upper_bound': upper_outliers.sample(n=min(5, len(upper_outliers))).tolist() if not upper_outliers.empty else [],
                'count': len(lower_outliers) + len(upper_outliers)
            }


        # Z-score analysis for outlier detection
        z_scores = (numeric_df - numeric_df.mean()) / numeric_df.std()
        z_outliers = z_scores[abs(z_scores) > CONFIG["Z_SCORE_THRESHOLD"]]  # Detecting outliers with Z-score threshold of 3

        # Display detected outliers if any
        if not z_outliers.empty:
            logging.debug(f"Outliers detected using Z-score: {z_outliers}")
        else:
            logging.debug("No outliers detected using Z-score.")

        def plot_box_plot(df, data):
            sns.boxplot(data=data)
        # Use common function to generate plot and save
        analysis_str= create_plot_with_title(df, plot_box_plot, "Outlier Detection Box Plot", output_dir, saved_files, data=numeric_df)
        if analysis_str:
            analysis_str = f"\n### Outlier Detection\n{analysis_str}\nThis boxplot shows the distribution of values for numerical features and highlights potential outliers\n"
            #analysis_str+= report_relevant_columns(numeric_df.columns.to_list(), "") # sending a list of column names now.
        else:
            analysis_str = f"\n<!--### Outlier Detection\nNo outlier analysis generated\n-->\n"   #returning markdown comment
        logging.info("Box plot saved.")
        return analysis_str

    except Exception as e:
         return handle_analysis_error("outlier detection", e)

def plot_time_series(df, output_dir, saved_files):
    """
    Generates time series plot if Date field available in the dataframe
    """
    logging.info("Starting time series analysis...")
    try:
        # Look for a column containing the word 'date' in any case
        date_column = next((col for col in df.columns if 'date' in col.lower()), None)
        if not date_column:
            logging.warning("No 'Date' column found for time series analysis")
            return f"\n<!--### Time Series Analysis\nNo time series analysis found\n-->\n"  #returning markdown comment
      
        # validate if date column is correct date format
        try:
            df[date_column] = pd.to_datetime(df[date_column], errors='raise')
        except Exception as e:
            logging.warning(f"Column '{date_column}' does not have valid date format for time series analysis")
            return f"\n<!--### Time Series Analysis\nNo time series analysis generated as date column not in correct format\n-->\n"  #returning markdown comment


        # Set the date column as index
        df.set_index(date_column, inplace=True)


        numeric_cols = df.select_dtypes(include=np.number).columns
        if len(numeric_cols) == 0:
            logging.warning("No numeric column found to plot time series analysis")
            return f"\n<!--### Time Series Analysis\nNo time series analysis found\n-->\n" #returning markdown comment

         # Use common function to generate plot and save
        analysis_str= create_plot_with_title(df, plot_time_series_chart, "Time Series Analysis", output_dir, saved_files, numeric_cols=numeric_cols)
        if analysis_str:
            analysis_str = f"### Time Series Analysis\n{analysis_str}\nThis line plot shows trends over time for numerical data with a `Date` column.\n"
            #analysis_str+= report_relevant_columns(numeric_cols.to_list(), "Relevant columns from the dataset are:") # sending a list of column names now.
        else:
            analysis_str = f"\n<!--### Time Series Analysis\nNo time series analysis found\n-->\n"  #returning markdown comment
        logging.info("Time series analysis chart saved.")
        return analysis_str
    except Exception as e:
         return handle_analysis_error("time series analysis", e)


def plot_geographic_analysis(df, output_dir, saved_files):
    """
    Generates geographic plots if `Latitude` and `Longitude` columns are present.
    """
    logging.info("Starting geographic analysis...")
    try:
         # Look for columns containing the word 'latitude'/'longitude' in any case
        latitude_column = next((col for col in df.columns if 'latitude' in col.lower()), None)
        longitude_column = next((col for col in df.columns if 'longitude' in col.lower()), None)
        if not latitude_column or not longitude_column:
           logging.warning("No 'Latitude' or 'Longitude' columns found for geographic analysis")
           return f"\n<!--### Geographic Distribution\nNo geographic data found\n-->\n"  #returning markdown comment
        
        # Use common function to generate plot and save
        analysis_str=create_plot_with_title(df, sns.scatterplot, "Geographic Distribution of Data", output_dir, saved_files, x=longitude_column, y=latitude_column, data=df)
        if analysis_str:
            analysis_str = f"### Geographic Distribution\n{analysis_str}\nThis scatter plot maps data points based on their geographic coordinates (`Latitude` and `Longitude`)\n"
            # Add sample of 5 rows from data            
            sample_data = f"\nSample rows for context\n{df[[latitude_column,longitude_column]].sample(min(5, len(df))).fillna('').to_markdown(index=False)}"
            analysis_str+=sample_data

        else:
             analysis_str = f"\n<!--### Geographic Distribution\nNo geographic data found\n-->\n"   #returning markdown comment
        logging.info("Geographic distribution chart saved.")
        return analysis_str
    except Exception as e:
         return handle_analysis_error("geographic analysis", e)

def plot_network_analysis(df, output_dir, saved_files):
    """
    Performs network analysis if the required columns are present
    """
    logging.info("Starting network analysis...")
    try:
        # Assuming your DataFrame has 'source' and 'destination' columns
        if 'source' not in df.columns or 'destination' not in df.columns:
            logging.warning("No 'source' or 'destination' columns found for network analysis")
            return  f"\n<!--### Network Analysis\nNo network analysis generated\n-->\n" #returning markdown comment
        # Create graph
        G = nx.from_pandas_edgelist(df, source='source', target='destination',create_using=nx.DiGraph())

         # Calculate network metrics
        degrees = dict(G.degree())
        centrality = nx.degree_centrality(G)
        # Visualization and save
        def plot_network_chart(df, G,degrees):
            nx.draw(G, with_labels=True, node_size=500, font_size=10, node_color=list(degrees.values())) # color map is based on node degree
        # Use common function to generate plot and save
        analysis_str = create_plot_with_title(df, plot_network_chart, "Network Analysis", output_dir, saved_files, G=G,degrees=degrees)
        if analysis_str:
            analysis_str = f"### Network Analysis\n{analysis_str}\nThis plot shows the network of cities and flights between them.\n"
            analysis_str+= f"Nodes: {list(G.nodes())} \n Edges: {list(G.edges())} \n Node Degrees: {degrees} \n Centralities: {centrality}\n"
             # Add sample of 5 rows from data            
            sample_data = f"\nSample rows for context\n{df.sample(min(5, len(df))).fillna('').to_markdown(index=False)}"
                                                          
            analysis_str+=sample_data
        else:
            analysis_str= f"\n<!--### Network Analysis\nNo network analysis generated\n-->\n" #returning markdown comment
        logging.info("Network analysis chart saved.")
        return analysis_str

    except Exception as e:
         return handle_analysis_error("network analysis", e)


def plot_categorical_data(df, output_dir, saved_files):
    """
    Generates bar plots for each categorical column
    """
    logging.info("Starting Categorical data analysis")
    try:

        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) == 0:
            logging.warning("No categorical column found.")
            return f"\n<!--### Categorical Data Distribution\nNo categorical columns to analyze\n-->\n" #returning markdown comment
        analysis_str = "### Categorical Data Distribution\nThe following plots show the distribution of categorical data:\n"
        
        top_n = 10  # Number of top categories to plot

        for col in categorical_cols:
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
            analysis_str +=  create_plot_with_title(df,plot_categorical_chart, f"Distribution of {col}", output_dir, saved_files, value_counts=value_counts)
            if analysis_str:
                analysis_str += f"\n"
                # Add sample of 5 rows from data
                
                sample_data = f"\nSample rows for context\n{df[[col]].sample(min(5, len(df))).fillna('').to_markdown(index=False)}"
                analysis_str+=sample_data
            logging.info(f"Categorical distribution chart for {col} saved")
        return analysis_str

    except Exception as e:
        return handle_analysis_error("categorical plot analysis", e)

def plot_histograms(df, output_dir, saved_files):
    """
     Generates histogram plots for each numerical column
    """
    logging.info("Starting Histograms data analysis")
    try:
        numeric_df = prepare_data_for_analysis(df, "numeric")
        if numeric_df.empty:
            logging.warning("No numeric column found.")
            return f"\n<!--### Numerical Data Histograms\nNo Numerical column found\n-->\n"  #returning markdown comment
        analysis_str = "\n### Numerical Data Histograms\n"
        for col in numeric_df.columns:
            # Use common function to generate plot and save
            analysis_str +=  create_plot_with_title(df, plot_histogram_chart, f"Distribution of {col}", output_dir, saved_files, col=col)
            if analysis_str:
                analysis_str +=  f"\n\n"
                # Add sample of 5 rows from data
                #analysis_str+= f"Relevant columns from the dataset are:{', '.join(numeric_df.columns)}\n" #Adding column names
            logging.info(f"Histogram distribution chart for {col} saved")
        return analysis_str

    except Exception as e:
         return handle_analysis_error("histogram analysis", e)

def perform_clustering(df, output_dir, saved_files, n_clusters=3):
    """
    Performs clustering on numerical data
    """
    logging.info("Starting clustering analysis")
    try:
        numeric_df = prepare_data_for_analysis(df, "numeric")
        if numeric_df.empty:
           logging.warning("No numerical columns for cluster analysis")
           return f"\n<!--### Clustering Analysis\nNo numerical columns for clustering analysis\n-->\n"   #returning markdown comment
        
        # Impute missing values with the mean
        imputer = SimpleImputer(strategy='mean')
        df_scaled = imputer.fit_transform(numeric_df)

        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_scaled)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42,n_init=10)
        df['Cluster'] = kmeans.fit_predict(df_scaled)
        
       # Use common function to generate plot and save
        analysis_str = create_plot_with_title(df, plot_cluster_chart, "Cluster Analysis", output_dir, saved_files, df_scaled=df_scaled) #removed df from kwargs
        if analysis_str:
            analysis_str = f"### Clustering Analysis\n{analysis_str}\nThis scatter plot represents cluster analysis\n"
            # Add sample of 5 rows from data            
            sample_data = f"\nSample rows for context\n{df.sample(min(5, len(df))).fillna('').to_markdown(index=False)}"
            analysis_str+=sample_data
        else:
            analysis_str= f"\n<!--### Clustering Analysis\nNo Clustering analysis generated\n-->\n" #returning markdown comment

        logging.info("Cluster analysis complete.")
        return analysis_str
    except Exception as e:
         return handle_analysis_error("cluster analysis", e)


def perform_pca(df, output_dir, saved_files, n_components=2):
    """
    Performs PCA for dimensionality reduction
    """
    logging.info("Starting PCA analysis")
    try:
        numeric_df = prepare_data_for_analysis(df, "numeric")
        if numeric_df.empty:
             logging.warning("No numerical columns for PCA analysis")
             return f"\n<!--### PCA Analysis\nNo numerical columns found for PCA analysis\n-->\n"  #returning markdown comment
        
        # Impute missing values with the mean
        imputer = SimpleImputer(strategy='mean')
        df_scaled = imputer.fit_transform(numeric_df)

        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_scaled)
        pca = PCA(n_components=n_components)
        pca_components = pca.fit_transform(df_scaled)
        df['PCA1'] = pca_components[:, 0]
        df['PCA2'] = pca_components[:, 1]

        # Use common function to generate plot and save
        analysis_str = create_plot_with_title(df,plot_pca_chart,"Principal Component Analysis", output_dir, saved_files, df_scaled=df_scaled) #removed df from kwargs
        if analysis_str:
           analysis_str = f"\n### PCA Analysis\n{analysis_str}\nThis plot shows the principle component analysis.\n"
        else:
            analysis_str= f"\n<!--### PCA Analysis\nNo PCA analysis generated\n-->\n"   #returning markdown comment
        logging.info("PCA analysis complete.")
        return analysis_str

    except Exception as e:
          return handle_analysis_error("pca analysis", e)

def read_csv_with_multiple_encodings(file_path):
    try:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        enc = result['encoding']
        logging.info(f"File encoding identified as: {enc}")

        try:
            df = pd.read_csv(file_path, encoding=enc)
            return df  # Return the dataframe if successful
        except UnicodeDecodeError as e:
            # If the encoding fails, continue to the next one
            logging.error(f"Failed to read with encoding: {enc}")
            raise ValueError(f"Unable to read the file with encoding {enc}: {e}")  # re-raise the exception for caller to handle.
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        raise

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
    logging.info(f"Column names changed to {df.columns}")

    # Further cleaning logic for text or other data
    #Example
    for column in df.select_dtypes(include='object'):
        df[column] = df[column].str.strip()  #remove whitespace from text

    logging.info(f"Removed white spaces from all string columns")
    return df

def do_basic_analysis(df, csv_file):
    """Performs basic analysis of the dataframe

    Args:
        df (pd.DataFrame): Input dataframe
        csv_file (str): Input CSV file path

    Returns:
        str: analysis output as string
    """
    # Summary Statistics (for both numeric and categorical columns)
    #details_summary = df.describe(include='all')        
    details_summary = df.describe(include='all').map(lambda x: f"{x:.2f}" if isinstance(x, float) else (x if pd.notna(x) else ''))
    # Add sample of 5 rows from data
    sample_data = f"\n{df.sample(min(5, len(df))).to_markdown(index=False)}"
    

    # Missing Values Count
    missing_values = df.isna().sum()

    # Percentage of Missing Values for each column
    missing_percentage = (df.isna().mean() * 100)

    # Displaying the missing values as percentage
    missing_info = pd.DataFrame({
        'Missing Values Count': missing_values,
        'Missing Percentage (%)': missing_percentage
    })

    analysis_str = "# Interim Automated Data Assessment Report\n\n"    
    analysis_str += "## Overview\n"
    analysis_str += f"File name: {os.path.basename(csv_file)}\n\n"
    analysis_str += f"The file has {len(df)} rows and {len(df.columns)} columns\n\n"

    analysis_str +="### First 5 sample rows from file, for context\n\n"
    analysis_str += sample_data + "\n\n"

    # Write details summary as Markdown table
    analysis_str += "### Summary Statistics of the file\n"
    
    details_summary_str = details_summary.dropna(axis=0, how='all').to_markdown()  # Converts the DataFrame to Markdown format, remove nan rows.
    analysis_str += details_summary_str + "\n\n"

    # Write missing values report as Markdown table
    analysis_str += "## Missing values report\n"
    missing_info_str = missing_info.to_markdown()  # Converts the DataFrame to Markdown format
    analysis_str += missing_info_str + "\n\n"
    logging.info("Generated basic summary statistics and checked for missing values")
    
    
    return analysis_str

def analyze_csv(csv_file):
    try:
        logging.info(f"Reading .csv file: {csv_file}")
        df = read_csv_with_multiple_encodings(csv_file)
        logging.info(f"Successfully loaded the csv file")
    except Exception as e:
        logging.error(f"Error reading csv file: {e}")
        return None, None  # return None, so that the main function can handle it and log the errors

    # Use the same directory as of the input CSV file
    output_dir = os.path.dirname(csv_file)

    # save all analysis in file
    analyses_file_path = os.path.join(output_dir, f"data_analyses{fSuffix}.md")

    logging.info(f"Output directory set to: {output_dir}")

    # Following variable to track successfully created files. This is to ensure that final document has only generated file and no empty paths
    saved_files = set()
    try:
          # Data Cleaning
          df = clean_data(df)

          analysis_content = ""
          analysis_content += do_basic_analysis(df, csv_file)
          analysis_content += generate_word_cloud(df, output_dir, saved_files)
          analysis_content += plot_correlation_matrix(df, output_dir, saved_files)
          analysis_content += plot_outliers(df, output_dir, saved_files)
          analysis_content += plot_time_series(df, output_dir, saved_files)
          if any(col.lower() in ['latitude', 'longitude'] for col in df.columns):
            analysis_content += plot_geographic_analysis(df, output_dir, saved_files)
          if 'source' in df.columns and 'destination' in df.columns:
           analysis_content += plot_network_analysis(df, output_dir, saved_files)
          analysis_content += plot_categorical_data(df, output_dir, saved_files)
          analysis_content += plot_histograms(df, output_dir, saved_files)
          analysis_content += perform_clustering(df, output_dir, saved_files)
          analysis_content += perform_pca(df, output_dir, saved_files)          

          # Write analysis to file
          try:
            with open(analyses_file_path, "w") as analyses_file:
                analyses_file.write(analysis_content)
          except Exception as e:
            logging.error(f"Error writing to analysis file {analyses_file_path}: {e}")
            return None, saved_files
          logging.info(f"All analysis written to file {analyses_file_path}")
          return analyses_file_path, saved_files

    except Exception as e:
        logging.error(f"Error during the analysis process: {e}")
        return None, None

# Now write the story to README.md, integrating images and captions
def tell_me_a_story(analyses_path, saved_files):
    """
    Narrates a story based on the analysis done and available in the interim analyses.md file

    Args:
        analyses_path (str): path to analyses file. Readme.md too will be written in this directory
        saved_files (set): set of paths of the files saved during the analyses process
    """
    readme_path = os.path.join(analyses_path, "README.md")
    try:
        with open(readme_path, "x") as readme_file, open(analyses_path, "r") as analysis_file:
            analyses_content = analysis_file.read()
            story_context = f"Dataset Analysis:\n{analyses_content}"
            story = bot_helper(
                "Generate a creative but data-driven story based on the analysis. It should be in markdown format, well-structured, using headers, lists, and emphasis appropriately. "
                "The narrative should clearly describe the data to users, the analysis performed, insights or anomalies identified, and implications. Include relevant images from the analysis "
                "and describe them in the story to make it visually engaging. Use external hyperlinks and references to strengthen the storyline",
                story_context
            )
            # " Focus on four aspects:  a) The data you received b) The analysis you carried out c) The insights you discovered d) The implications of findings."
            readme_file.write("*Every story is complicated until it finds the right storyteller — Anonymous*\n\n\n")
            readme_file.write(f"{story}\n")
            logging.info("Added story to README.md file")
            return readme_path
    except FileExistsError:
        logging.warning(f"File {readme_path} exists already. Not generating the README.md")
        return readme_path
    except Exception as e:
        logging.error(f"Error generating README.md: {e}")
        return None

# encoding the image to base64. Used by bot_helper_image function
def encode_image(image_path):
    """Encode an image to a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to generate a vision analyses by LLM using image as input
def bot_helper_image(image_path, question="As a data analyst, describe the data and text in this image", context=""):
    """Send an image and question to OpenAI GPT-4 model for analysis."""
    logging.info(f"Image received: {image_path}")
    # Encode the image to base64
    base64_image = encode_image(image_path)

    # Create the payload
    payload = {
        "model": CONFIG["LLM_MODEL"],  # openai uses the same model for vision
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{question}\n\n**Context:**\n```\n{context}\n```"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low"
                        },
                    },
                ],
            }
        ],
    }

    try:
        # Make the API request
        response = requests.post(CONFIG["AIPROXY_URL"], json=payload, headers=HEADERS)
        response.raise_for_status()  # Raise an error for bad HTTP status codes

        # Parse and return the response
        response_json = response.json()

        if "choices" in response_json and response_json["choices"]:
            logging.info("Printing the response from AI LLM API")            
            for key, value in response_json.items():
                 logging.debug(f"{key}: {value}")
            return response_json["choices"][0]["message"]["content"]
        else:
            logging.error("Unexpected response format.")
            return "Unexpected response format from AI LLM API service"

    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with AI Proxy API: {e}")
        return f"An error occurred while fetching AI insights: {str(e)}"
    except Exception as e:
     logging.error(f"An unexpected error occurred during AI proxy API call : {e}")
     return f"An unexpected error occurred: {e}"

# Function to interact with LLM via AI Proxy
def bot_helper(question, context):
    """
    Sends a query to an AI LLM bot and returns the response.

    Args:
        question (str): The query to be sent to the bot.
        context (str): Additional context to provide to the bot.

    Returns:
        str: The response from the bot, or an error message if the request fails.
    """
    try:
        logging.info(f"Sending question to AI LLM bot: {question}")
        payload = {
            "model": CONFIG["LLM_MODEL"],  #
            "messages": [
                {
                    "role": "system",
                    "content": "You are a data analysis expert tasked with generating a clear and concise story in markdown format. The story must include data insights, statistical observations, visualization interpretations and recommendations. Use well-structured markdown including headers, lists, and emphasis."
                },
                {
                    "role": "user",
                    "content": f"{question}\n\n**Context:**\n```\n{context}\n```"
                },
            ],
            "max_tokens": 200,  # Increased max_tokens for detailed responses
        }
        response = requests.post(CONFIG["AIPROXY_URL"], headers=HEADERS, json=payload)
        response.raise_for_status()
        response_json = response.json()

        if 'choices' in response_json and response_json['choices']:
            logging.info("Printing the response from AI LLM API")
            for key, value in response_json.items():
                logging.debug(f"{key}: {value}")
            return response_json['choices'][0]['message']['content']
        else:
            logging.error("Received unexpected response format from AI.")
            return "Unexpected response format from AI LLM API service"

    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with AI Proxy API: {e}")
        return f"An error occurred while fetching AI insights: {str(e)}"
    except Exception as e:
     logging.error(f"An unexpected error occurred during AI proxy API call : {e}")
     return f"An unexpected error occurred: {e}"


# --- Plotting Functions ---
def plot_time_series_chart(df, numeric_cols):
    """ Helper function to plot time series graph"""
    for col in numeric_cols:
        plt.plot(df.index, df[col], label=col)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.xticks(rotation=45)

def plot_categorical_chart(df,value_counts):
    """ Helper function to plot categorical data"""
    value_counts.plot(kind='barh', color='skyblue')

def plot_histogram_chart(df, col):
    """ Helper function to plot histogram data"""
    df[col].hist()
    plt.xticks(rotation=45, ha='right')

def plot_cluster_chart(df, df_scaled):
     """ Helper function to plot clusters"""
     plt.scatter(df_scaled[:, 0], df_scaled[:, 1], c=df['Cluster'], cmap='viridis')

def plot_pca_chart(df, df_scaled):
    """ Helper function to plot pca data"""
    plt.scatter(df['PCA1'], df['PCA2'], alpha=0.7, edgecolors='w', s=80, label='Data Points')
    plt.xlabel("Principal Component 1", fontsize=12)
    plt.ylabel("Principal Component 2", fontsize=12)
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.legend(loc="best", fontsize=10)
    plt.tight_layout()

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

    try:
        dataset_path = args.dataset_path

        logging.info(f"Starting data analysis on file {dataset_path}")

        # takes the .csv file and analyse it for various statistical analyses
        analyses_file, saved_files = analyze_csv(dataset_path)

        if analyses_file:
            # takes the .md analyses file and narrates a story in readme.md file
            readme_file = tell_me_a_story(os.path.dirname(analyses_file), saved_files)
            if readme_file:
                logging.info(f"Analysis of the data is complete. Interim results saved to {analyses_file} and final story to {readme_file}")
                
            else:
                 logging.error("Error generating README.md file")                 
        else:            
            logging.error(f"Error during the analyses process")
    except Exception as e:
        logging.error(f"Error occurred in main function: {e}")
        
