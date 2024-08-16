import sqlite3
import pandas as pd

# Connect to the SQLite database
db_path = "/Users/vesper/Desktop/LSE/Capstone Project/dissertation/arctic_shift/filtered_data/relevant_data.db"
conn = sqlite3.connect(db_path)

# Load the filtered public dataset
filtered_public_data = pd.read_sql_query("SELECT * FROM filtered_public_data", conn)

# Replace the contents of cleaned_public_data with filtered_public_data
filtered_public_data.to_sql('cleaned_public_data', conn, if_exists='replace', index=False)

conn.close()

print("cleaned_public_data has been updated with the filtered public data.")
