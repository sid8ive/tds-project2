import os
import subprocess
import sys

# /// script
# dependencies = [
#   'requests',
#   'pandas',
#   'matplotlib',
#   'seaborn',
#   'tabulate',
#   'requests',
#   'chardet',
#   'wordcloud',
#   'openai',
#   'geopandas',
#   'folium',
#   'chardet'
# ]
# ///


# Try importing the installed packages
try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import requests
    import chardet
    from datetime import datetime
    from matplotlib import rcParams
    import re
    import logging
    import base64
    from wordcloud import WordCloud, STOPWORDS
    import openai
    import geopandas as gpd
    import folium
    import chardet
    

    print("All packages are successfully imported.")
except ImportError as e:
    print(f"ImportError: {e}. Ensure all packages are installed. You may need to re-run the script.")
    sys.exit(1)

# Configuration Section
CONFIG = {
    #"AIPROXY_URL": "https://api.openai.com/v1/chat/completions",
    "AIPROXY_URL": "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",    
    "AIPROXY_TOKEN": os.getenv("AIPROXY_TOKEN")
}


# Set the API header and key globally for the OpenAI library reference
HEADERS = {"Authorization": f"Bearer {CONFIG['AIPROXY_TOKEN']}", "Content-Type": "application/json"}
openai.api_key =  {CONFIG['AIPROXY_TOKEN']}

saved_charts = []


# Function to generate a word cloud with explanations for each step
def generate_word_cloud(df, readme_file, output_dir, saved_files):
    print("Starting word cloud analysis...")

    # Combine all text data from the dataframe into one large string
    all_text = ""
    for col in df.select_dtypes(include=['object']).columns:
        all_text += " " + " ".join(df[col].dropna().astype(str))

    # Combine and clean text
    all_text = " ".join(df.select_dtypes(include=['object']).apply(lambda x: ' '.join(x.dropna().astype(str)), axis=0))
    all_text = re.sub(r'http[s]?://\S+', '', all_text.lower())
    all_text = re.sub(r'[^\w\s]', '', all_text)  # Remove punctuation
    all_text = re.sub(r'\b\w{1,2,3}\b', '', all_text)  # Remove short words upto 3 characters
    stopwords = set(STOPWORDS)

    # Generate the word cloud
    wordcloud = WordCloud(width=400, height=200, background_color="white", max_words=200, stopwords=stopwords).generate(all_text)

    # Plot the word cloud
    plt.figure(figsize=(6, 3))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')  # No axes for word cloud
    plt.title("Word Cloud of data")

    # Save the word cloud visualization
    generate_chart(plt, "word_cloud.png", df, output_dir, saved_files)
    readme_file.write(f"![Word Cloud](word_cloud.png)\n\n")
    print("Word cloud saved.")
    return "word_cloud.png"



# Function to generate a vision analyses by LLM using image as input
# Refer https://platform.openai.com/docs/guides/vision?lang=node
def bot_helper_image(image_path, question="As a data analyst, describe the data and text in this image."):
    """Send an image and question to OpenAI GPT-4 model for analysis."""
    # API Endpoint
    endpoint = CONFIG['AIPROXY_URL']
    
    # Set your OpenAI API key
    api_key = CONFIG["AIPROXY_TOKEN"]

    # Encode the image to base64
    base64_image = encode_image(image_path)

    # Create the payload
    payload = {
        "model": "gpt-4o-mini",  # openai uses the same model for vision
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
    }

    # # Define headers
    # headers = {
    #     "Authorization": f"Bearer {api_key}",
    #     "Content-Type": "application/json",
    # }

    try:
        # Make the API request
        response = requests.post(endpoint, json=payload, headers=HEADERS)
        print("Response from openAI on image assessment",response)
        response.raise_for_status()  # Raise an error for bad HTTP status codes

        # Parse and return the response
        response_json = response.json()
        if "choices" in response_json and response_json["choices"]:
            return response_json["choices"][0]["message"]["content"]
        else:
            return "Unexpected response format."

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

