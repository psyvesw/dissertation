# ChatGPT in Higher Education: Expert and Public Perceptions

This repository contains the data, code, and results for the study on expert and public perceptions of ChatGPT in higher education. The project employs advanced Natural Language Processing (NLP) techniques, including topic modeling and sentiment analysis, to analyze discourse from both experts and the public.

## Repository Structure

### 1. Data

- **Raw Data**: The raw datasets are stored in compressed files.
  - `expert_raw_data.zip`: Contains the raw expert data.
  - `public_raw_data.zip`: Contains the raw public data.
  
- **Filtered Data**: The filtered and processed data used throughout the analysis is stored in an SQLite database.
  - `all_data.db.zip`: The database containing all filtered data used in the analysis, stored in an SQLite format.

### 2. Code

The code is organized into three main sections: data collection, preprocessing, and analysis.

#### **Data Collection**
- `scripts/`: Contains all scripts related to data collection.
- `subreddits_selection.ipynb`: Notebook for selecting relevant subreddits for data collection.

#### **Preprocessing**
- `combine_public_data.py`: combine post with comments
- `add_id_expert.py`: Adds unique identifiers to the expert dataset.
- `clean_text_data.py`: Cleans and preprocesses text data for analysis.
- `load_and_chunk_data.py`: Loads and chunks large expert datasets into manageable segments.
- `public_filter_again.py`: Filters public data with refined criteria.
- `replace_public_with_filtered.py`: Replaces raw public data with filtered versions.

#### **Topic Modeling**
- `calculate_embeddings.ipynb`: Notebook for generating text embeddings for topic modeling.
- `dimention_reduction.ipynb`: Performs dimensionality reduction on the embeddings.
- `clustering+BERTopic.ipynb`: Clusters the data and applies BERTopic for topic extraction.
- `remove_irrelevant_documents.ipynb`: remove documents from the irrelavant topic

#### **Sentiment Analysis**
- `sentiment_analysis.ipynb`: Conducts sentiment analysis on the expert and public datasets.

### 3. Results

- **Subreddit Information**
  - `subreddit_data.csv`: Contains details on the subreddits selected for data collection.

- **Expert Themes**
  - `expert_theme.xlsx`: Contains all expert themes, along with corresponding subtopics (old name + new name), keywords, and representative documents.

- **Public Themes**
  - `public_theme.xlsx`: Contains all public themes, along with corresponding subtopics (old name + new name), keywords, and representative documents.

- **Sentiment Results**
  - `sentiment_analysis_results.xlsx`: Contains the results of the sentiment analysis.

- **Interactive Visualizations**
  - `expert_sunburst.html`: Interactive sunburst graph visualizing expert themes and subtopics.
  - `public_sunburst.html`: Interactive sunburst graph visualizing public themes and subtopics.
