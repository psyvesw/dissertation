import sqlite3
import pandas as pd
import re
import emoji
from langdetect import detect

# Function to clean text
def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+|www.\S+', '', text)
    # Remove user mentions and hashtags
    text = re.sub(r'@\w+|#\w+', '', text)
    # Remove emojis
    text = emoji.replace_emoji(text, replace='')
    # Normalize text to lowercase
    text = text.lower()
    return text

# Function to identify and remove bot-generated content
def is_bot(author):
    return bool(re.search(r'bot', author, re.IGNORECASE))

# Function to detect language and filter non-English text
def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False

# Function to check if text is clean
def check_cleaned_text(text):
    # Check for URLs
    url_check = re.search(r'http\S+|www.\S+', text) is None
    # Check for user mentions and hashtags
    mention_hashtag_check = re.search(r'@\w+|#\w+', text) is None
    # Check for emojis
    emoji_check = emoji.replace_emoji(text) == text
    # Check for lowercase
    lowercase_check = text == text.lower()
    return url_check and mention_hashtag_check and emoji_check and lowercase_check

# Connect to the SQLite database
db_path = "/Users/vesper/Desktop/LSE/Capstone Project/dissertation/arctic_shift/filtered_data/relevant_data.db"
conn = sqlite3.connect(db_path)

# Load combined public data
public_data = pd.read_sql_query("SELECT * FROM combined_public_data", conn)

# Debug: Check initial data sample
print("Initial Public Data Sample:")
print(public_data[['text']].sample(5))

# Remove bot-generated content
public_data = public_data[~public_data['author'].apply(is_bot)]

# Remove rows with missing text
public_data = public_data.dropna(subset=['text'])

# Filter non-English content
public_data = public_data[public_data['text'].apply(is_english)]

# Debug: Check data sample after language filtering
print("Public Data Sample After Language Filtering:")
print(public_data[['text']].sample(5))

# Apply the cleaning function to the text column
public_data['cleaned_text'] = public_data['text'].apply(clean_text)

# Debug: Check data sample after cleaning
print("Public Data Sample After Cleaning:")
print(public_data[['text', 'cleaned_text']].sample(5))

# Remove duplicates
public_data = public_data.drop_duplicates(subset='cleaned_text')

# Save the cleaned public data to a new table in the SQLite database
public_data.to_sql('cleaned_public_data', conn, if_exists='replace', index=False)

# Load expert data
expert_data = pd.read_sql_query("SELECT * FROM chunked_expert_data", conn)

# Debug: Check initial data sample
print("Initial Expert Data Sample:")
print(expert_data[['content']].sample(5))

# Remove rows with missing content
expert_data = expert_data.dropna(subset=['content'])

# Filter non-English content
expert_data = expert_data[expert_data['content'].apply(is_english)]

# Debug: Check data sample after language filtering
print("Expert Data Sample After Language Filtering:")
print(expert_data[['content']].sample(5))

# Apply the cleaning function to the content column
expert_data['cleaned_content'] = expert_data['content'].apply(clean_text)

# Debug: Check data sample after cleaning
print("Expert Data Sample After Cleaning:")
print(expert_data[['content', 'cleaned_content']].sample(5))

# Remove duplicates
expert_data = expert_data.drop_duplicates(subset='cleaned_content')

# Save the cleaned expert data to a new table in the SQLite database
expert_data.to_sql('cleaned_expert_data', conn, if_exists='replace', index=False)

# Verify Cleaning
# Sample size for inspection
sample_size = 10

# Function to verify cleaning
def verify_cleaning(data, text_column):
    sample = data.sample(n=sample_size)
    sample['is_clean'] = sample[text_column].apply(check_cleaned_text)
    return sample[['id', text_column, 'is_clean']]

# Verify cleaned public data
public_sample = verify_cleaning(public_data, 'cleaned_text')
print("Public Data Cleaning Verification Sample:")
print(public_sample)

# Verify cleaned expert data
expert_sample = verify_cleaning(expert_data, 'cleaned_content')
print("Expert Data Cleaning Verification Sample:")
print(expert_sample)

# Close the database connection
conn.close()

print("Text data has been cleaned, verified, and saved back to the SQLite database.")
