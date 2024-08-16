import sqlite3
import pandas as pd
import re

def chunk_text_by_paragraph(text, max_chunk_size=500):
    paragraphs = text.split('\n\n')
    chunks = []
    
    for paragraph in paragraphs:
        words = paragraph.split()
        
        if len(words) > max_chunk_size:
            for i in range(0, len(words), max_chunk_size):
                chunks.append(' '.join(words[i:i + max_chunk_size]))
        else:
            chunks.append(paragraph)
    
    return chunks

# Load the CSV file into a DataFrame
csv_path = "/Users/vesper/Desktop/LSE/Capstone Project/dissertation/data/expert_data/expert_data.csv"
expert_data = pd.read_csv(csv_path)

# Add a unique identifier to each row
expert_data['document_id'] = expert_data.index + 1

# Connect to the SQLite database
db_path = "/Users/vesper/Desktop/LSE/Capstone Project/dissertation/arctic_shift/filtered_data/relevant_data.db"
conn = sqlite3.connect(db_path)

# Create a new DataFrame to store chunked data
chunked_data = []

for index, row in expert_data.iterrows():
    chunks = chunk_text_by_paragraph(row['content'])
    for i, chunk in enumerate(chunks):
        chunked_data.append({
            'original_id': row['document_id'],
            'source': row['source'],
            'title': row['title'],
            'author': row.get('author', ''),  # Add a check for the author column if it exists
            'publication_date': row['publication_date'],
            'content': chunk,
            'chunk_id': i + 1
        })

# Convert chunked data to DataFrame
chunked_df = pd.DataFrame(chunked_data)

# Write the chunked DataFrame to a new table in the SQLite database
chunked_df.to_sql('chunked_expert_data', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()

print("Data has been successfully loaded, chunked by paragraph, and stored in the SQLite database.")
