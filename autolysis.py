import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import chardet
from datetime import datetime
from matplotlib import rcParams
import re
from wordcloud import WordCloud
import os
import subprocess
import sys
import base64
import requests
import json
import base64
import openai
from openai import OpenAI

# Function to check and install required packages
def install_package(package):
    try:
        print(f"Attempting to install {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}.")
    except subprocess.CalledProcessError:
        print(f"Error installing package: {package}")
        sys.exit(1)

# List of required packages
required_packages = [
    'pandas', 
    'matplotlib', 
    'seaborn', 
    'tabulate',
    'requests', 
    'chardet',    
    'wordcloud'
]

# Install missing packages
for package in required_packages:
    try:
        print(f"Checking if {package} is installed...")
        __import__(package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"Package {package} not found. Installing...")
        install_package(package)

client = OpenAI()

# Configuration Section
CONFIG = {
    "AI_PROXY_URL": "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
    #"AI_PROXY_URL": "https://api.openai.com/v1/chat/completions",
    "AI_PROXY_TOKEN": os.getenv("AIPROXY_TOKEN")
}

HEADERS = {"Authorization": f"Bearer {CONFIG['AI_PROXY_TOKEN']}", "Content-Type": "application/json"}

saved_charts = []

# Set the API key globally for the OpenAI library
openai.api_key =  {CONFIG['AI_PROXY_TOKEN']}


# Function to generate a word cloud
def generate_word_cloud(df, readme_file, output_dir, saved_files):
    print("Starting word cloud analysis...")

    # Combine all text data from the dataframe into one large string
    all_text = ""
    for col in df.select_dtypes(include=['object']).columns:
        all_text += " " + " ".join(df[col].dropna().astype(str))

    # Remove URLs using regular expression
    all_text = re.sub(r'http[s]?://\S+', '', all_text)  # Remove URLs
    all_text = re.sub(r'\b\w{1,2,3}\b', '', all_text)   # Remove words shorter than 3 characters

    # Generate the word cloud
    wordcloud = WordCloud(width=400, height=200, background_color="white", max_words=200).generate(all_text)

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



def encode_image(image_path):
    """Encode an image to a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def bot_helper_image(image_path, question="Describe the data and text in this image."):
    """Send an image and question to OpenAI GPT-4 Vision model for analysis."""
    # API Endpoint
    endpoint = CONFIG['AI_PROXY_URL']
    
    # Set your OpenAI API key
    api_key = CONFIG["AI_PROXY_TOKEN"]

    # Encode the image to base64
    base64_image = encode_image(image_path)

    # Create the payload
    payload = {
        "model": "gpt-4o-mini",  # Ensure this is the correct vision model
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

    # Define headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        # Make the API request
        response = requests.post(endpoint, json=payload, headers=headers)
        print(response)
        response.raise_for_status()  # Raise an error for bad HTTP status codes

        # Parse and return the response
        response_json = response.json()
        if "choices" in response_json and response_json["choices"]:
            return response_json["choices"][0]["message"]["content"]
        else:
            return "Unexpected response format."

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"




# Function to interact with LLM via AI Proxy
def bot_helper(question, context):
    try:
        print(f"Sending query to AI LLM bot: {question}")
        payload = {
            "model": "gpt-4o-mini",  # Adjust based on the actual model you're allowed to use
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
        response = requests.post(CONFIG["AI_PROXY_URL"], headers=HEADERS, json=payload)
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

# Function to save visualizations with quality check
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

# Function to visualize outliers
def plot_outliers(df, readme_file, output_dir, saved_files):
    print("Starting outlier analysis...")
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty:
        print("No numeric data for outlier analysis.")
        return
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=numeric_df)
    plt.title("Outlier Detection")
    
    # Rotate the x-axis labels to be vertical
    plt.xticks(rotation=90)
    
    # Save the visualization
    generate_chart(plt, "outliers.png", df, output_dir, saved_files)
    readme_file.write(f"![Outlier Detection](outliers.png)\n\n")
    print("Outlier plot saved.")

# Function for time series analysis
def plot_time_series(df, readme_file, output_dir,saved_files):
    print("Starting time series analysis...")
    if 'Date' in df.columns:
        try:
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date')
            numeric_columns = df.select_dtypes(include=['number']).columns
            if numeric_columns.empty:
                print("No numeric columns for time series analysis.")
                return
            plt.figure(figsize=(12, 6))
            sns.lineplot(data=df, x='Date', y=numeric_columns[0])
            plt.title(f"Time Series Analysis for {numeric_columns[0]}")
            plt.legend([numeric_columns[0]], loc='upper left')  # Add legend
            generate_chart(plt, "time_series.png", df, output_dir,saved_files)
            readme_file.write(f"![Time Series Analysis](time_series.png)\n\n")
            print("Time series plot saved.")
        except Exception as e:
            print(f"Error in Time Series Analysis: {e}")
    else:
        print("Date column not found for time series analysis.")
        return None

# Function for geographic analysis
def plot_geographic_analysis(df, readme_file, output_dir,saved_files):
    print("Starting geographic analysis...")
    if 'Latitude' in df.columns and 'Longitude' in df.columns:
        plt.figure(figsize=(10, 8))
        numeric_column = df.select_dtypes(include=['number']).columns[0] if not df.select_dtypes(include=['number']).empty else 'Count'
        sns.scatterplot(data=df, x='Longitude', y='Latitude', hue=numeric_column)
        plt.title("Geographic Analysis")
        plt.legend(title=numeric_column)
        generate_chart(plt, "geographic_analysis.png", df, output_dir,saved_files)
        readme_file.write(f"![Geographic Analysis](geographic_analysis.png)\n\n")
        print("Geographic plot saved.")
    else:
        print("Latitude and Longitude columns are missing.")
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
                split_label = "\n".join(
                    [label[i:i + max_chars_per_line] for i in range(0, len(label), max_chars_per_line)]
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

# List of potential encodings to check
encodings_to_try = ['utf-8', 'ISO-8859-1', 'unicode_escape', 'utf-16', 'latin1']

def read_csv_with_multiple_encodings(file_path):
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

    print(f"Shape of the DataFrame: {df.shape}")

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

    # Use the directory of the input CSV file
    output_dir = os.path.dirname(file_path)
    readme_path = os.path.join(output_dir, "README.md")
    analyses_path = os.path.join(output_dir, "analyses.md")
    print(f"Output directory set to: {output_dir}")

    saved_files = []  # Track successfully created files

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
            "The narrative should clearly describes the data, analysis performed, insights gained, and implications. Include relevant images from the analysis "
            "and describe them in the story to make it visually engaging. Use external hyperlinks and references to strengthen the storyline",
            story_context
        )
        #"   Focus on four aspects:  a) The data you received b) The analysis you carried out c) The insights you discovered d) The implications of findings."
        readme_file.write("#### *Every story is complicated until it finds the right storyteller — Anonymous*\n\n\n")
        readme_file.write(f"{story}\n")
        print("Added story to README.md.")

    print("Analysis complete! Results saved to analyses.md and story to README.md in the same directory as the input CSV file.")



# Start here
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("The usage format of this file: uv run autolysis.py <dataset.csv>")
        sys.exit(1)
    dataset_path = sys.argv[1]
    print(f"Starting analysis on {dataset_path}...")
    analyze_csv(dataset_path)
