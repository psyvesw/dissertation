import sqlite3
import pandas as pd

# Connect to the SQLite database
db_path = "/Users/vesper/Desktop/LSE/Capstone Project/dissertation/arctic_shift/filtered_data/relevant_data.db"
conn = sqlite3.connect(db_path)

# Load the comments and posts tables
comments = pd.read_sql_query("SELECT id, body AS text, author, created_utc, permalink, score FROM comments", conn)
posts = pd.read_sql_query("SELECT id, (title || ' ' || selftext) AS text, author, created_utc, permalink, score FROM posts", conn)

# Combine the dataframes
public_data = pd.concat([comments, posts])

# Close the database connection
conn.close()

# Save the combined data to a new table in the SQLite database
conn = sqlite3.connect(db_path)
public_data.to_sql('combined_public_data', conn, if_exists='replace', index=False)
conn.close()

print("Combined public data has been saved to the SQLite database.")