#encoding the image to base64. Used by bot_helper_image function
def encode_image(image_path):
    """Encode an image to a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Function to interact with LLM via AI Proxy
def bot_helper(question, context):
    try:
        print(f"Sending question to AI LLM bot: {question}")
        payload = {
            "model": "gpt-4o-mini",  # 
            "messages": [
                {
                    "role": "system",
                    "content": "You are a data scientist, specializing in analyzing and providing insights from CSV data. Focus on statistical analysis, pattern recognition, and actionable recommendations. Use tabular or bulletised or visual representation where helpful"
                },
                {
                    "role": "user",
                    "content": f"{question}\n\n**Context:**\n```\n{context}\n```"
                }
            ]
        }
        response = requests.post(CONFIG["AIPROXY_URL"], headers=HEADERS, json=payload)
        response.raise_for_status()
        response_json = response.json()
        
        if 'choices' in response_json and response_json['choices']:
            print("Received response from AI.")
            return response_json['choices'][0]['message']['content']
        else:
            print("Received unexpected response format from AI.")
            return "Unexpected response format from AI service."

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with AI Proxy: {e}")
        return f"An error occurred while fetching insights: {str(e)}"

# Function to detect encoding
def detect_encoding(file_path):
    try:
        print(f"Detecting encoding for {file_path}...")
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        result = chardet.detect(raw_data)
        print(f"Detected encoding: {result['encoding']}")
        return result['encoding']
    except Exception as e:
        print(f"Error detecting file encoding: {e}")
        sys.exit(1)

# Function to generate charts and  visualizations 
def generate_chart(plt, file_name, df, output_dir, saved_files):
    try:
        full_path = os.path.join(output_dir, file_name)
        print(f"Generating chart/graph as {file_name}...")
        plt.tight_layout()
        plt.savefig(full_path, bbox_inches='tight', dpi=100)
        print(f"Chart saved at: {full_path}")
        plt.close()
        
        # Add to saved files
        if os.path.exists(full_path):
            saved_files.append(full_path)
        else:
            print(f"Warning: File {full_path} does not exist after saving.")
    except Exception as e:
        print(f"Error generating the chart {file_name}: {e}")

# # Basic quality check for charts
# def evaluate_chart_quality(fig, data):
#     print("Evaluating chart quality...")
#     # Example criteria:
#     # - Check if the plot has a title
#     # - Ensure labels are not overlapping (this is very simplistic)
#     if fig._suptitle:
#         title_score = 1
#     else:
#         title_score = 0
    
#     # Check for overlap - this is a placeholder; actual implementation would be more complex
#     overlap_score = 1 if not plt.gca().get_xticklabels()[0].get_text().strip() == "" else 0
    
#     quality = (title_score + overlap_score) / 2  # Simple average score
#     print(f"Chart quality score: {quality}")
#     return quality

# Function to create correlation matrix
def plot_correlation_matrix(df, readme_file, output_dir, saved_files):
    print("Starting correlation matrix analysis...")
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty:
        print("Warning: No numeric columns found for correlation analysis.")
        return None
    correlation = numeric_df.corr()
    print("Correlation Matrix (Text Table):")
    print(correlation)
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title("Correlation Heatmap")
    generate_chart(plt, "correlation_heatmap.png", df, output_dir, saved_files)
    readme_file.write(f"![Correlation Heatmap](correlation_heatmap.png)\n\n")
    print("Correlation heatmap saved.")
    return correlation


def plot_outliers(df, readme_file, output_dir, saved_files):
    print("Starting outlier analysis...")
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty:
        print("No numeric data for outlier analysis.")
        return

    # Box plot
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=numeric_df)
    plt.title("Outlier Detection (Box Plot)")
    plt.xticks(rotation=90)
    generate_chart(plt, "outliers_boxplot.png", df, output_dir, saved_files)
    readme_file.write(f"![Outlier Detection (Box Plot)](outliers_boxplot.png)\n\n")
    print("Box plot saved.")

    # Z-score analysis
    z_scores = (numeric_df - numeric_df.mean()) / numeric_df.std()
    threshold = 3  # Adjust threshold as needed
    outliers = z_scores[z_scores.abs() > threshold]

    if not outliers.empty:
        print("Outliers detected using Z-score:")
        print(outliers)
        # Consider additional visualization or analysis for identified outliers



# Function for time series analysis. USes all columns with Date or Year mentioned and formats accordingly
# This will match columns like "birth_YEAR_CHIld", "publication_date"
def plot_time_series(df, readme_file, output_dir, saved_files):
    print("Starting time series analysis...")

    time_series_columns = [col for col in df.columns if re.search(r'(year|date)', col.lower())]

    for time_col in time_series_columns:
        try:
            # Convert to datetime, handling different formats as needed
            if 'Year' in time_col:
                df[time_col] = pd.to_datetime(df[time_col], format='%Y')
            else:
                df[time_col] = pd.to_datetime(df[time_col])

            df = df.sort_values(by=time_col)

            numeric_columns = df.select_dtypes(include=['number']).columns
            if numeric_columns.empty:
                print(f"No numeric columns to plot against {time_col}.")
                continue

            for numeric_col in numeric_columns:
                plt.figure(figsize=(12, 6))
                sns.lineplot(data=df, x=time_col, y=numeric_col)
                plt.title(f"Time Series Analysis for {numeric_col} over {time_col}")
                plt.legend([numeric_col], loc='upper left')  # Add legend
                generate_chart(plt, f"time_series_{time_col}_{numeric_col}.png", df, output_dir, saved_files)
                readme_file.write(f"![Time Series Analysis for {numeric_col} over {time_col}](time_series_{time_col}_{numeric_col}.png)\n\n")
                print(f"Time series plot for {numeric_col} over {time_col} saved.")

        except Exception as e:
            print(f"Error in Time Series Analysis for {time_col}: {e}")

# Function for geographic analysis. Uses country, city, longitude, latitude column names
# case insitive and uses any column that may contain the keywords like birth_CItY or city_LONGitude
def plot_geographic_analysis(df, readme_file, output_dir, saved_files):
    print("Starting geographic analysis...")

    # Check for latitude and longitude columns
    latitude_cols = [col for col in df.columns if 'latitude' in col.lower()]
    longitude_cols = [col for col in df.columns if 'longitude' in col.lower()]

    if latitude_cols and longitude_cols:
        # Assuming the first match is the correct one
        latitude_col = latitude_cols[0]
        longitude_col = longitude_cols[0]

        # Standard scatter plot
        plt.figure(figsize=(10, 8))
        numeric_column = df.select_dtypes(include=['number']).columns[0] if not df.select_dtypes(include=['number']).empty else 'Count'
        sns.scatterplot(data=df, x=longitude_col, y=latitude_col, hue=numeric_column)
        plt.title("Geographic Analysis")
        plt.legend(title=numeric_column)
        generate_chart(plt, "geographic_analysis.png", df, output_dir, saved_files)
        readme_file.write(f"![Geographic Analysis](geographic_analysis.png)\n\n")
        print("Geographic plot saved.")

    # Check for city and country columns
    city_cols = [col for col in df.columns if 'city' in col.lower()]
    country_cols = [col for col in df.columns if 'country' in col.lower()]

    if city_cols and country_cols:
        # Assuming the first match is the correct one
        city_col = city_cols[0]
        country_col = country_cols[0]

        # Geocode cities and countries (replace with your preferred geocoding service)
        gdf = gpd.GeoDataFrame(df)
        gdf['geometry'] = gpd.GeoSeries.from_xy(gdf['Longitude'], gdf['Latitude'])  # Assuming you have geocoded the data

        # Create a map
        m = folium.Map(location=[40, 0], zoom_start=2)

        # Add markers to the map
        for index, row in gdf.iterrows():
            folium.Marker([row['Latitude'], row['Longitude']], popup=row['City']).add_to(m)

        # Save the map as an HTML file
        m.save('geographic_map.html')
        readme_file.write(f"Geographic analysis visualized in `geographic_map.html`\n\n")
        print("Geographic map saved.")

    else:
        print("No suitable geographic columns found.")
        return None

# Function for categorical data analysis
def plot_categorical_data(df, readme_file, output_dir,saved_files):
    print("Starting categorical data analysis...")
    non_numeric_df = df.select_dtypes(exclude=['number'])
    for col in non_numeric_df.columns:
        # Count the unique values in the column
        value_counts = df[col].value_counts()
        num_unique_values = len(value_counts)
        print(f"Analyzing distribution for column: {col}")

        def adjust_labels(ax, labels, max_chars_per_line=10, rotate=False):
            """
            Helper function to adjust labels by splitting long ones into multiple lines
            and optionally rotating them.
            """
            new_labels = []
            for label in labels:
                label_str = str(label)  # Ensure label is a string

                split_label = "\n".join(
                    [label_str[i:i + max_chars_per_line] for i in range(0, len(label_str), max_chars_per_line)]
                )
                new_labels.append(split_label)
            ax.set_xticks(range(len(new_labels)))
            ax.set_xticklabels(new_labels, rotation=90 if rotate else 0, ha='center' if rotate else 'right')

        if num_unique_values <= 15:
            # Case 1: Bars are up to 15, don't rotate, split long labels into multiple lines
            plt.figure(figsize=(12, 8))
            ax = sns.countplot(x=col, data=df, order=value_counts.index)
            plt.title(f"Distribution of {col}")
            adjust_labels(ax, value_counts.index, max_chars_per_line=10, rotate=False)
            plt.legend(title="Counts")
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            plt.subplots_adjust(bottom=0.25)
            generate_chart(plt, f"{col}_distribution.png", df, output_dir,saved_files)
            readme_file.write(f"![{col} Distribution]({col}_distribution.png)\n\n")
            print(f"Saved {col} distribution plot.")

        elif 15 < num_unique_values <= 30:
            # Case 2: Bars are more than 15 but up to 30, rotate labels, split into 15-character lines
            plt.figure(figsize=(12, 8))
            ax = sns.countplot(x=col, data=df, order=value_counts.index)
            plt.title(f"Distribution of {col}")
            adjust_labels(ax, value_counts.index, max_chars_per_line=15, rotate=True)
            plt.legend(title="Counts")
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            plt.subplots_adjust(bottom=0.35)
            generate_chart(plt, f"{col}_distribution.png", df, output_dir,saved_files)
            readme_file.write(f"![{col} Distribution]({col}_distribution.png)\n\n")
            print(f"Saved {col} distribution plot.")

        else:
            # Case 3: Bars are more than 30, create two graphs (top 15 and bottom 15 value-wise)
            top_15 = value_counts.head(15)
            bottom_15 = value_counts.tail(15)

            # Top 15 graph
            plt.figure(figsize=(12, 8))
            ax = sns.barplot(x=top_15.index, y=top_15.values)
            plt.title(f"Top 15 Distribution of {col}")
            adjust_labels(ax, top_15.index, max_chars_per_line=15, rotate=True)
            plt.legend(title="Counts")
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            plt.subplots_adjust(bottom=0.35)
            generate_chart(plt, f"{col}_top_15_distribution.png", df, output_dir,saved_files)
            readme_file.write(f"![{col} Top 15 Distribution]({col}_top_15_distribution.png)\n\n")
            print(f"Saved top 15 distribution for {col}.")

            # Bottom 15 graph
            plt.figure(figsize=(12, 8))
            ax = sns.barplot(x=bottom_15.index, y=bottom_15.values)
            plt.title(f"Bottom 15 Distribution of {col}")
            adjust_labels(ax, bottom_15.index, max_chars_per_line=15, rotate=True)
            plt.legend(title="Counts")
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            plt.subplots_adjust(bottom=0.35)
            generate_chart(plt, f"{col}_bottom_15_distribution.png", df, output_dir,saved_files)
            readme_file.write(f"![{col} Bottom 15 Distribution]({col}_bottom_15_distribution.png)\n\n")
            print(f"Saved bottom 15 distribution for {col}.")

# List of potential encodings to check, since we may not know provided csv file encoding
encodings_to_try = ['utf-8', 'ISO-8859-1', 'unicode_escape', 'utf-16', 'latin1']



def read_csv_with_multiple_encodings(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    enc = result['encoding']
    print("File encoding identified as:", enc )
    
    try:
        
            df = pd.read_csv(file_path, encoding=enc)
            return df  # Return the dataframe if successful
    except UnicodeDecodeError:
            # If the encoding fails, continue to the next one
            print(f"Failed to read with encoding: {enc}")
            raise ValueError("Unable to read the file with any of the provided encodings.")

    '''
    for encoding in encodings_to_try:
        try:
            # Try reading the CSV with the current encoding
            print(f"Trying encoding: {encoding}")
            df = pd.read_csv(file_path, encoding=encoding)
            print(f"File successfully read with encoding: {encoding}")
            return df  # Return the dataframe if successful
        except UnicodeDecodeError:
            # If the encoding fails, continue to the next one
            print(f"Failed to read with encoding: {encoding}")
            continue
    raise ValueError("Unable to read the file with any of the provided encodings.")
    '''


def analyze_csv(file_path):
    try:
        print(f"Reading CSV file: {file_path}")
        encoding = detect_encoding(file_path)
        df = read_csv_with_multiple_encodings(file_path)
        print(f"Successfully read CSV with {len(df)} rows and {len(df.columns)} columns.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    #Summary Statistics (for both numeric and categorical columns)
    details_summary = df.describe(include='all')

    #print(f"Shape of the DataFrame: {df.shape}")

    # Missing Values Count
    missing_values = df.isna().sum()

    # Percentage of Missing Values for each column
    missing_percentage = (df.isna().mean() * 100)

    # Displaying the missing values as percentage
    missing_info = pd.DataFrame({
        'Missing Values Count': missing_values,
        'Missing Percentage (%)': missing_percentage
    })

    print("Generated summary statistics and checked for missing values.")

    # Use the same directory as of the input CSV file
    output_dir = os.path.dirname(file_path)
    readme_path = os.path.join(output_dir, "README.md")
    analyses_path = os.path.join(output_dir, "analyses.md")
    print(f"Output directory set to: {output_dir}")

    # Track successfully created files. This is to ensure that final document has only generated file and no empty paths
    saved_files = []  

    with open(analyses_path, "w") as analysis_file:

        analysis_file.write("# Automated Data Assessment Report\n\n")
        analysis_file.write(f"## Overview\nFile: {os.path.basename(file_path)}\n\n")
        analysis_file.write("## Summarization\n")
        analysis_file.write(f"The CSV file has {len(df)} rows and {len(df.columns)} columns.\n\n")

        # Write details summary as Markdown table
        analysis_file.write("### Summary Statistics of CSV file\n")
        details_summary_str = details_summary.to_markdown()  # Converts the DataFrame to Markdown format
        analysis_file.write(details_summary_str + "\n\n")

        # Write missing values report as Markdown table
        analysis_file.write("## Missing values report\n")
        missing_info_str = missing_info.to_markdown()  # Converts the DataFrame to Markdown format
        analysis_file.write(missing_info_str + "\n\n")

        # Word Cloud
        analysis_file.write("### Word Cloud Analysis\n")
        img=generate_word_cloud(df, analysis_file, output_dir, saved_files)
        image_full_path = os.path.join(output_dir, img)
        print("Analysing image using AI bot")
        analysis_file.write(bot_helper_image(image_full_path))
        analysis_file.write("This word cloud visualizes the most frequent words from the content\n")

        # Correlation Matrix
        analysis_file.write("### Correlation Analysis\n")
        correlation = plot_correlation_matrix(df, analysis_file, output_dir, saved_files)
        if correlation is not None:
            analysis_file.write("This heatmap visualizes the correlation between numerical features in the dataset:\n")        
            analysis_file.write(f"Correlation insights:\n- {bot_helper('Provide insights on the correlation matrix.', str(correlation))}\n\n")

        # Outliers
        analysis_file.write("### Outlier Detection\n")
        plot_outliers(df, analysis_file, output_dir, saved_files)
        analysis_file.write("This boxplot shows the distribution of values for numerical features and highlights potential outliers\n")        
        analysis_file.write("Outlier insights:\n")
        analysis_file.write(f"- {bot_helper('Analyze the outliers in the data.', 'Outlier plot generated')}\n\n")

        # Time Series
        analysis_file.write("### Time Series Analysis\n")
        t = plot_time_series(df, analysis_file, output_dir, saved_files)
        if t!=None:
            analysis_file.write("This line plot shows trends over time for numerical data with a `Date` column\n")            
            analysis_file.write("Time series insights:\n")
            analysis_file.write(f"- {bot_helper('Analyze trends or patterns in the time series data.', 'Time series plot generated')}\n\n")
        else:
            analysis_file.write("### No Time Series Analysis data found. Skip this section\n")

        # Geographic Analysis
        analysis_file.write("### Geographic Distribution\n")
        g = plot_geographic_analysis(df, analysis_file, output_dir, saved_files)
        if g!=None:
            analysis_file.write("This scatter plot maps data points based on their geographic coordinates (`Latitude` and `Longitude`)\n")            
            analysis_file.write("Geographic insights:\n")
            analysis_file.write(f"- {bot_helper('What can you say about the geographic distribution?', 'Geographic plot generated')}\n\n")
        else:
            analysis_file.write("### No Geographic Distribution data found. Skip this section\n")

        # Categorical Data
        analysis_file.write("### Categorical Data Distribution\n")
        analysis_file.write("The following plots show the distribution of categorical data:\n")
        plot_categorical_data(df, analysis_file, output_dir, saved_files)        
        analysis_file.write("Categorical insights:\n")
        analysis_file.write(f"- {bot_helper('What insights can you derive from the categorical distributions?', 'Categorical plots generated')}\n\n")

        # General Insights
        analysis_context = f"Dataset summary statistics:\n{details_summary}\nMissing values:\n{missing_values}"
        analysis_response = bot_helper("Analyze the dataset and provide insights.", analysis_context)
        analysis_file.write("## General Insights\n")
        analysis_file.write(f"{analysis_response}\n\n")

        # Numeric Insights
        numeric_context = f"Numeric columns summary:\n{df.select_dtypes(include=['number']).describe()}"
        numeric_response = bot_helper("Provide insights about numeric columns.", numeric_context)
        analysis_file.write("## Numeric Insights\n")
        analysis_file.write(f"{numeric_response}\n\n")        


    # Now write the story to README.md, integrating images and captions
    with open(readme_path, "w") as readme_file, open(analyses_path, "r") as analysis_file:
        analyses_content = analysis_file.read()
        story_context = f"Dataset Analysis:\n{analyses_content}"
        story = bot_helper(
            "Generate a creative but data-driven story based on the analysis. It should be in markdown format, well-structured, using headers, lists, and emphasis appropriately. "+
            "The narrative should clearly describes the data to users, analysis performed, insights or anomalies identified, and implications. Include relevant images from the analysis "
            "and describe them in the story to make it visually engaging. Use external hyperlinks and references to strengthen the storyline",
            story_context
        )
        #"   Focus on four aspects:  a) The data you received b) The analysis you carried out c) The insights you discovered d) The implications of findings."
        readme_file.write("#### *Every story is complicated until it finds the right storyteller — Anonymous*\n\n\n")
        readme_file.write(f"{story}\n")
        print("Added story to README.md file")

    print(f"Analysis of the data is complete. Interim results saved to {analyses_path} and final story to {readme_path}")


# Start here
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("The usage format to run this file: uv run autolysis.py <data.csv file>")
        sys.exit(1)
    dataset_path = sys.argv[1]
    print(f"Starting data analysis on file {dataset_path}...")
    analyze_csv(dataset_path)
