# ChatGPT in Higher Education: Expert and Public Perceptions

This repository contains the data, code, and results for the study on expert and public perceptions of ChatGPT in higher education.

## Repository Structure

### 1. Data

The raw datasets, filtered and processed data used throughout the analysis are stored here: https://drive.google.com/drive/folders/1nXKC23aA8rBMQvrlcb5u2E7OWFJr_rPf?usp=sharing.

### 2. Code

The code is organized into three main sections: data collection, preprocessing, and analysis.

#### **Data Collection**
- `scripts/`: Contains all scripts related to data collection.
- `subreddits_selection.ipynb`: Notebook for selecting relevant subreddits for data collection.

#### **Preprocessing**
- `combine_public_data.py`: Combine post with comments
- `add_id_expert.py`: Adds unique identifiers to the expert dataset.
- `clean_text_data.py`: Cleans and preprocesses text data for analysis.
- `load_and_chunk_data.py`: Loads and chunks large expert datasets into manageable segments.
- `public_filter_again.py`: Filters public data with refined criteria.
- `replace_public_with_filtered.py`: Replaces raw public data with filtered versions.

#### **Topic Modeling**
- `calculate_embeddings.ipynb`: Notebook for generating text embeddings for topic modeling.
- `dimention_reduction.ipynb`: Performs dimensionality reduction on the embeddings.
- `clustering+BERTopic.ipynb`: Clusters the data and applies BERTopic for topic extraction.
- `remove_irrelevant_documents.ipynb`: Remove documents from the irrelavant topic

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
